import { useMemo, useState } from 'react';
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { customers } from './data/mockData';

const money = new Intl.NumberFormat('ko-KR');

function formatMoney(value) {
  return `${money.format(value)}만원`;
}

function formatPercent(value) {
  return `${value.toFixed(1)}%`;
}

function App() {
  const [customerId, setCustomerId] = useState(customers[0].customerId);
  const [searchedId, setSearchedId] = useState(customers[0].customerId);

  const customer = useMemo(() => {
    return customers.find((item) => item.customerId === searchedId);
  }, [searchedId]);

  function handleSubmit(event) {
    event.preventDefault();
    setSearchedId(customerId.trim());
  }

  return (
    <main className="dashboard">
      <h1>소상공인 고객 분석 대시보드</h1>

      <section>
        <h2>CUSTOMER_ID 검색</h2>
        <form className="search-form" onSubmit={handleSubmit}>
          <input
            value={customerId}
            onChange={(event) => setCustomerId(event.target.value)}
            placeholder="예: CUST-1001"
          />
          <button type="submit">조회</button>
        </form>
        <p>조회 가능 ID: {customers.map((item) => item.customerId).join(', ')}</p>
      </section>

      {!customer && (
        <section>
          <h2>조회 결과</h2>
          <p>일치하는 고객이 없습니다.</p>
        </section>
      )}

      {customer && (
        <>
          <section>
            <h2>고객 기본정보</h2>
            <table>
              <tbody>
                <tr>
                  <th>고객ID</th>
                  <td>{customer.customerId}</td>
                </tr>
                <tr>
                  <th>지역(상권)</th>
                  <td>{customer.marketArea}</td>
                </tr>
                <tr>
                  <th>업종</th>
                  <td>{customer.industry}</td>
                </tr>
                <tr>
                  <th>기준분기</th>
                  <td>{customer.baseQuarter}</td>
                </tr>
              </tbody>
            </table>
          </section>

          <section>
            <h2>금융 현황</h2>
            <table>
              <tbody>
                <tr>
                  <th>가입 금융상품</th>
                  <td>{customer.finance.products.join(', ')}</td>
                </tr>
                <tr>
                  <th>대출 여부</th>
                  <td>{customer.finance.hasLoan ? '있음' : '없음'}</td>
                </tr>
                <tr>
                  <th>대출 종류</th>
                  <td>{customer.finance.loanType || '-'}</td>
                </tr>
                <tr>
                  <th>대출 잔액</th>
                  <td>{formatMoney(customer.finance.loanBalance)}</td>
                </tr>
              </tbody>
            </table>
          </section>

          <section className="summary" aria-label="매출 현황">
            <article>
              <strong>고객 매출</strong>
              <span>{formatMoney(customer.sales.currentSales)}</span>
            </article>
            <article>
              <strong>매출 증감률</strong>
              <span>{formatPercent(customer.sales.salesGrowthRate)}</span>
            </article>
            <article>
              <strong>동일 상권·업종 평균 매출</strong>
              <span>{formatMoney(customer.sales.peerAverageSales)}</span>
            </article>
          </section>

          <section>
            <h2>분기별 매출 비교</h2>
            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={customer.quarterlySales}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="quarter" />
                <YAxis />
                <Tooltip formatter={(value) => formatMoney(value)} />
                <Legend />
                <Line type="monotone" dataKey="customerSales" name="고객 매출" stroke="#2563eb" strokeWidth={2} />
                <Line type="monotone" dataKey="peerAverageSales" name="동일 상권·업종 평균 매출" stroke="#16a34a" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </section>

          <section>
            <h2>상담 참고정보</h2>
            <p>추후 분석 결과 표시 영역</p>
          </section>
        </>
      )}
    </main>
  );
}

export default App;
