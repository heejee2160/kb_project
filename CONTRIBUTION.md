공찬석:필요 데이터 셋 탐색, python위험신호, ai판단
김규린:필요 데이터 셋 탐색, sql 상권, 대출분석
김소희:주제 설정, 가상 데이터 형성, 역할 배분, pandas 고객금융분석
김하연:공공 데이터 정제, SQL DB 형성, 대시보드
류강민:필요 데이터 셋 탐색,sql 금융상품 분석
sql/oracle_financial_analysis.sql: Oracle 19c/21c DDL, 분석 뷰(VW_FINANCIAL_ANALYSIS, VW_MARKET_SALES_CLEAN), 1~4단계 SQL 분석 쿼리
src/verify_and_execute_analysis.py: SQLite/Pandas 5대 정합성 검증 파이프라인 (건수 6,000건, 총액 1,180.8억원, 상권 Fan-out 차단 100% 검증)
data/dashboard/api_products.json & api_products.csv: 대시보드 API (/api/products) 연계용 3,607건 요약 데이터
src/app_api_snippet.py: Flask 백엔드 연계 엔드포인트 구현 코드
report/2번_담당자_금융상품_분석_완료_보고서.md: 상세 분석 결과 보고서
실행 방법:
python src/verify_and_execute_analysis.py
최희지:필요 데이터 셋 탐색, readme 작성, 저장소 관리, 브랜치, 커밋 규칙 형성, pandas 상권 비교분석 보조
홍준표:필요 데이터 셋 탐색:pandas 상권 비교 분석
