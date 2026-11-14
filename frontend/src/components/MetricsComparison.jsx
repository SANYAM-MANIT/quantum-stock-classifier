import React from "react";

function MetricRow({ label, qValue, cValue, unit = "%", higherIsBetter = true }) {
  const qNum = typeof qValue === "number" ? qValue : parseFloat(qValue);
  const cNum = typeof cValue === "number" ? cValue : parseFloat(cValue);

  const diff = (qNum - cNum).toFixed(1);
  const isQBetter = qNum > cNum;
  const isCBetter = cNum > qNum;
  const isEqual = qNum === cNum;

  return (
    <tr className="border-b border-slate-800/60 hover:bg-slate-900/40 transition">
      <td className="py-2.5 px-3 text-xs font-medium text-slate-300">
        {label}
      </td>
      <td className="py-2.5 px-3 text-xs font-mono font-bold text-indigo-300 text-center">
        {qValue}{unit}
      </td>
      <td className="py-2.5 px-3 text-xs font-mono font-bold text-emerald-300 text-center">
        {cValue}{unit}
      </td>
      <td className="py-2.5 px-3 text-xs text-center">
        {isEqual ? (
          <span className="text-slate-400 font-mono text-[11px]">Tie</span>
        ) : isQBetter ? (
          <span className="text-indigo-400 font-semibold text-[11px]">
            Quantum (+{diff}{unit})
          </span>
        ) : (
          <span className="text-emerald-400 font-semibold text-[11px]">
            Classical (+{Math.abs(diff)}{unit})
          </span>
        )}
      </td>
    </tr>
  );
}

export default function MetricsComparison({ qsvm, svm, majorityBaseline, classBalance }) {
  const formatPct = (val) => (val * 100).toFixed(1);

  const qAcc = qsvm.accuracy * 100;
  const cAcc = svm.accuracy * 100;
  const accDiff = Math.abs(qAcc - cAcc).toFixed(1);

  let winnerText = "Both models achieved identical accuracy";
  let winnerBadgeColor = "bg-slate-800 text-slate-300 border-slate-700";
  if (qAcc > cAcc) {
    winnerText = `Quantum Model won by +${accDiff}% on this stock`;
    winnerBadgeColor = "bg-indigo-950/70 text-indigo-300 border-indigo-700/50";
  } else if (cAcc > qAcc) {
    winnerText = `Classical Model won by +${accDiff}% on this stock`;
    winnerBadgeColor = "bg-emerald-950/70 text-emerald-300 border-emerald-700/50";
  }

  return (
    <div className="space-y-4">
      {/* Showdown Result Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-5 shadow-lg flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${winnerBadgeColor}`}>
              {winnerText}
            </span>
            <span className="text-xs text-slate-400">
              Tested over the last 100 real trading days
            </span>
          </div>
          <p className="text-xs text-slate-300 mt-2 max-w-2xl leading-relaxed">
            <strong>Key Finding:</strong> Market moves contain substantial day-to-day noise. Classical RBF kernel handles smooth decision boundaries with regularized margins, while the 4-qubit quantum kernel explores 16-dimensional Hilbert space interactions. Both stay close to the baseline coin toss.
          </p>
        </div>

        <div className="flex items-center gap-4 bg-slate-950/80 border border-slate-800 px-4 py-2.5 rounded-xl self-start md:self-auto shrink-0">
          <div className="text-center">
            <span className="text-[10px] text-slate-400 uppercase tracking-wide block">Quantum</span>
            <span className="text-lg font-mono font-black text-indigo-400">
              {formatPct(qsvm.accuracy)}%
            </span>
          </div>
          <div className="text-slate-600 font-bold text-sm">vs</div>
          <div className="text-center">
            <span className="text-[10px] text-slate-400 uppercase tracking-wide block">Classical</span>
            <span className="text-lg font-mono font-black text-emerald-400">
              {formatPct(svm.accuracy)}%
            </span>
          </div>
          <div className="border-l border-slate-800 pl-3 text-center">
            <span className="text-[10px] text-slate-400 uppercase tracking-wide block">Baseline</span>
            <span className="text-lg font-mono font-black text-amber-400">
              {formatPct(majorityBaseline)}%
            </span>
          </div>
        </div>
      </div>

      {/* Side-by-Side Comparison Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-lg">
        <div className="px-5 py-3.5 border-b border-slate-800 flex items-center justify-between">
          <h3 className="text-sm font-bold text-white">
            Performance Metrics Comparison Table
          </h3>
          <span className="text-xs text-slate-400 font-mono">
            Out-of-sample (100 Days)
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-slate-950/60 text-[11px] font-semibold text-slate-400 uppercase tracking-wider border-b border-slate-800">
                <th className="py-2.5 px-3">Metric</th>
                <th className="py-2.5 px-3 text-center text-indigo-300">Quantum SVM (QSVC)</th>
                <th className="py-2.5 px-3 text-center text-emerald-300">Classical SVM (RBF)</th>
                <th className="py-2.5 px-3 text-center">Advantage</th>
              </tr>
            </thead>
            <tbody>
              <MetricRow
                label="Accuracy (Overall Correct Predictions)"
                qValue={formatPct(qsvm.accuracy)}
                cValue={formatPct(svm.accuracy)}
              />
              <MetricRow
                label="Precision (Accuracy When Predicting UP)"
                qValue={formatPct(qsvm.precision)}
                cValue={formatPct(svm.precision)}
              />
              <MetricRow
                label="Recall (Percentage of Real UP Days Caught)"
                qValue={formatPct(qsvm.recall)}
                cValue={formatPct(svm.recall)}
              />
              <MetricRow
                label="F1 Score (Balanced Quality Score)"
                qValue={formatPct(qsvm.f1)}
                cValue={formatPct(svm.f1)}
              />
              <MetricRow
                label="Execution / Training Time"
                qValue={qsvm.training_time.toFixed(2)}
                cValue={svm.training_time.toFixed(2)}
                unit="s"
                higherIsBetter={false}
              />
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
