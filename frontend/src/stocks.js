export const INDIAN_STOCKS = [
  { name: "Reliance Industries Limited", symbol: "RELIANCE.NS", sector: "Energy & Telecom", exchange: "NSE" },
  { name: "Tata Consultancy Services (TCS)", symbol: "TCS.NS", sector: "IT Services", exchange: "NSE" },
  { name: "HDFC Bank Limited", symbol: "HDFCBANK.NS", sector: "Banking", exchange: "NSE" },
  { name: "Infosys Limited", symbol: "INFY.NS", sector: "IT Services", exchange: "NSE" },
  { name: "ICICI Bank Limited", symbol: "ICICIBANK.NS", sector: "Banking", exchange: "NSE" },
  { name: "State Bank of India (SBI)", symbol: "SBIN.NS", sector: "Banking", exchange: "NSE" },
  { name: "Bharti Airtel Limited", symbol: "BHARTIARTL.NS", sector: "Telecom", exchange: "NSE" },
  { name: "ITC Limited", symbol: "ITC.NS", sector: "Consumer Goods", exchange: "NSE" },
  { name: "Larsen & Toubro Limited (L&T)", symbol: "LT.NS", sector: "Infrastructure", exchange: "NSE" },
  { name: "Hindustan Unilever Limited", symbol: "HINDUNILVR.NS", sector: "Consumer Goods", exchange: "NSE" },
  { name: "Bajaj Finance Limited", symbol: "BAJFINANCE.NS", sector: "Banking", exchange: "NSE" },
  { name: "Maruti Suzuki India Limited", symbol: "MARUTI.NS", sector: "Automotive", exchange: "NSE" },
  { name: "Titan Company Limited", symbol: "TITAN.NS", sector: "Consumer Goods", exchange: "NSE" },
  { name: "Sun Pharmaceutical Industries", symbol: "SUNPHARMA.NS", sector: "Healthcare", exchange: "NSE" },
  { name: "Wipro Limited", symbol: "WIPRO.NS", sector: "IT Services", exchange: "NSE" },
  { name: "Kotak Mahindra Bank", symbol: "KOTAKBANK.NS", sector: "Banking", exchange: "NSE" },
  { name: "Tata Consumer Products", symbol: "TATACONSUM.NS", sector: "Consumer Goods", exchange: "NSE" }
];

export const US_STOCKS = [
  { name: "Apple Inc.", symbol: "AAPL", sector: "Technology", exchange: "NASDAQ" },
  { name: "Microsoft Corporation", symbol: "MSFT", sector: "Technology", exchange: "NASDAQ" },
  { name: "NVIDIA Corporation", symbol: "NVDA", sector: "Semiconductors", exchange: "NASDAQ" },
  { name: "Alphabet Inc. (Google)", symbol: "GOOGL", sector: "Technology", exchange: "NASDAQ" },
  { name: "Amazon.com Inc.", symbol: "AMZN", sector: "Consumer & Cloud", exchange: "NASDAQ" },
  { name: "Tesla Inc.", symbol: "TSLA", sector: "Automotive & Energy", exchange: "NASDAQ" }
];

export const ALL_STOCKS = [...INDIAN_STOCKS, ...US_STOCKS];

export function getStockInfo(symbol) {
  if (!symbol) return null;
  const match = ALL_STOCKS.find((s) => s.symbol.toUpperCase() === symbol.toUpperCase());
  if (match) return match;
  return {
    name: symbol,
    symbol: symbol.toUpperCase(),
    sector: "Custom Asset",
    exchange: symbol.endsWith(".NS") ? "NSE" : symbol.endsWith(".BO") ? "BSE" : "US Market"
  };
}

export function isIndianStock(symbol) {
  if (!symbol) return false;
  const s = symbol.toUpperCase();
  return s.endsWith(".NS") || s.endsWith(".BO");
}
