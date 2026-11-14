import React, { useState } from "react";

export default function KernelHeatmap({ matrix }) {
  const [hoveredCell, setHoveredCell] = useState(null);

  if (!matrix || !matrix.length) return null;

  // Map similarity from 0 to 1 to HSL color
  const getCellColor = (value) => {
    const clamped = Math.max(0, Math.min(1, value));
    const lightness = 12 + clamped * 52; // 12% to 64%
    const hue = 250 - clamped * 65; // 250 (indigo) to 185 (cyan)
    return `hsl(${hue}, 82%, ${lightness}%)`;
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-lg">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 mb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <span>🧬 Quantum Similarity Heatmap (First 30 Days)</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            This grid shows how similar any two trading days look to our 4 quantum qubits. Each square compares Day <em>i</em> with Day <em>j</em>.
          </p>
        </div>

        <div className="text-xs bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2 font-mono text-slate-300 shrink-0">
          {hoveredCell ? (
            <span>
              Day {hoveredCell.r + 1} vs Day {hoveredCell.c + 1} Similarity:{" "}
              <strong className="text-cyan-300 font-bold">
                {(hoveredCell.val * 100).toFixed(1)}%
              </strong>
            </span>
          ) : (
            <span className="text-slate-400">👆 Hover any box to check similarity</span>
          )}
        </div>
      </div>

      <div className="overflow-x-auto pb-2">
        <div className="min-w-[420px] max-w-[600px] mx-auto">
          <div
            className="grid gap-[2px] bg-slate-950 p-2 rounded-xl border border-slate-800"
            style={{
              gridTemplateColumns: `repeat(${matrix.length}, minmax(0, 1fr))`
            }}
          >
            {matrix.map((row, rIdx) =>
              row.map((val, cIdx) => (
                <div
                  key={`${rIdx}-${cIdx}`}
                  onMouseEnter={() => setHoveredCell({ r: rIdx, c: cIdx, val })}
                  onMouseLeave={() => setHoveredCell(null)}
                  style={{ backgroundColor: getCellColor(val) }}
                  className="aspect-square rounded-[2px] cursor-crosshair transition-transform duration-75 hover:scale-125 hover:z-10 hover:ring-2 hover:ring-white"
                  title={`Day ${rIdx + 1} vs Day ${cIdx + 1}: ${(val * 100).toFixed(1)}% match`}
                />
              ))
            )}
          </div>

          {/* Colorbar legend */}
          <div className="mt-3.5 flex items-center justify-between text-[11px] text-slate-400 px-1">
            <span>0% (Completely Different Days)</span>
            <div
              className="h-2.5 flex-1 mx-3 rounded-full shadow-inner"
              style={{
                background:
                  "linear-gradient(90deg, hsl(250, 82%, 12%) 0%, hsl(217, 82%, 38%) 50%, hsl(185, 82%, 64%) 100%)"
              }}
            />
            <span>100% (Identical Days)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
