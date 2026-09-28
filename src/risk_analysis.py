"""
risk_analysis.py  -  6번 담당: 소상공인 위험신호 분석

목적: 매출·상권·대출 정보를 바탕으로 은행원이 추가로 확인해야 할 고객을 찾는다.
주의: 대출 승인·부실 판정용이 아니라 '추가 확인 대상'을 찾는 참고지표다.

실행: python risk_analysis.py
결과: output/ 폴더에 CSV 3개 저장 (대시보드·AI 브리핑에서 사용)
"""
import pandas as pd
from pathlib import Path

# ------------------------------------------------------------
# 설정: 파일 위치
#   이 코드 파일이 있는 폴더 기준으로 CSV를 찾는다.
#   CSV가 같은 폴더에 있어도, data 폴더 안에 있어도 둘 다 동작한다.
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
CSV_NAME = "financial_products_with_small_business_customers.csv"
candidates = [BASE_DIR / CSV_NAME, BASE_DIR / "data" / CSV_NAME]
PRODUCT_FILE = next((p for p in candidates if p.exists()), None)
if PRODUCT_FILE is None:
    raise FileNotFoundError(
        f"{CSV_NAME} 파일을 찾을 수 없습니다. 이 코드 파일과 같은 폴더나 data 폴더에 넣어주세요.\n"
        f"찾아본 위치: {BASE_DIR}"
    )
OUTPUT_DIR = BASE_DIR / "output"


# ============================================================
# STEP 1. 데이터 불러오기
# ============================================================
df = pd.read_csv(PRODUCT_FILE, encoding="utf-8-sig")
print("[STEP 1] 원본:", df.shape[0], "행 (상품 가입 1건 = 1행)")


# ============================================================
# STEP 2. 고객 단위로 중복 제거
#   원본은 고객 1명이 상품을 여러 건 가입해서 같은 대출잔액이 반복된다.
#   그대로 합치면 대출잔액이 약 3.3배 부풀려지므로 고객당 1행만 남긴다.
# ============================================================
cust_cols = [
    "customer_id", "행정동_코드", "지역", "업종",
    "가상_고객_매출_금액", "가상_고객_매출_증감률", "상권_매출_증감률",
    "대출_보유_여부", "대출_종류", "대출_잔액",
]
cust = df[cust_cols].drop_duplicates("customer_id").copy()

# 고객별 금융상품 가입 요약 (가입 건수, 가입금액 합계)
prod = df.groupby("customer_id").agg(
    상품_가입_건수=("subscription_id", "count"),
    상품_가입금액_합계=("amount", "sum"),
)
cust = cust.merge(prod, on="customer_id", how="left")
print("[STEP 2] 고객 수:", len(cust), "명")


# ============================================================
# STEP 3. 위험신호 계산에 쓸 지표 만들기
# ============================================================
# 상권 대비 격차: 음수면 '같은 동네·같은 업종보다 이 가게가 더 나쁘다'는 뜻
cust["상권_대비_격차"] = cust["가상_고객_매출_증감률"] - cust["상권_매출_증감률"]

# 매출 대비 대출 비율: 클수록 매출에 비해 갚아야 할 돈이 많다
cust["매출_대비_대출_비율"] = cust["대출_잔액"] / cust["가상_고객_매출_금액"]


# ============================================================
# STEP 4. 기준값 정하기 (임의 숫자 대신 데이터 분포 사용)
#   '하위 25%' = 전체 고객을 줄 세웠을 때 가장 나쁜 4분의 1
# ============================================================
TH = {
    "고객_매출_감소": cust["가상_고객_매출_증감률"].quantile(0.25),
    "상권_대비_부진": cust["상권_대비_격차"].quantile(0.25),
    "상권_악화": cust["상권_매출_증감률"].quantile(0.25),
    # 대출 부담은 대출 보유 고객끼리 비교해서 상위 25%
    "대출_부담_과다": cust.loc[cust["대출_보유_여부"] == "Y",
                             "매출_대비_대출_비율"].quantile(0.75),
}
for k, v in TH.items():
    print(f"[STEP 4] 기준값 {k}: {v:.3f}")


# ============================================================
# STEP 5. 위험신호 4개 적용 (True = 신호 있음)
# ============================================================
cust["신호_매출감소"] = cust["가상_고객_매출_증감률"] <= TH["고객_매출_감소"]
cust["신호_상권대비부진"] = cust["상권_대비_격차"] <= TH["상권_대비_부진"]
cust["신호_상권악화"] = cust["상권_매출_증감률"] <= TH["상권_악화"]
cust["신호_대출부담"] = (cust["대출_보유_여부"] == "Y") & \
                     (cust["매출_대비_대출_비율"] >= TH["대출_부담_과다"])

signal_cols = ["신호_매출감소", "신호_상권대비부진", "신호_상권악화", "신호_대출부담"]
cust["신호_개수"] = cust[signal_cols].sum(axis=1)


# ============================================================
# STEP 6. 위험등급과 유형 붙이기
#   우선점검: 신호 2개 이상 + 대출 보유 (갚아야 할 돈이 있어 사후관리 필요)
#   관찰:     신호 2개 이상 + 대출 미보유 (상담 시 참고)
#   정상:     그 외
# ============================================================
def grade(row):
    if row["신호_개수"] >= 2 and row["대출_보유_여부"] == "Y":
        return "우선점검"
    if row["신호_개수"] >= 2:
        return "관찰"
    return "정상"


def risk_type(row):
    # 은행원이 무엇을 확인해야 하는지 방향을 잡기 위한 분류
    if row["신호_매출감소"] and row["신호_상권악화"]:
        return "상권동반형"      # 지역·업종 전체가 어려움
    if row["신호_매출감소"] and row["신호_상권대비부진"]:
        return "개별부진형"      # 상권은 괜찮은데 이 가게만 부진
    if row["신호_대출부담"]:
        return "대출부담형"
    return "-"


cust["위험등급"] = cust.apply(grade, axis=1)
cust["위험유형"] = cust.apply(risk_type, axis=1)


# ============================================================
# STEP 7. 결과가 맞는지 스스로 검증
# ============================================================
assert cust["customer_id"].is_unique, "고객 중복이 남아 있음"
assert len(cust) == df["customer_id"].nunique(), "고객 수 불일치"
loan_rows = df["대출_잔액"].sum()
loan_cust = cust["대출_잔액"].sum()
print(f"[STEP 7] 대출잔액 합계: 행 기준 {loan_rows:,}원 → 고객 기준 {loan_cust:,}원 "
      f"({loan_rows / loan_cust:.1f}배 과대 방지)")
print("[STEP 7] 등급별 고객 수:", cust["위험등급"].value_counts().to_dict())


# ============================================================
# STEP 8. 결과 저장 (대시보드·AI 브리핑·팀원 교차검증용)
# ============================================================
import os
os.makedirs(OUTPUT_DIR, exist_ok=True)

# (1) 고객별 위험신호 전체
cust.to_csv(f"{OUTPUT_DIR}/risk_customers.csv", index=False, encoding="utf-8-sig")

# (2) 업종별 요약
summary = cust.groupby("업종").agg(
    고객수=("customer_id", "count"),
    우선점검_고객수=("위험등급", lambda s: (s == "우선점검").sum()),
    대출보유_고객수=("대출_보유_여부", lambda s: (s == "Y").sum()),
    대출잔액_합계=("대출_잔액", "sum"),
    고객매출증감률_중앙값=("가상_고객_매출_증감률", "median"),
)
summary["우선점검_비율(%)"] = (summary["우선점검_고객수"] / summary["고객수"] * 100).round(1)
summary = summary.sort_values("우선점검_비율(%)", ascending=False)
summary.to_csv(f"{OUTPUT_DIR}/risk_summary_by_industry.csv", encoding="utf-8-sig")

# (3) 사용한 기준값 기록 (README·발표 근거)
pd.DataFrame(
    [{"신호": k, "기준값": round(v, 3), "근거": "하위 25%" if k != "대출_부담_과다" else "대출 보유자 중 상위 25%"}
     for k, v in TH.items()]
).to_csv(f"{OUTPUT_DIR}/risk_thresholds.csv", index=False, encoding="utf-8-sig")

print("[STEP 8] 저장 완료: risk_customers.csv / risk_summary_by_industry.csv / risk_thresholds.csv")
