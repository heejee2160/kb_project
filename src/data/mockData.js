export const customers = [
  {
    customerId: 'CUST-1001',
    marketArea: '서울 강남구 역삼 상권',
    industry: '음식점',
    baseQuarter: '2024 Q4',
    finance: {
      products: ['사업자 입출금', '카드가맹 정산', '사업자 대출'],
      hasLoan: true,
      loanType: '운전자금 대출',
      loanBalance: 4200,
    },
    sales: {
      currentSales: 9200,
      salesGrowthRate: -4.8,
      peerAverageSales: 9800,
    },
    quarterlySales: [
      { quarter: '2024 Q1', customerSales: 8700, peerAverageSales: 9300 },
      { quarter: '2024 Q2', customerSales: 9600, peerAverageSales: 9700 },
      { quarter: '2024 Q3', customerSales: 10100, peerAverageSales: 9900 },
      { quarter: '2024 Q4', customerSales: 9200, peerAverageSales: 9800 },
    ],
  },
  {
    customerId: 'CUST-1002',
    marketArea: '서울 마포구 홍대 상권',
    industry: '카페',
    baseQuarter: '2024 Q4',
    finance: {
      products: ['사업자 입출금', '적금', '카드가맹 정산'],
      hasLoan: false,
      loanType: '',
      loanBalance: 0,
    },
    sales: {
      currentSales: 6100,
      salesGrowthRate: 6.1,
      peerAverageSales: 5800,
    },
    quarterlySales: [
      { quarter: '2024 Q1', customerSales: 5100, peerAverageSales: 5400 },
      { quarter: '2024 Q2', customerSales: 5600, peerAverageSales: 5600 },
      { quarter: '2024 Q3', customerSales: 5750, peerAverageSales: 5700 },
      { quarter: '2024 Q4', customerSales: 6100, peerAverageSales: 5800 },
    ],
  },
  {
    customerId: 'CUST-1003',
    marketArea: '서울 성동구 성수 상권',
    industry: '소매',
    baseQuarter: '2024 Q4',
    finance: {
      products: ['사업자 입출금', '사업자 대출', '신용카드'],
      hasLoan: true,
      loanType: '시설자금 대출',
      loanBalance: 7800,
    },
    sales: {
      currentSales: 7400,
      salesGrowthRate: -9.3,
      peerAverageSales: 8600,
    },
    quarterlySales: [
      { quarter: '2024 Q1', customerSales: 8300, peerAverageSales: 8200 },
      { quarter: '2024 Q2', customerSales: 8100, peerAverageSales: 8400 },
      { quarter: '2024 Q3', customerSales: 7900, peerAverageSales: 8500 },
      { quarter: '2024 Q4', customerSales: 7400, peerAverageSales: 8600 },
    ],
  },
];
