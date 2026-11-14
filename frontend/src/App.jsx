import React, { useState, useMemo } from "react";
import { runStockClassifier } from "./api.js";
import {
  INDIAN_STOCKS,
  US_STOCKS,
  getStockInfo,
  isIndianStock
} from "./stocks.js";
import MetricsComparison from "./components/MetricsComparison.jsx";
import AccuracyChart from "./components/AccuracyChart.jsx";
import ConfusionMatrices from "./components/ConfusionMatrices.jsx";
import PricePredictionChart from "./components/PricePredictionChart.jsx";
import KernelHeatmap from "./components/KernelHeatmap.jsx";
import ProjectMethodology from "./components/ProjectMethodology.jsx";

export default function App() {
  const [marketTab, setMarketTab] = useState("india"); // "india" | "us"
  const [sectorFilter, setSectorFilter] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedSymbol, setSelectedSymbol] = useState("RELIANCE.NS");
  const [customInput, setCustomInput] = useState("");
  const [activeViewTab, setActiveViewTab] = useState("chart"); // "chart" | "matrices" | "heatmap" | "methodology"
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  // Filter stocks based on market tab, sector, and search query
  const availableStocks = marketTab === "india" ? INDIAN_STOCKS : US_STOCKS;

  const sectors = useMemo(() => {
    const s = new Set(availableStocks.map((item) => item.sector));
    return ["All", ...Array.from(s)];
  }, [availableStocks]);

  const filteredStocks = useMemo(() => {
    return availableStocks.filter((stock) => {
      const matchesSector = sectorFilter === "All" || stock.sector === sectorFilter;
      const q = searchQuery.toLowerCase().trim();
      const matchesSearch =
        !q ||
        stock.name.toLowerCase().includes(q) ||
        stock.symbol.toLowerCase().includes(q) ||
        stock.sector.toLowerCase().includes(q);
      return matchesSector && matchesSearch;
    });
  }, [availableStocks, sectorFilter, searchQuery]);

  const handleRun = async (symbolToRun) => {
    const sym = (symbolToRun || customInput || selectedSymbol).trim().toUpperCase();
    if (!sym) {
      setError("Please choose a company or enter a valid ticker symbol.");
      return;
    }

    setSelectedSymbol(sym);
    setError("");
    setLoading(true);

    try {
      const data = await runStockClassifier(sym);
      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to fetch data or compute models. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const currentInfo = getStockInfo(result?.ticker || selectedSymbol);
  const isIndian = isIndianStock(result?.ticker || selectedSymbol);
  const currencySymbol = isIndian ? "₹" : "$";
  const latestPrice = result?.recent_prices?.[result.recent_prices.length - 1]?.close;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col antialiased">
      {/* College Project Top Nav */}
      <header className="border-b border-slate-800/80 bg-slate-900/70 backdrop-blur sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-cyan-500 flex items-center justify-center font-black text-white text-base shadow-md">
              Q
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base sm:text-lg font-extrabold text-white tracking-tight">
                  QuantumTrade Lab
                </h1>
                <span className="text-[11px] font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-800/50 px-2 py-0.5 rounded-md">
                  v2.0 Local Statevector
                </span>
              </div>
              <p className="text-[11px] text-slate-400">
                Department of Computer Science & Engineering &bull; B.Tech Capstone Project
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 self-start md:self-auto text-xs text-slate-400">
            <div className="flex items-center gap-1.5 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>Flask API: <strong>localhost:5001</strong></span>
            </div>
            <div className="hidden sm:block text-[11px] text-slate-500 font-mono">
              Qiskit 1.4 &bull; Scikit-Learn
            </div>
          </div>
        </div>
      </header>

      {/* Main App Container */}
      <main className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 space-y-6">
        {/* Project Abstract & Academic Context */}
        <section className="bg-slate-900/60 border border-slate-800/90 rounded-2xl p-4 sm:p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <h2 className="text-sm font-bold text-white uppercase tracking-wider text-slate-300">
              Project Overview: Quantum SVM vs Classical RBF SVM
            </h2>
            <p className="text-xs text-slate-300 max-w-3xl leading-relaxed">
              We benchmark a <strong>4-Qubit Quantum Support Vector Machine (QSVM)</strong> utilizing an entangled <code>ZZFeatureMap</code> against a standard <strong>Classical RBF-Kernel SVM</strong>. The objective is predicting whether an equity closes <strong>UP (1)</strong> or <strong>DOWN (0)</strong> the next trading day using 5 years of Yahoo Finance market data across 250 training days and 100 out-of-sample test days.
            </p>
          </div>
          <div className="bg-amber-950/30 border border-amber-600/30 rounded-xl p-3 shrink-0 text-[11px] text-amber-200/90 max-w-xs">
            <strong>Honest Student Note:</strong> Stock markets have low signal-to-noise ratios. Real prediction accuracy typically hovers near 50-55%. This demo assesses quantum feature maps on financial datasets.
          </div>
        </section>

        {/* Stock Selector Workspace */}
        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
            <div>
              <h3 className="text-sm font-bold text-white">
                Select Company for Analysis
              </h3>
              <p className="text-xs text-slate-400">
                Pick a company from the Indian National Stock Exchange (NSE) or US Equities, or enter a custom symbol.
              </p>
            </div>

            {/* Market Switcher */}
            <div className="flex items-center gap-1.5 bg-slate-950 p-1 rounded-xl border border-slate-800 self-start sm:self-auto">
              <button
                type="button"
                onClick={() => {
                  setMarketTab("india");
                  setSectorFilter("All");
                  setSelectedSymbol(INDIAN_STOCKS[0].symbol);
                }}
                className={`px-3 py-1.5 text-xs font-bold rounded-lg transition ${
                  marketTab === "india"
                    ? "bg-indigo-600 text-white shadow"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                🇮🇳 Indian Equities (NSE)
              </button>
              <button
                type="button"
                onClick={() => {
                  setMarketTab("us");
                  setSectorFilter("All");
                  setSelectedSymbol(US_STOCKS[0].symbol);
                }}
                className={`px-3 py-1.5 text-xs font-bold rounded-lg transition ${
                  marketTab === "us"
                    ? "bg-indigo-600 text-white shadow"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                🇺🇸 US Equities (NASDAQ/NYSE)
              </button>
            </div>
          </div>

          {/* Search & Sector Filters */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
            {/* Sector Pills */}
            <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 text-xs">
              <span className="text-slate-500 font-medium text-[11px] mr-1">Sector:</span>
              {sectors.map((sec) => (
                <button
                  key={sec}
                  type="button"
                  onClick={() => setSectorFilter(sec)}
                  className={`px-2.5 py-1 rounded-lg font-medium whitespace-nowrap transition text-xs ${
                    sectorFilter === sec
                      ? "bg-slate-800 text-white border border-slate-700"
                      : "text-slate-400 hover:text-slate-200 bg-slate-950/60"
                  }`}
                >
                  {sec}
                </button>
              ))}
            </div>

            {/* Quick Search */}
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search company or ticker..."
                className="w-full md:w-64 bg-slate-950 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white placeholder:text-slate-500 focus:outline-none focus:border-indigo-500"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery("")}
                  className="absolute right-2.5 top-1.5 text-slate-400 hover:text-white text-xs"
                >
                  &times;
                </button>
              )}
            </div>
          </div>

          {/* Companies Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5 max-h-56 overflow-y-auto pr-1">
            {filteredStocks.map((stock) => {
              const isSelected = selectedSymbol === stock.symbol;
              return (
                <button
                  key={stock.symbol}
                  type="button"
                  disabled={loading}
                  onClick={() => {
                    setSelectedSymbol(stock.symbol);
                    handleRun(stock.symbol);
                  }}
                  className={`text-left p-3 rounded-xl border transition flex flex-col justify-between gap-1.5 cursor-pointer disabled:opacity-50 ${
                    isSelected
                      ? "bg-indigo-600/20 border-indigo-500 text-white ring-1 ring-indigo-500 shadow-md"
                      : "bg-slate-950/80 border-slate-800/90 text-slate-300 hover:border-slate-700 hover:bg-slate-900/60"
                  }`}
                >
                  <div className="font-bold text-xs leading-snug line-clamp-1">
                    {stock.name}
                  </div>
                  <div className="flex items-center justify-between text-[11px] text-slate-400">
                    <span className="font-mono text-indigo-300 font-semibold">{stock.symbol}</span>
                    <span className="text-[10px] bg-slate-900 px-1.5 py-0.5 rounded text-slate-400 border border-slate-800">
                      {stock.exchange} &bull; {stock.sector}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>

          {/* Custom Search & Run Bar */}
          <div className="pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2">
              <span className="text-slate-400">Custom Ticker:</span>
              <input
                type="text"
                value={customInput}
                onChange={(e) => setCustomInput(e.target.value.toUpperCase())}
                placeholder="e.g. INFY.NS, MSFT"
                disabled={loading}
                maxLength={20}
                className="w-36 sm:w-44 bg-slate-950 border border-slate-700 focus:border-indigo-500 focus:outline-none rounded-lg px-2.5 py-1.5 font-mono text-white text-xs placeholder:text-slate-600"
              />
              <button
                type="button"
                disabled={loading || !customInput.trim()}
                onClick={() => handleRun(customInput)}
                className="bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-white font-semibold px-3 py-1.5 rounded-lg border border-slate-700 transition"
              >
                Load Custom
              </button>
            </div>

            <button
              type="button"
              disabled={loading}
              onClick={() => handleRun(selectedSymbol)}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-800/60 text-white font-bold text-xs sm:text-sm px-5 py-2 rounded-xl shadow transition flex items-center gap-2 cursor-pointer disabled:cursor-not-allowed ml-auto"
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24" fill="none">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                  </svg>
                  <span>Computing Models...</span>
                </>
              ) : (
                <span>Run Prediction Benchmark &rarr;</span>
              )}
            </button>
          </div>
        </section>

        {/* Loading State */}
        {loading && (
          <div className="bg-slate-900 border border-indigo-500/30 rounded-2xl p-8 text-center space-y-3 shadow-xl">
            <div className="inline-flex p-3 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
              <svg className="animate-spin h-8 w-8" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
              </svg>
            </div>
            <div>
              <h3 className="text-base font-bold text-white">
                Computing Quantum & Classical Kernels...
              </h3>
              <p className="text-xs text-slate-400 max-w-lg mx-auto mt-1">
                Executing 4-qubit statevector projections and classical RBF support vector optimization for{" "}
                <strong>{currentInfo?.name || selectedSymbol}</strong>.
              </p>
            </div>
          </div>
        )}

        {/* Error Notice */}
        {!loading && error && (
          <div className="bg-rose-950/40 border border-rose-500/40 rounded-2xl p-4 flex items-start gap-3">
            <span className="text-rose-400 font-bold text-base leading-none">&times;</span>
            <div>
              <h4 className="text-xs sm:text-sm font-bold text-rose-200">
                Error Loading Stock
              </h4>
              <p className="text-xs text-rose-300/90 mt-0.5">{error}</p>
            </div>
          </div>
        )}

        {/* Results Workspace */}
        {!loading && result && (
          <section className="space-y-6">
            {/* Active Company Banner */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono font-bold text-cyan-400 bg-cyan-950/60 border border-cyan-800/40 px-2 py-0.5 rounded">
                    {result.ticker}
                  </span>
                  <span className="text-xs text-slate-400">
                    {currentInfo?.exchange} &bull; {currentInfo?.sector}
                  </span>
                </div>
                <h2 className="text-xl sm:text-2xl font-black text-white mt-1">
                  {currentInfo?.name || result.ticker}
                </h2>
                {latestPrice && (
                  <div className="text-xs text-slate-300 mt-1 flex items-center gap-2">
                    <span>Latest Observed Close:</span>
                    <strong className="text-white font-mono text-sm">
                      {currencySymbol}{latestPrice.toFixed(2)}
                    </strong>
                  </div>
                )}
              </div>

              <div className="flex flex-wrap items-center gap-2 text-xs">
                <div className="bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-center">
                  <span className="text-[10px] text-slate-500 uppercase block">Training Sample</span>
                  <strong className="text-slate-200">250 Days</strong>
                </div>
                <div className="bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 text-center">
                  <span className="text-[10px] text-slate-500 uppercase block">Testing Sample</span>
                  <strong className="text-slate-200">100 Days</strong>
                </div>
                {result.cached && (
                  <span className="text-[11px] text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-1 rounded-lg">
                    Instant Cached Result
                  </span>
                )}
              </div>
            </div>

            {/* Metrics & Head-to-Head Showdown */}
            <MetricsComparison
              qsvm={result.qsvm}
              svm={result.svm}
              majorityBaseline={result.majority_baseline}
              classBalance={result.class_balance}
            />

            {/* Interactive Tabs for Visualizations */}
            <div className="space-y-4">
              <div className="flex items-center gap-2 border-b border-slate-800 pb-2 overflow-x-auto text-xs font-bold">
                <button
                  type="button"
                  onClick={() => setActiveViewTab("chart")}
                  className={`px-3.5 py-2 rounded-xl transition whitespace-nowrap ${
                    activeViewTab === "chart"
                      ? "bg-slate-800 text-white border border-slate-700 shadow"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Daily Prices & Prediction Hits
                </button>
                <button
                  type="button"
                  onClick={() => setActiveViewTab("matrices")}
                  className={`px-3.5 py-2 rounded-xl transition whitespace-nowrap ${
                    activeViewTab === "matrices"
                      ? "bg-slate-800 text-white border border-slate-700 shadow"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Scorecards (Confusion Matrix)
                </button>
                <button
                  type="button"
                  onClick={() => setActiveViewTab("heatmap")}
                  className={`px-3.5 py-2 rounded-xl transition whitespace-nowrap ${
                    activeViewTab === "heatmap"
                      ? "bg-slate-800 text-white border border-slate-700 shadow"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  30x30 Quantum Similarity Heatmap
                </button>
                <button
                  type="button"
                  onClick={() => setActiveViewTab("methodology")}
                  className={`px-3.5 py-2 rounded-xl transition whitespace-nowrap ${
                    activeViewTab === "methodology"
                      ? "bg-slate-800 text-white border border-slate-700 shadow"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  Project Methodology & Circuit
                </button>
              </div>

              {/* Tab Contents */}
              {activeViewTab === "chart" && (
                <div className="space-y-5">
                  <PricePredictionChart
                    recentPrices={result.recent_prices}
                    ticker={result.ticker}
                    fullName={currentInfo?.name}
                    isIndian={isIndian}
                  />
                  <AccuracyChart
                    qsvmAcc={result.qsvm.accuracy}
                    svmAcc={result.svm.accuracy}
                    majorityBaseline={result.majority_baseline}
                  />
                </div>
              )}

              {activeViewTab === "matrices" && (
                <div className="space-y-5">
                  <ConfusionMatrices
                    qsvmMatrix={result.qsvm.confusion_matrix}
                    svmMatrix={result.svm.confusion_matrix}
                  />
                  <AccuracyChart
                    qsvmAcc={result.qsvm.accuracy}
                    svmAcc={result.svm.accuracy}
                    majorityBaseline={result.majority_baseline}
                  />
                </div>
              )}

              {activeViewTab === "heatmap" && (
                <KernelHeatmap matrix={result.kernel_matrix_30x30} />
              )}

              {activeViewTab === "methodology" && (
                <ProjectMethodology />
              )}
            </div>
          </section>
        )}
      </main>

      {/* College Project Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-5 text-center text-xs text-slate-500 space-y-1 mt-auto">
        <div>
          <strong>B.Tech Major Capstone Project</strong> &bull; Comparative Quantum Machine Learning on Financial Equities
        </div>
        <div className="text-[11px] text-slate-600">
          Built using Qiskit 1.4 Statevector Simulator, Scikit-learn, and React. Powered by Yahoo Finance OHLCV market feeds.
        </div>
      </footer>
    </div>
  );
}
