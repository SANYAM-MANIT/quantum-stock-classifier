import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ReferenceLine
} from "recharts";

export default function AccuracyChart({ qsvmAcc, svmAcc, majorityBaseline }) {
  const data = [
    {
      name: "Quantum Model",
      accuracy: Number((qsvmAcc * 100).toFixed(1)),
      color: "#6366f1"
    },
    {
      name: "Classical Model",
      accuracy: Number((svmAcc * 100).toFixed(1)),
      color: "#10b981"
    },
    {
      name: "Blind Guessing",
      accuracy: Number((majorityBaseline * 100).toFixed(1)),
      color: "#f59e0b"
    }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
      <div>
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <span>📊 Accuracy Comparison (%)</span>
        </h3>
        <p className="text-xs text-slate-400 mt-1 mb-3">
          How often each method guessed the right tomorrow-direction on the 100 test days. Notice how close everything is to 50%!
        </p>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 15, right: 20, left: -5, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="name"
              tick={{ fill: "#94a3b8", fontSize: 12, fontWeight: 600 }}
              axisLine={{ stroke: "#334155" }}
            />
            <YAxis
              domain={[0, 100]}
              tickFormatter={(val) => `${val}%`}
              tick={{ fill: "#94a3b8", fontSize: 11 }}
              axisLine={{ stroke: "#334155" }}
            />
            <Tooltip
              cursor={{ fill: "rgba(148, 163, 184, 0.08)" }}
              contentStyle={{
                backgroundColor: "#0f172a",
                borderColor: "#334155",
                borderRadius: "0.5rem",
                color: "#f8fafc",
                fontSize: "12px"
              }}
              formatter={(value) => [`${value}%`, "Accuracy"]}
            />
            <ReferenceLine
              y={50}
              stroke="#64748b"
              strokeDasharray="4 4"
              label={{
                value: "50% (Random Coin Toss)",
                position: "insideTopRight",
                fill: "#94a3b8",
                fontSize: 11
              }}
            />
            <Bar dataKey="accuracy" radius={[6, 6, 0, 0]} maxBarSize={60}>
              {data.map((entry, idx) => (
                <Cell key={`cell-${idx}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
