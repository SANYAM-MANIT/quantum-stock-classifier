import React from "react";

function ScorecardTable({ title, modelType, matrix, accentColor }) {
  // matrix is [[TN, FP], [FN, TP]]
  const tn = matrix?.[0]?.[0] ?? 0;
  const fp = matrix?.[0]?.[1] ?? 0;
  const fn = matrix?.[1]?.[0] ?? 0;
  const tp = matrix?.[1]?.[1] ?? 0;

  const totalCorrect = tn + tp;
  const totalWrong = fp + fn;

  return (
    <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 flex-1 flex flex-col justify-between">
      <div className="mb-3">
        <div className="flex items-center justify-between">
          <h4 className={`text-sm font-bold ${accentColor}`}>{title}</h4>
          <span className="text-[11px] text-slate-400 font-mono">
            {totalCorrect}/100 Correct
          </span>
        </div>
        <p className="text-[11px] text-slate-400">{modelType}</p>
      </div>

      <div className="grid grid-cols-3 gap-2 text-center text-xs">
        <div className="flex items-center justify-center text-slate-500 font-medium text-[11px]">
          Actual \ Predicted
        </div>
        <div className="bg-slate-900 py-1 px-2 rounded font-semibold text-slate-300 border border-slate-800 text-[11px]">
          Guessed DOWN
        </div>
        <div className="bg-slate-900 py-1 px-2 rounded font-semibold text-slate-300 border border-slate-800 text-[11px]">
          Guessed UP
        </div>

        <div className="bg-slate-900 py-2 px-2 rounded font-semibold text-slate-300 border border-slate-800 flex items-center justify-center text-[11px]">
          Actually Went DOWN
        </div>
        <div className="bg-emerald-950/40 border border-emerald-500/30 rounded-lg py-2.5 flex flex-col items-center justify-center">
          <span className="text-lg font-black text-emerald-300 font-mono">{tn}</span>
          <span className="text-[10px] text-emerald-400/90 font-medium">✅ Correct</span>
        </div>
        <div className="bg-rose-950/40 border border-rose-500/30 rounded-lg py-2.5 flex flex-col items-center justify-center">
          <span className="text-lg font-black text-rose-300 font-mono">{fp}</span>
          <span className="text-[10px] text-rose-400/90 font-medium">❌ Mistake</span>
        </div>

        <div className="bg-slate-900 py-2 px-2 rounded font-semibold text-slate-300 border border-slate-800 flex items-center justify-center text-[11px]">
          Actually Went UP
        </div>
        <div className="bg-rose-950/40 border border-rose-500/30 rounded-lg py-2.5 flex flex-col items-center justify-center">
          <span className="text-lg font-black text-rose-300 font-mono">{fn}</span>
          <span className="text-[10px] text-rose-400/90 font-medium">❌ Mistake</span>
        </div>
        <div className="bg-emerald-950/40 border border-emerald-500/30 rounded-lg py-2.5 flex flex-col items-center justify-center">
          <span className="text-lg font-black text-emerald-300 font-mono">{tp}</span>
          <span className="text-[10px] text-emerald-400/90 font-medium">✅ Correct</span>
        </div>
      </div>

      <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
        <span>Green = Got it right</span>
        <span>Red = Got it wrong</span>
      </div>
    </div>
  );
}

export default function ConfusionMatrices({ qsvmMatrix, svmMatrix }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
      <div>
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <span>🎯 Model Scorecards (Confusion Matrix)</span>
        </h3>
        <p className="text-xs text-slate-400 mt-1 mb-3">
          A clear breakdown of how many times each model guessed right vs. wrong out of the 100 test days.
        </p>
      </div>

      <div className="flex flex-col sm:flex-row gap-4">
        <ScorecardTable
          title="Quantum Model"
          modelType="Quantum SVM (4-Qubit Circuit)"
          matrix={qsvmMatrix}
          accentColor="text-indigo-400"
        />
        <ScorecardTable
          title="Classical Model"
          modelType="Standard Computer SVM (RBF)"
          matrix={svmMatrix}
          accentColor="text-emerald-400"
        />
      </div>
    </div>
  );
}
