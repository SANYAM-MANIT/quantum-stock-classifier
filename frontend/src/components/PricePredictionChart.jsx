import React, { useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function PricePredictionChart({
  recentPrices,
  ticker,
  fullName,
  isIndian = false
}) {
  const [selectedModel, setSelectedModel] = useState("qsvm");
  const currencySymbol = isIndian ? "₹" : "$";

  // Dot showing green for correct guess, red for wrong guess
  const renderPredictionDot = (props) => {
    const { cx, cy, payload } = props;
    if (cx === undefined || cy === undefined || !payload) return null;

    const isCorrect =
      selectedModel === "qsvm" ? payload.qsvm_correct : payload.svm_correct;

    return (
      <circle
        key={`dot-${payload.date}`}
        cx={cx}
        cy={cy}
        r={4}
        fill={isCorrect ? "#10b981" : "#f43f5e"}
        stroke="#0f172a"
        strokeWidth={1.5}
      />
    );
  };

  const CustomTooltip = ({ active, payload }) => {
    if (!active || !payload || !payload.length) return null;
    const item = payload[0].payload;
    const pred = selectedModel === "qsvm" ? item.qsvm_pred : item.svm_pred;
    const correct = selectedModel === "qsvm" ? item.qsvm_correct : item.svm_correct;

    return (
      <div className="bg-slate-950 border border-slate-700 rounded-xl p-3 shadow-2xl text-xs space-y-1.5 min-w-[200px]">
        <div className="font-bold text-slate-200 border-b border-slate-800 pb-1 flex justify-between">
          <span>{item.date}</span>
          <span className="font-mono text-slate-400">{ticker}</span>
        </div>
        <div className="text-slate-300">
          Closing Price:{" "}
          <strong className="font-mono text-white text-sm">
            {currencySymbol}
            {item.close.toFixed(2)}
          </strong>
        </div>
        <div className="text-slate-300">
          Next Day Actually Went:{" "}
          <span
            className={
              item.actual_label === 1
                ? "text-emerald-400 font-bold"
                : "text-rose-400 font-bold"
            }
          >
            {item.actual_label === 1 ? "UP 📈" : "DOWN 📉"}
          </span>
        </div>
        <div className="text-slate-300">
          {selectedModel === "qsvm" ? "Quantum Model" : "Classical Model"} Predicted:{" "}
          <span
            className={
              pred === 1
                ? "text-emerald-400 font-bold"
                : "text-rose-400 font-bold"
            }
          >
            {pred === 1 ? "UP 📈" : "DOWN 📉"}
          </span>
        </div>
        <div className="pt-1 border-t border-slate-800">
          <span
            className={`inline-block px-2 py-0.5 rounded text-[11px] font-bold ${
              correct
                ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40"
                : "bg-rose-500/20 text-rose-300 border border-rose-500/40"
            }`}
          >
            {correct ? "✅ Guessed Correctly" : "❌ Guessed Wrong"}
          </span>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <span>📈 Real Daily Closing Prices (Last 100 Test Days)</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            <strong>{fullName || ticker}:</strong>{" "}
            <span className="text-emerald-400 font-bold">🟢 Green Dot</span> = Model guessed right &bull;{" "}
            <span className="text-rose-400 font-bold">🔴 Red Dot</span> = Model made a mistake.
          </p>
        </div>

        <div className="inline-flex rounded-xl bg-slate-950 p-1 border border-slate-800 self-start">
          <button
            type="button"
            onClick={() => setSelectedModel("qsvm")}
            className={`px-3 py-1.5 text-xs font-bold rounded-lg transition ${
              selectedModel === "qsvm"
                ? "bg-indigo-600 text-white shadow"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Show Quantum Guesses
          </button>
          <button
            type="button"
            onClick={() => setSelectedModel("svm")}
            className={`px-3 py-1.5 text-xs font-bold rounded-lg transition ${
              selectedModel === "svm"
                ? "bg-emerald-600 text-white shadow"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Show Classical Guesses
          </button>
        </div>
      </div>

      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={recentPrices} margin={{ top: 10, right: 20, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="date"
              tick={{ fill: "#94a3b8", fontSize: 11 }}
              minTickGap={25}
              axisLine={{ stroke: "#334155" }}
            />
            <YAxis
              domain={["auto", "auto"]}
              tickFormatter={(v) => `${currencySymbol}${v}`}
              tick={{ fill: "#94a3b8", fontSize: 11 }}
              axisLine={{ stroke: "#334155" }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="close"
              stroke="#94a3b8"
              strokeWidth={1.8}
              dot={renderPredictionDot}
              activeDot={{ r: 6, stroke: "#f8fafc", strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
