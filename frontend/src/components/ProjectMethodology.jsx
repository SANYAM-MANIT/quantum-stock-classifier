import React from "react";

export default function ProjectMethodology() {
  const steps = [
    {
      num: "01",
      title: "Real Market Data Fetch",
      desc: "Downloads 5 years of daily OHLCV (Open, High, Low, Close, Volume) data from Yahoo Finance via the Python API.",
      tag: "yfinance"
    },
    {
      num: "02",
      title: "4 Technical Indicators",
      desc: "Calculates RSI (14-day), MACD Histogram (12/26/9 EMA), 20-day Moving Average Ratio, and Daily Volume % Change.",
      tag: "pandas & numpy"
    },
    {
      num: "03",
      title: "Chronological Split & Scaling",
      desc: "First 250 days for training, last 100 days for testing (no random shuffle to prevent lookahead bias). Scaled to [0, π] so rotation angles don't wrap around 2π.",
      tag: "scikit-learn"
    },
    {
      num: "04",
      title: "4-Qubit ZZFeatureMap",
      desc: "Encodes each 4D feature vector into 4 qubits using Hadamard gates and ZZ entangling gates: (π - x_i)(π - x_j).",
      tag: "Qiskit 1.x"
    },
    {
      num: "05",
      title: "Quantum Kernel & Classification",
      desc: "Computes quantum state fidelities |⟨ψ(x_i)|ψ(x_j)⟩|² to build the kernel matrix and trains a Support Vector Classifier.",
      tag: "QSVC / SVC"
    }
  ];

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 sm:p-6 shadow-lg space-y-5">
      <div>
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <span>Project Architecture & Workflow</span>
        </h3>
        <p className="text-xs text-slate-400 mt-1">
          How our project transforms raw stock prices into quantum states and evaluates predictions.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {steps.map((s) => (
          <div
            key={s.num}
            className="bg-slate-950/70 border border-slate-800/90 rounded-xl p-3.5 flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono font-bold text-indigo-400 bg-indigo-950/60 px-2 py-0.5 rounded border border-indigo-900/50">
                  Step {s.num}
                </span>
                <span className="text-[10px] text-slate-500 font-mono">{s.tag}</span>
              </div>
              <h4 className="text-xs font-bold text-slate-200 mb-1">{s.title}</h4>
              <p className="text-[11px] text-slate-400 leading-relaxed">{s.desc}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-slate-950/50 border border-slate-800/80 rounded-xl p-4 text-xs text-slate-300 space-y-1.5">
        <div className="font-semibold text-slate-200">
          Why scale features to [0, π]?
        </div>
        <p className="text-slate-400 leading-relaxed text-[11px]">
          Quantum rotation gates (like RZ and Phase gates) are naturally periodic with period 2π. If data isn't scaled, extreme values like 0 and 2π would rotate to the exact same quantum state (aliasing). Scaling strictly to [0, π] ensures that smaller numbers and larger numbers always map to distinct, separated points on the Bloch sphere.
        </p>
      </div>
    </div>
  );
}
