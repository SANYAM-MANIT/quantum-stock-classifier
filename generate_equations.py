import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

output_dir = "/Users/sanyamjain/Downloads/quantum-stock-classifier/eq_images"
os.makedirs(output_dir, exist_ok=True)

equations = [
    {
        "filename": "eq_primal_svm.png",
        "formula": r"$\min_{\mathbf{w}, b, \mathbf{\xi}} \; \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^M \xi_i \quad \mathrm{s.t.} \quad y_i(\mathbf{w}\cdot\mathbf{x}_i + b) \geq 1 - \xi_i, \; \xi_i \geq 0$",
        "color": "#38bdf8",
        "border": "#38bdf8",
        "size": (8.6, 1.4),
        "fontsize": 14.5
    },
    {
        "filename": "eq_dual_svm.png",
        "formula": r"$\max_{\mathbf{\alpha}} \; \sum_{i=1}^M \alpha_i - \frac{1}{2}\sum_{i,j=1}^M \alpha_i \alpha_j y_i y_j (\mathbf{x}_i \cdot \mathbf{x}_j) \quad \mathrm{s.t.} \quad 0 \leq \alpha_i \leq C, \; \sum_{i=1}^M \alpha_i y_i = 0$",
        "color": "#818cf8",
        "border": "#818cf8",
        "size": (8.8, 1.4),
        "fontsize": 14
    },
    {
        "filename": "eq_decision.png",
        "formula": r"$f(\mathbf{x}) = \mathrm{sign}\left( \sum_{i=1}^M \alpha_i y_i (\mathbf{x}_i \cdot \mathbf{x}) + b \right)$",
        "color": "#34d399",
        "border": "#34d399",
        "size": (6.5, 1.2),
        "fontsize": 15
    },
    {
        "filename": "eq_kernel_trick.png",
        "formula": r"$K(\mathbf{x}, \mathbf{x}^\prime) = \langle \phi(\mathbf{x}), \phi(\mathbf{x}^\prime) \rangle_{\mathcal{H}}, \quad K_{\mathrm{RBF}}(\mathbf{x}, \mathbf{x}^\prime) = \exp(-\gamma \|\mathbf{x} - \mathbf{x}^\prime\|^2)$",
        "color": "#fbbf24",
        "border": "#fbbf24",
        "size": (8.6, 1.4),
        "fontsize": 14.5
    },
    {
        "filename": "eq_quantum_state.png",
        "formula": r"$|\psi(\mathbf{x})\rangle = U_{\Phi}(\mathbf{x}) |0\rangle^{\otimes n} \in \mathcal{H} \cong \mathbb{C}^{2^n} \quad (\mathrm{Hilbert \; Space \; Dimension} = 2^n)$",
        "color": "#38bdf8",
        "border": "#38bdf8",
        "size": (8.4, 1.3),
        "fontsize": 14.5
    },
    {
        "filename": "eq_quantum_kernel.png",
        "formula": r"$K(\mathbf{x}_i, \mathbf{x}_j) = |\langle \psi(\mathbf{x}_i) | \psi(\mathbf{x}_j) \rangle|^2 = |\langle 0^{\otimes n}| U_{\Phi}^\dagger(\mathbf{x}_j) U_{\Phi}(\mathbf{x}_i) |0^{\otimes n}\rangle|^2$",
        "color": "#34d399",
        "border": "#34d399",
        "size": (8.8, 1.4),
        "fontsize": 14.5
    },
    {
        "filename": "eq_hhl_system.png",
        "formula": r"$\mathbf{A}_{\mathrm{LS}} \cdot [b, \; \mathbf{\alpha}]^T = [0, \; \mathbf{y}]^T \quad \Longrightarrow \quad A\mathbf{x} = \mathbf{b} \quad \mathrm{via} \; \mathrm{HHL} \; O(\log N)$",
        "color": "#fb7185",
        "border": "#fb7185",
        "size": (8.4, 1.3),
        "fontsize": 14.5
    },
    {
        "filename": "eq_circuit_transition.png",
        "formula": r"$P(|0000\rangle) = |\langle 0000 | U_{\Phi}^\dagger(\mathbf{x}_j) U_{\Phi}(\mathbf{x}_i) | 0000 \rangle|^2 = K(\mathbf{x}_i, \mathbf{x}_j)$",
        "color": "#38bdf8",
        "border": "#38bdf8",
        "size": (8.2, 1.3),
        "fontsize": 14.5
    },
    {
        "filename": "eq_scaling.png",
        "formula": r"$\mathbf{x} = [x_{\mathrm{RSI}}, \; x_{\mathrm{MACD}}, \; x_{\mathrm{MARatio}}, \; x_{\mathrm{Vol}}]^T \in [0, \pi]^4 \quad (\mathrm{Prevents} \; 2\pi \; \mathrm{Phase \; Wrapping})$",
        "color": "#34d399",
        "border": "#34d399",
        "size": (8.8, 1.3),
        "fontsize": 14
    },
    {
        "filename": "eq_zz_feature_map.png",
        "formula": r"$U_{\Phi}(\mathbf{x}) = \left[ U_Z(\mathbf{x}) H^{\otimes 4} \right]^2 \quad \mathrm{with} \quad \phi_{ij}(\mathbf{x}) = 2(\pi - x_i)(\pi - x_j)$",
        "color": "#818cf8",
        "border": "#818cf8",
        "size": (8.4, 1.3),
        "fontsize": 14.5
    },
    {
        "filename": "eq_vectorized_gram.png",
        "formula": r"$K_{ij} = |\mathbf{\Psi}_i^\dagger \mathbf{\Psi}_j|^2 \quad \Longrightarrow \quad K = |\mathbf{\Psi} \mathbf{\Psi}^\dagger|^{\odot 2} \in \mathbb{R}^{M \times M} \quad (700\times \; \mathrm{Speedup})$",
        "color": "#38bdf8",
        "border": "#38bdf8",
        "size": (8.6, 1.3),
        "fontsize": 14.5
    }
]

bg_color = "#0a1124"

for eq in equations:
    w, h = eq["size"]
    fig = plt.figure(figsize=(w, h), dpi=260)
    fig.patch.set_facecolor(bg_color)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_facecolor(bg_color)
    
    # Rounded badge box
    box = FancyBboxPatch((0.015, 0.08), 0.97, 0.84, transform=ax.transAxes,
                         boxstyle="round,pad=0.03,rounding_size=0.06",
                         facecolor="#101935", edgecolor=eq["border"], linewidth=1.8)
    ax.add_patch(box)
    
    ax.text(0.5, 0.5, eq["formula"], color=eq["color"], fontsize=eq["fontsize"],
            ha="center", va="center", transform=ax.transAxes)
    
    fpath = os.path.join(output_dir, eq["filename"])
    fig.savefig(fpath, facecolor=bg_color, edgecolor="none", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f"Generated: {eq['filename']}")

print("All 11 equation images created successfully!")
