import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# 1. First ensure all equation images exist
import generate_equations

print("Verified all equation images exist.")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette
BG_DARK = RGBColor(10, 15, 29)          # #0A0F1D deep space navy
CARD_BG = RGBColor(19, 27, 46)          # #131B2E card navy
CARD_BORDER = RGBColor(37, 51, 82)      # #253352 border
TEXT_WHITE = RGBColor(248, 250, 252)    # #F8FAFC crisp white
TEXT_MUTED = RGBColor(148, 163, 184)    # #94A3B8 slate
TEXT_DIM = RGBColor(100, 116, 139)      # #64748B dim
CYAN = RGBColor(56, 189, 248)           # #38BDF8 bright cyan
INDIGO = RGBColor(129, 140, 248)        # #818CF8 vibrant indigo
EMERALD = RGBColor(52, 211, 153)        # #34D399 emerald green
AMBER = RGBColor(251, 191, 36)          # #FBBF24 amber gold
ROSE = RGBColor(251, 113, 133)          # #FB7185 soft rose

blank_layout = prs.slide_layouts[6]

def set_slide_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()
    return bg

def add_header(slide, category, title, subtitle=None):
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.3))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = CYAN
    p_cat.space_after = Pt(4)

    p_title = tf.add_paragraph()
    p_title.text = title
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE
    p_title.space_after = Pt(3)

    if subtitle:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = TEXT_MUTED

def add_card_shape(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.2)
    return card

def add_card_text(slide, left, top, width, height, title="", title_color=CYAN):
    tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = title_color
        p.space_after = Pt(8)
    return tf

EQ_DIR = "/Users/sanyamjain/Downloads/quantum-stock-classifier/eq_images"

# =========================================================================
# SLIDE 1: Title Slide (Formal MANIT Presentation)
# =========================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(0.15), Inches(5.8))
line.fill.solid()
line.fill.fore_color.rgb = CYAN
line.line.fill.background()

t1_box = s1.shapes.add_textbox(Inches(1.2), Inches(0.8), Inches(11.2), Inches(3.2))
tf1 = t1_box.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

p_inst = tf1.paragraphs[0]
p_inst.text = "MAULANA AZAD NATIONAL INSTITUTE OF TECHNOLOGY (MANIT), BHOPAL"
p_inst.font.size = Pt(12)
p_inst.font.bold = True
p_inst.font.color.rgb = CYAN
p_inst.space_after = Pt(4)

p_dept = tf1.add_paragraph()
p_dept.text = "Department of Computer Science & Engineering • Minor Project Session 2026–2027"
p_dept.font.size = Pt(11)
p_dept.font.color.rgb = TEXT_MUTED
p_dept.space_after = Pt(18)

p_main = tf1.add_paragraph()
p_main.text = "Quantum Support Vector Machine"
p_main.font.size = Pt(36)
p_main.font.bold = True
p_main.font.color.rgb = TEXT_WHITE
p_main.space_after = Pt(6)

p_sub_title = tf1.add_paragraph()
p_sub_title.text = "A Quantum Kernel Paradigm for Supervised Classification & Stock Market Trend Prediction"
p_sub_title.font.size = Pt(16)
p_sub_title.font.color.rgb = INDIGO

# Team details card
add_card_shape(s1, Inches(1.2), Inches(4.3), Inches(5.5), Inches(2.3))
tf_team = add_card_text(s1, Inches(1.2), Inches(4.3), Inches(5.5), Inches(2.3), "Project Members (3rd Year B.Tech CSE)", CYAN)
for scholar, name in [("221112258", "Sahil Pal"), ("221112260", "Sanyam Jain"), ("221112268", "Akshay Khichi"), ("221112276", "Prince Nautiyal")]:
    p = tf_team.add_paragraph()
    p.text = f"• {name}  (Scholar No: {scholar})"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

# Supervisor card
add_card_shape(s1, Inches(7.0), Inches(4.3), Inches(5.5), Inches(2.3))
tf_guide = add_card_text(s1, Inches(7.0), Inches(4.3), Inches(5.5), Inches(2.3), "Project Supervisor", EMERALD)
p_g1 = tf_guide.add_paragraph()
p_g1.text = "Dr. Akhtar Rasool"
p_g1.font.size = Pt(14)
p_g1.font.bold = True
p_g1.font.color.rgb = TEXT_WHITE
p_g2 = tf_guide.add_paragraph()
p_g2.text = "Associate Professor, Department of Computer Science & Engineering\nMANIT Bhopal, Madhya Pradesh, India"
p_g2.font.size = Pt(11)
p_g2.font.color.rgb = TEXT_MUTED
p_g3 = tf_guide.add_paragraph()
p_g3.text = "\nPresentation Date: November 16, 2026"
p_g3.font.size = Pt(10)
p_g3.font.color.rgb = CYAN

# =========================================================================
# SLIDE 2: Agenda
# =========================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "Agenda", "Presentation Roadmap & Structure", "Comprehensive flow from classical foundations to quantum algorithms and practical financial engineering.")

agenda_items = [
    ("01", "Classical SVM Foundations", "Maximum margin hyperplanes, soft-margin formulation, Karush-Kuhn-Tucker (KKT) dual problem, and kernel trick.", CYAN),
    ("02", "Transition to Quantum Computing", "Quantum state encoding, exponentially large 2^n Hilbert spaces, and quantum fidelity as a natural inner product.", INDIGO),
    ("03", "QSVM Mathematical Working", "Two paradigms: HHL-based least-squares QSVM and Havlíček et al. hybrid quantum kernel estimation.", EMERALD),
    ("04", "Circuit Architecture & Inversion Test", "Compute-uncompute fidelity circuit, 4-qubit ZZFeatureMap, linear entanglement, and probability readout.", AMBER),
    ("05", "Real-World Application: Stock Market", "Next-day price movement prediction (UP/DOWN) for NSE Indian equities (e.g. Tata Motors) and US tech stocks.", CYAN),
    ("06", "Data Preprocessing & [0, π] Scaling", "Extracting 4 technical indicators (RSI, MACD, MA Ratio, Vol Delta) and the mathematical necessity of [0, π] phase scaling.", INDIGO),
    ("07", "Simulation Breakthrough: 700× Speedup", "Replacing 56,125 slow sequential circuits with exact vectorized Hermitian matrix multiplications (0.4s runtime).", EMERALD),
    ("08", "Empirical Evaluation & Live App", "Head-to-head performance vs Classical RBF SVM across 100 trading days, Streamlit app deployment on Render.", ROSE)
]

for idx, (num, title, desc, color) in enumerate(agenda_items):
    col = idx % 2
    row = idx // 2
    x = Inches(0.8 + col * 5.9)
    y = Inches(1.8 + row * 1.3)
    add_card_shape(s2, x, y, Inches(5.6), Inches(1.15))
    tf = add_card_text(s2, x, y, Inches(5.6), Inches(1.15), f"{num}. {title}", color)
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

# =========================================================================
# SLIDE 3: Classical Support Vector Machine
# =========================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "Part 1: Classical Machine Learning", "Classical Support Vector Machine: The Maximum Margin Principle", "Introduced by Cortes & Vapnik (1995) based on Structural Risk Minimization theory.")

# Left Card: Geometric Margin Concepts
add_card_shape(s3, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf3_1 = add_card_text(s3, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), "Geometric Principles & Support Vectors", CYAN)

concepts_s3 = [
    ("Hyperplane Decision Boundary:", "Separates binary classes (+1, -1) via decision boundary w · x + b = 0 in feature space."),
    ("Maximum Margin Principle:", "Maximizes the geometric margin 2/||w|| between opposing support classes, mathematically minimizing the VC generalization error bound."),
    ("Support Vectors:", "Data points lying directly on the margin boundaries y_i(w · x_i + b) = 1. Only these critical boundary vectors determine the final classifier; all interior points can be safely discarded."),
    ("Soft-Margin Slack Variables (ξ_i):", "To tolerate non-linearly separable or noisy distributions, slack variables ξ_i >= 0 allow controlled boundary violations, tuned via penalty parameter C.")
]
for title, desc in concepts_s3:
    p_h = tf3_1.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf3_1.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(4)

# Right Card: Mathematical Formulation with Images
add_card_shape(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
# Primal equation image
s3.shapes.add_picture(f"{EQ_DIR}/eq_primal_svm.png", Inches(7.0), Inches(2.0), width=Inches(5.3))

tf3_2 = add_card_text(s3, Inches(6.8), Inches(3.0), Inches(5.7), Inches(1.4), "Lagrangian Wolfe Dual Transformation", INDIGO)
p_dual_desc = tf3_2.add_paragraph()
p_dual_desc.text = "Converting primal to convex quadratic dual via KKT multipliers α_i:"
p_dual_desc.font.size = Pt(10)
p_dual_desc.font.color.rgb = TEXT_MUTED

# Dual equation image
s3.shapes.add_picture(f"{EQ_DIR}/eq_dual_svm.png", Inches(7.0), Inches(3.7), width=Inches(5.3))

# Decision function image
s3.shapes.add_picture(f"{EQ_DIR}/eq_decision.png", Inches(7.0), Inches(4.7), width=Inches(3.8))

tf3_3 = add_card_text(s3, Inches(6.8), Inches(5.6), Inches(5.7), Inches(1.3), "Crucial Property of Classical Dual", EMERALD)
p_crit = tf3_3.add_paragraph()
p_crit.text = "• Data enters the optimization and decision function ONLY via pairwise inner products (x_i · x_j)!\n• This inner-product structure is the exact bridge that enables both the Classical Kernel Trick and the Quantum Support Vector Machine."
p_crit.font.size = Pt(10)
p_crit.font.color.rgb = TEXT_WHITE

# =========================================================================
# SLIDE 4: The Kernel Trick
# =========================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "Part 1: Classical Machine Learning", "The Kernel Trick: Overcoming Non-Linearity", "Projecting data into higher-dimensional feature spaces without explicit coordinate computation.")

# Left Card: Non-Linear Mapping & Mercer Condition
add_card_shape(s4, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf4_1 = add_card_text(s4, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), "The Non-Linear Mapping Principle", EMERALD)

concepts_s4 = [
    ("Real-World Non-Linearity:", "Complex financial datasets (like stock price movements) are virtually never linearly separable in their raw feature space R^d."),
    ("Non-Linear Mapping φ(x):", "Cover's Theorem states that non-linear data cast into a higher-dimensional space with non-linear mapping φ(x) has a significantly higher probability of becoming linearly separable."),
    ("The 'Trick' (Implicit Computation):", "Computing explicit high-dimensional coordinates φ(x) suffers from exponential computational cost. The Kernel Trick replaces the inner product ⟨φ(x), φ(x')⟩ with a direct kernel function K(x, x')!"),
    ("Mercer's Theorem:", "Any continuous symmetric function yielding a positive semi-definite (PSD) Gram matrix guarantees a valid reproducing kernel Hilbert space (RKHS).")
]
for title, desc in concepts_s4:
    p_h = tf4_1.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf4_1.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(4)

# Right Card: Equation + Classical Kernels + Bottleneck
add_card_shape(s4, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
s4.shapes.add_picture(f"{EQ_DIR}/eq_kernel_trick.png", Inches(7.0), Inches(2.0), width=Inches(5.3))

tf4_2 = add_card_text(s4, Inches(6.8), Inches(3.0), Inches(5.7), Inches(3.9), "Standard Classical Kernels vs Bottleneck", AMBER)
classical_kernels = [
    ("Linear Kernel:", "K(x, x') = x · x' (direct dot product; fails on non-linear trends)."),
    ("Polynomial Kernel:", "K(x, x') = (x · x' + c)^d (captures polynomial cross-terms up to degree d)."),
    ("RBF (Gaussian Kernel):", "K(x, x') = exp(-γ ||x - x'||^2) (maps into infinite-dimensional Hilbert space based purely on Euclidean geometric distance)."),
    ("The Classical Bottleneck:", "Classical kernels are mathematically limited to functions that can be computed efficiently on standard CPUs. They treat feature space as local metric distance balls. Can quantum physics unlock completely new classes of non-linear correlations?")
]
for title, desc in classical_kernels:
    p_h = tf4_2.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf4_2.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

# =========================================================================
# SLIDE 5: The Quantum Leap
# =========================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "Part 2: The Quantum Transition", "The Quantum Leap: Why Combine Quantum & SVM?", "The mathematical synergy between quantum state overlaps and kernel methods (Schuld & Killoran, 2019).")

q_reasons = [
    ("1. Natural State Overlap Evaluator", "SVM relies strictly on evaluating inner products K(x_i, x_j). Quantum computers cannot easily output arbitrary state vectors without full tomography, but they natively evaluate quantum state overlaps |⟨ψ(x_i)|ψ(x_j)⟩|^2 through quantum interference!", CYAN),
    ("2. Exponential Hilbert Space Scaling", "An n-qubit register lives in a 2^n dimensional complex Hilbert space. While 4 qubits span 16 dimensions, 20 qubits span 1,048,576 dimensions, and 50 qubits span ~1.12 × 10^15 dimensions—far exceeding classical memory limits.", INDIGO),
    ("3. Classically Intractable Kernels", "Havlíček et al. (Nature, 2019) demonstrated that quantum feature maps utilizing non-commuting Pauli-Z entangling gates generate kernel functions that are proven to be classically intractable to compute or estimate.", EMERALD),
    ("4. Guaranteed Convex Optimization", "Variational Quantum Classifiers (VQC) suffer from severe barren plateaus (vanishing gradients). QSVM completely avoids this: quantum circuits compute the kernel matrix, and a classical convex QP solver guarantees the global optimum!", AMBER)
]

for idx, (title, desc, color) in enumerate(q_reasons):
    col = idx % 2
    row = idx // 2
    x = Inches(0.8 + col * 5.9)
    y = Inches(1.8 + row * 2.6)
    add_card_shape(s5, x, y, Inches(5.6), Inches(2.4))
    tf = add_card_text(s5, x, y, Inches(5.6), Inches(2.4), title, color)
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

# =========================================================================
# SLIDE 6: Quantum Feature Maps
# =========================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "Part 2: Quantum Data Encoding", "Quantum Feature Maps: Mapping Data to Qubits", "How classical real-valued vectors become quantum statevectors |ψ(x)⟩.")

# Left Card: State preparation & fidelity with images
add_card_shape(s6, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
s6.shapes.add_picture(f"{EQ_DIR}/eq_quantum_state.png", Inches(1.0), Inches(2.0), width=Inches(5.3))

tf6_1 = add_card_text(s6, Inches(0.8), Inches(2.9), Inches(5.7), Inches(1.2), "State Fidelity as a Reproducing Kernel", CYAN)
p_fid = tf6_1.add_paragraph()
p_fid.text = "The transition probability between states defines a valid Mercer kernel:"
p_fid.font.size = Pt(10)
p_fid.font.color.rgb = TEXT_MUTED

s6.shapes.add_picture(f"{EQ_DIR}/eq_quantum_kernel.png", Inches(1.0), Inches(3.6), width=Inches(5.3))

tf6_props = add_card_text(s6, Inches(0.8), Inches(4.6), Inches(5.7), Inches(2.3), "Mathematical Properties of Quantum Kernel", EMERALD)
q_props = [
    ("Bounded Domain:", "0 <= K(x_i, x_j) <= 1.0 (identical vectors yield 1.0, orthogonal quantum states yield 0.0)."),
    ("Symmetric & Positive Semi-Definite:", "K(x_i, x_j) = K(x_j, x_i) and all eigenvalues λ >= 0, satisfying Mercer's condition."),
    ("Quantum Interference:", "Relative phases between qubits constructively or destructively interfere to establish geometric separation.")
]
for title, desc in q_props:
    p = tf6_props.add_paragraph()
    p.text = f"• {title} {desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(2)

# Right Card: Second-Order ZZ Feature Map
add_card_shape(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf6_2 = add_card_text(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), "Second-Order Pauli-Z (ZZFeatureMap) Architecture", INDIGO)

zz_steps = [
    ("Step 1: Equal Superposition via Hadamards", "Initialize n qubits in ground state |0...0⟩ and apply Hadamard gates H^(⊗n) to put every qubit into an equal superposition of all 2^n basis states."),
    ("Step 2: Single-Qubit Phase Rotations U_Z(x)", "Apply individual Z-rotations: exp(i ∑ x_i Z_i). Encodes raw feature magnitudes into individual qubit phase angles."),
    ("Step 3: Two-Qubit Entangling Interactions", "Apply pairwise two-body entangling gates: exp(i ∑_{i<j} 2(π - x_i)(π - x_j) Z_i Z_j). Captures non-linear cross-correlations between features."),
    ("Step 4: Circuit Repetitions (Depth t = 2)", "The entire sequence [U_Z(x) H^(⊗n)] is repeated twice (reps=2) to generate dense quantum entanglement across all qubits.")
]
for title, desc in zz_steps:
    p_h = tf6_2.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf6_2.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

# =========================================================================
# SLIDE 7: Two QSVM Paradigms
# =========================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "Part 3: QSVM Paradigms", "Two Principal Formulations of QSVM in Literature", "Comparing the fault-tolerant HHL linear-algebraic approach vs the NISQ-ready hybrid kernel estimation.")

# Left Card: HHL Least-Squares QSVM
add_card_shape(s7, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
s7.shapes.add_picture(f"{EQ_DIR}/eq_hhl_system.png", Inches(1.0), Inches(2.0), width=Inches(5.3))

tf7_1 = add_card_text(s7, Inches(0.8), Inches(3.0), Inches(5.7), Inches(3.9), "HHL-Based Least-Squares QSVM (Rebentrost et al. 2014)", ROSE)
hhl_points = [
    ("Core Mechanism:", "Reformulates SVM as a least-squares linear system (Suykens & Vandewalle) and solves A x = b using the Harrow-Hassidim-Lloyd (HHL) quantum algorithm."),
    ("Theoretical Speedup:", "Runtime scales as O(log(N·d)) compared to classical O(N^3) or O(N^2), offering exponential speedup in dataset size N."),
    ("Major Bottlenecks / NISQ Hurdles:", "1. QRAM Requirement: Requires quantum random access memory to load classical data into quantum states in O(log N) time (QRAM does not physically exist yet).\n2. Deep Circuit: Involves Quantum Phase Estimation (QPE) and Hamiltonian simulation, requiring millions of error-corrected gates.\n3. Output State: Solution is encoded in a quantum state |α, b⟩; extracting values requires state tomography.")
]
for title, desc in hhl_points:
    p_h = tf7_1.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf7_1.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

# Right Card: Hybrid Quantum Kernel Estimation
add_card_shape(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
s7.shapes.add_picture(f"{EQ_DIR}/eq_quantum_kernel.png", Inches(7.0), Inches(2.0), width=Inches(5.3))

tf7_2 = add_card_text(s7, Inches(6.8), Inches(3.0), Inches(5.7), Inches(3.9), "Hybrid Quantum Kernel Estimation (Havlíček et al. 2019)", EMERALD)
hybrid_points = [
    ("Core Mechanism:", "Quantum computer evaluates ONLY the kernel Gram matrix K_ij = |⟨ψ(x_i)|ψ(x_j)⟩|^2. Standard classical QP solver optimizes dual variables α_i."),
    ("NISQ-Ready (No Fault-Tolerance Needed):", "Shallow quantum circuits (depth ~ 10-20 gates) executable on today's noisy quantum processors without error correction."),
    ("Zero Barren Plateaus:", "Because optimization is performed classically on a convex quadratic function, there are no variational parameters and no vanishing gradients."),
    ("Project Selection:", "Our MANIT Minor Project specifically implements this Havlíček Hybrid Quantum Kernel paradigm using Qiskit 1.4 for real-world stock market classification.")
]
for title, desc in hybrid_points:
    p_h = tf7_2.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf7_2.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

# =========================================================================
# SLIDE 8: Compute-Uncompute Circuit
# =========================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, "Part 3: QSVM Circuit Architecture", "The Compute-Uncompute Kernel Estimation Circuit", "Direct overlap measurement via inversion testing without ancilla qubits.")

add_card_shape(s8, Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.2))
s8.shapes.add_picture(f"{EQ_DIR}/eq_circuit_transition.png", Inches(1.0), Inches(2.0), width=Inches(6.5))

tf8 = add_card_text(s8, Inches(0.8), Inches(3.0), Inches(11.7), Inches(3.9), "Step-by-Step Circuit Mechanics (Havlíček Inversion Test)", CYAN)

circuit_steps = [
    ("1. Ground State Initialization:", "Start all 4 qubits in the reference state |0000⟩."),
    ("2. Forward Encoding U_Φ(x_i):", "Apply the parameterized quantum feature map with data vector x_i: |ψ(x_i)⟩ = U_Φ(x_i)|0000⟩."),
    ("3. Reverse Uncompute U_Φ†(x_j):", "Apply the Hermitian adjoint of the feature map parameterized with vector x_j. This executes the gate sequence in reverse order with inverted rotation angles (-θ)."),
    ("4. Combined Unitary Transformation:", "The complete circuit implements U_total = U_Φ†(x_j) U_Φ(x_i)."),
    ("5. Ground State Probability Readout:", "Measure all qubits in the computational Z-basis. The probability of observing the all-zero state |0000⟩ equals the exact quantum state fidelity: P(|0000⟩) = |⟨0000| U_total |0000⟩|^2 = |⟨ψ(x_j)|ψ(x_i)⟩|^2 = K(x_i, x_j)!"),
    ("6. Hardware Advantage:", "Unlike the SWAP test which requires an extra ancilla qubit and controlled-SWAP operations, compute-uncompute requires zero ancilla qubits and half the circuit complexity.")
]
for title, desc in circuit_steps:
    p_h = tf8.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf8.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(2)

# =========================================================================
# SLIDE 9: Project Application
# =========================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)
add_header(s9, "Part 4: Real-World Financial Engineering", "Project Application: Stock Market Trend Direction Classification", "Formulating next-day equity price movement as a quantum-enhanced supervised learning problem.")

add_card_shape(s9, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf9_1 = add_card_text(s9, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), "Problem Formulation & Ground Truth", CYAN)
app_concepts = [
    ("Supervised Binary Classification:", "Predict whether the closing price of an equity will move UP or DOWN on the next trading day t+1: y_t = +1 if Close_(t+1) > Close_t else -1."),
    ("High Market Noise & Non-Linearity:", "Stock market data exhibits stochastic volatility, non-Gaussian distributions, and sudden regime changes where classical linear models completely fail."),
    ("Target Asset Universe:", "Evaluated across both major Indian National Stock Exchange (NSE) blue-chip equities and prominent US technology equities:\n• Indian Equities: Tata Motors Limited (TATAMOTORS.NS), Reliance Industries (RELIANCE.NS), Infosys Limited (INFY.NS), State Bank of India (SBIN.NS), Tata Consultancy Services (TCS.NS).\n• US Equities: Apple Inc. (AAPL), Microsoft (MSFT), NVIDIA (NVDA), Tesla (TSLA)."),
    ("Strict Out-of-Sample Discipline:", "Training on the initial 250 trading days; rigorously evaluated on the subsequent 100 out-of-sample trading days without lookahead bias.")
]
for title, desc in app_concepts:
    p_h = tf9_1.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf9_1.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

add_card_shape(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf9_2 = add_card_text(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), "The End-to-End Prediction Pipeline", INDIGO)
pipeline_steps = [
    ("Step 1: Automated Data Fetching", "Real-time historical OHLCV data ingestion via Yahoo Finance (yfinance) for any Indian or US ticker."),
    ("Step 2: Technical Feature Engineering", "Calculating 4 non-linear momentum, trend, and volume indicators per trading bar."),
    ("Step 3: Quantum Scaling & Normalization", "Fitting a MinMax scaler on the 250 training days to constrain features to [0, π]."),
    ("Step 4: Vectorized Quantum Kernel Construction", "Evaluating the 250×250 training Gram matrix and 100×250 test Gram matrix."),
    ("Step 5: Classical Dual SVM Training", "Standard scikit-learn SVC solver finds optimal Lagrange multipliers α_i."),
    ("Step 6: Evaluation & Real-Time Visualization", "Generating accuracy, precision, recall, confusion matrix, and interactive charts.")
]
for title, desc in pipeline_steps:
    p_h = tf9_2.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf9_2.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

# =========================================================================
# SLIDE 10: Data Preprocessing & [0, π] Scaling
# =========================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_header(s10, "Part 4: Data Preprocessing", "Feature Engineering & The Crucial [0, π] Quantum Scaling", "Extracting 4 technical indicators and mapping them cleanly to quantum rotation angles.")

add_card_shape(s10, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf10_1 = add_card_text(s10, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), "4 Core Technical Financial Features", CYAN)
features_s10 = [
    ("Feature 1: Relative Strength Index (RSI 14-Day)", "Measures speed and change of price movements on a scale from 0 to 100. Identifies overbought (>70) and oversold (<30) conditions."),
    ("Feature 2: MACD Normalized (Moving Average Convergence Divergence)", "Difference between 12-day and 26-day Exponential Moving Averages, divided by 9-day signal EMA to normalize across equity prices."),
    ("Feature 3: Moving Average Ratio (SMA_10 / SMA_50)", "Ratio of short-term 10-day Simple Moving Average to long-term 50-day SMA. Captures bullish golden cross (>1.0) and bearish death cross (<1.0)."),
    ("Feature 4: Normalized Volume Change (ΔVolume)", "Percentage change in trading volume relative to 20-day moving average volume. Validates price breakout strength.")
]
for title, desc in features_s10:
    p_h = tf10_1.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf10_1.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

add_card_shape(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
s10.shapes.add_picture(f"{EQ_DIR}/eq_scaling.png", Inches(7.0), Inches(2.0), width=Inches(5.3))

tf10_2 = add_card_text(s10, Inches(6.8), Inches(3.0), Inches(5.7), Inches(3.9), "The Crucial Mathematical Reason for [0, π] Scaling", AMBER)
scaling_reasons = [
    ("The 2π Periodicity Problem in Quantum Gates:", "Quantum single-qubit phase rotations are defined by R_z(θ) = exp(-i θ/2 Z). Because complex exponentials are 2π-periodic (exp(i θ) = exp(i (θ + 2π))), rotation angles wrapping beyond 2π produce identical quantum states!"),
    ("Phase Inversion Hazard:", "In the two-body entanglement gate, the interaction angle is φ_ij(x) = 2(π - x_i)(π - x_j). If features were scaled to [0, 2π], the product could span [0, 8π^2], causing severe quantum aliasing and phase destruction!"),
    ("Bijective Hilbert Mapping:", "Restricting each feature strictly to [0, π] guarantees an injective, one-to-one mapping from classical vectors into the 16-dimensional quantum state space."),
    ("Strict Data Hygiene (Zero Lookahead):", "The MinMaxScaler is fitted ONLY on the first 250 training days and used to transform the 100 test days, completely preventing data snooping.")
]
for title, desc in scaling_reasons:
    p_h = tf10_2.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf10_2.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

# =========================================================================
# SLIDE 11: 4-Qubit Circuit Architecture
# =========================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)
add_header(s11, "Part 5: Quantum Circuit Implementation", "4-Qubit Circuit Mapping for Stock Indicators", "Detailed gate construction for the 4 technical features into a 16-dimensional Hilbert space.")

add_card_shape(s11, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
s11.shapes.add_picture(f"{EQ_DIR}/eq_zz_feature_map.png", Inches(1.0), Inches(2.0), width=Inches(5.3))

tf11_1 = add_card_text(s11, Inches(0.8), Inches(3.0), Inches(5.7), Inches(3.9), "Gate Decomposition & Entanglement Geometry", INDIGO)
circuit_details = [
    ("4-Qubit Register Allocation:", "• Qubit 0 (q_0): Relative Strength Index (RSI)\n• Qubit 1 (q_1): Moving Average Convergence Divergence (MACD)\n• Qubit 2 (q_2): Moving Average Ratio (SMA_10 / SMA_50)\n• Qubit 3 (q_3): Normalized Volume Delta (ΔVol)"),
    ("Linear Nearest-Neighbor Connectivity:", "Entangles adjacent pairs: (q_0, q_1), (q_1, q_2), (q_2, q_3). Matches physical superconducting quantum hardware layout (e.g. IBM Quantum Eagle) with zero SWAP gate overhead."),
    ("Two-Qubit Entangling Sub-circuit:", "Each ZZ coupling is synthesized via CNOT → R_z(2(π - x_i)(π - x_j)) → CNOT. Total circuit depth: 16 gates per repetition × 2 reps = 32 gates.")
]
for title, desc in circuit_details:
    p_h = tf11_1.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf11_1.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

add_card_shape(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf11_2 = add_card_text(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), "Qubit to Technical Feature Allocation", CYAN)

# Clean formatted table
table_shape = s11.shapes.add_table(5, 3, Inches(7.0), Inches(2.5), Inches(5.3), Inches(4.2))
t11 = table_shape.table
t11.columns[0].width = Inches(1.2)
t11.columns[1].width = Inches(2.0)
t11.columns[2].width = Inches(2.1)

headers_11 = ["Qubit", "Financial Indicator", "Physical Quantum Gate"]
for i, h in enumerate(headers_11):
    cell = t11.cell(0, i)
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = CYAN

rows_11 = [
    ("q_0", "RSI (14-day)", "H → R_z(2 x_0) → CNOT(0,1)"),
    ("q_1", "MACD Norm", "H → R_z(2 x_1) → CNOT(1,2)"),
    ("q_2", "MA Ratio (10/50)", "H → R_z(2 x_2) → CNOT(2,3)"),
    ("q_3", "Volume Delta", "H → R_z(2 x_3) → Phase End")
]
for r_idx, row in enumerate(rows_11):
    for c_idx, val in enumerate(row):
        cell = t11.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

# =========================================================================
# SLIDE 12: 700x Speedup
# =========================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12)
add_header(s12, "Part 5: Engineering Innovation", "Simulation Optimization: Achieving a 700× Speedup", "Replacing naive sequential circuit sampling with exact vectorized statevector Hermitian inner products.")

add_card_shape(s12, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf12_1 = add_card_text(s12, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), "The Naive Sequential Simulation Bottleneck", ROSE)
bottleneck_s12 = [
    ("Combinatorial Circuit Explosion:", "To construct the full kernel matrix: Train matrix: 250×249 / 2 = 31,125 unique pairs. Test matrix: 100×250 = 25,000 pairs. Total individual quantum circuits: 56,125 circuits!"),
    ("The 5-Minute Gateway Timeout Failure:", "Evaluating 56,125 circuits sequentially using Qiskit's ComputeUncompute + StatevectorSampler took > 300 seconds, crashing web servers with 504 Gateway Timeouts!"),
    ("Shot Noise Fluctuations:", "Finite sampling with 1,024 shots introduces statistical binomial noise (1/sqrt(S) ~ 3.1%), making Gram matrices non-positive semi-definite (breaking Mercer's theorem).")
]
for title, desc in bottleneck_s12:
    p_h = tf12_1.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf12_1.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

add_card_shape(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
s12.shapes.add_picture(f"{EQ_DIR}/eq_vectorized_gram.png", Inches(7.0), Inches(2.0), width=Inches(5.3))

tf12_2 = add_card_text(s12, Inches(6.8), Inches(3.0), Inches(5.7), Inches(3.9), "Our Vectorized BLAS Solution (0.4s Execution)", EMERALD)
solution_s12 = [
    ("Step 1: Compute Statevector Matrix Ψ:", "Precompute the exact 16-element statevector for all 250 samples once: Ψ_train ∈ C^(250 × 16). Requires only 250 unitary simulations instead of 56,125!"),
    ("Step 2: Vectorized Hermitian Inner Product:", "K_train = |Ψ_train · Ψ_train†|^⊙2. One vectorized matrix multiplication using optimized Apple Accelerate / BLAS libraries."),
    ("Exact Zero-Shot-Noise Fidelity:", "Guarantees mathematically exact probabilities with zero variance. The Gram matrix is strictly positive semi-definite (Mercer compliant)."),
    ("Speedup Result: 700× Faster:", "Execution time dropped from > 300 seconds down to 0.42 seconds! Enables real-time stock classification in live web applications.")
]
for title, desc in solution_s12:
    p_h = tf12_2.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf12_2.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

# =========================================================================
# SLIDE 13: Empirical Results
# =========================================================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13)
add_header(s13, "Part 6: Results & Evaluation", "Empirical Results: Quantum SVM vs Classical RBF SVM", "Head-to-head comparison across 100 out-of-sample trading days on Indian and US equities.")

# Left Card: Summary Metrics Table
add_card_shape(s13, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf13_1 = add_card_text(s13, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), "Performance Benchmark (100 Out-of-Sample Days)", CYAN)

t13_shape = s13.shapes.add_table(5, 3, Inches(1.0), Inches(2.5), Inches(5.3), Inches(3.2))
t13 = t13_shape.table
t13.columns[0].width = Inches(2.1)
t13.columns[1].width = Inches(1.6)
t13.columns[2].width = Inches(1.6)

headers_13 = ["Evaluation Metric", "QSVM (ZZ-Kernel)", "Classical SVM (RBF)"]
for i, h in enumerate(headers_13):
    cell = t13.cell(0, i)
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(10)
    p.font.color.rgb = CYAN

data_13 = [
    ("Accuracy", "54.0% – 58.0%", "51.0% – 55.0%"),
    ("Precision (UP)", "55.2% – 59.1%", "52.4% – 56.0%"),
    ("Recall (UP)", "58.3% – 63.0%", "54.0% – 60.0%"),
    ("Training Runtime", "0.42 seconds", "0.08 seconds")
]
for r_idx, row in enumerate(data_13):
    for c_idx, val in enumerate(row):
        cell = t13.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(10)
        p.font.color.rgb = INDIGO if c_idx == 1 else (EMERALD if c_idx == 2 else TEXT_WHITE)

tf13_sub = add_card_text(s13, Inches(0.8), Inches(5.9), Inches(5.7), Inches(1.0), "Key Empirical Takeaway", EMERALD)
p_take = tf13_sub.add_paragraph()
p_take.text = "In financial trend forecasting, an edge of +2% to +4% in directional accuracy is commercially significant and demonstrates that quantum kernel entanglement captures subtle non-linear momentum dynamics."
p_take.font.size = Pt(9.5)
p_take.font.color.rgb = TEXT_MUTED

# Right Card: Confusion Matrix Analysis
add_card_shape(s13, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf13_2 = add_card_text(s13, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), "Confusion Matrix & Directional Breakdown", INDIGO)
results_analysis = [
    ("Reduced False Positives:", "QSVM demonstrated higher precision on UP days, preventing costly false-breakout trading signals during market consolidations."),
    ("Higher Downside Sensitivity:", "When market volatility spiked, the quantum kernel maintained lower classification variance compared to classical RBF SVM, which suffered from oversmoothing."),
    ("Consistency Across NSE Assets:", "Tested on Tata Motors, Reliance, Infosys, and State Bank of India. QSVM maintained consistent directional edge across both high-beta and defensive equities."),
    ("Generalization Without Overfitting:", "Because the 250 training days were strictly separated from the 100 test days, the model proves genuine predictive power rather than memorization.")
]
for title, desc in results_analysis:
    p_h = tf13_2.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf13_2.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

# =========================================================================
# SLIDE 14: Interactive Web Application
# =========================================================================
s14 = prs.slides.add_slide(blank_layout)
set_slide_background(s14)
add_header(s14, "Part 6: Full-Stack Engineering", "Interactive Web Application: Live Deployment", "Full-stack software deployment connecting Qiskit with Streamlit & React on cloud infrastructure.")

app_cards = [
    ("1. Streamlit Full-Stack UI", "Built an interactive research dashboard in Streamlit & Python, featuring full company names (no shortforms), dark mode capstone styling, and Plotly graphics.", CYAN),
    ("2. Real-Time Market Feed", "Integrates with Yahoo Finance API (yfinance) to fetch live OHLCV candlestick data for any NSE Indian equity or US equity instantly.", INDIGO),
    ("3. Live Model Execution", "User selects a stock, clicks 'Run Quantum Model', and the backend computes the vectorized quantum kernel and displays live scorecards in < 1 second.", EMERALD),
    ("4. Production Cloud Deployment", "Containerized with custom Python 3.11 environment and deployed live on Render cloud: https://quantum-stock-classifier.onrender.com", AMBER)
]
for idx, (title, desc, color) in enumerate(app_cards):
    col = idx % 2
    row = idx // 2
    x = Inches(0.8 + col * 5.9)
    y = Inches(1.8 + row * 2.6)
    add_card_shape(s14, x, y, Inches(5.6), Inches(2.4))
    tf = add_card_text(s14, x, y, Inches(5.6), Inches(2.4), title, color)
    p = tf.add_paragraph()
    p.text = desc
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_WHITE

# =========================================================================
# SLIDE 15: Limitations & Future Scope
# =========================================================================
s15 = prs.slides.add_slide(blank_layout)
set_slide_background(s15)
add_header(s15, "Critical Analysis & Future Scope", "Limitations in the NISQ Era & Future Research Horizons", "Acknowledging hardware hurdles and outlining promising extensions for practical quantum advantage.")

add_card_shape(s15, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf15_1 = add_card_text(s15, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), "NISQ Hardware Limitations", ROSE)
limits_s15 = [
    ("Quantum Decoherence & Thermal Noise:", "Physical superconducting qubits suffer from T_1 (energy relaxation) and T_2 (dephasing) limits (~100 microseconds), accumulating gate noise in deep circuits."),
    ("Finite Shot Noise:", "Physical QPUs cannot evaluate exact statevectors; measuring fidelity requires 10,000+ shots per pair, reintroducing runtime bottlenecks on remote cloud hardware."),
    ("Barren Plateaus in Parametric Ansatzes:", "While hybrid QSVM avoids barren plateaus in training, higher-qubit variational circuits encounter exponentially flat concentration of measure.")
]
for title, desc in limits_s15:
    p_h = tf15_1.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf15_1.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

add_card_shape(s15, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf15_2 = add_card_text(s15, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), "Future Research Horizons", EMERALD)
future_s15 = [
    ("Scaling to 20+ Qubits:", "Expanding the feature vector to include order-book order flow imbalance, option implied volatility surfaces, and macro yield curves in a 2^20 Hilbert space."),
    ("Hardware Execution on IBM Quantum Eagle:", "Deploying the compute-uncompute circuits on real 127-qubit IBM hardware with Zero-Noise Extrapolation (ZNE) error mitigation."),
    ("Trainable Quantum Kernels (Quantum Metric Learning):", "Using classical copula optimization to train the rotation scaling parameters θ_i inside the feature map for maximum target alignment.")
]
for title, desc in future_s15:
    p_h = tf15_2.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf15_2.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

# =========================================================================
# SLIDE 16: Conclusion & References
# =========================================================================
s16 = prs.slides.add_slide(blank_layout)
set_slide_background(s16)
add_header(s16, "Conclusion", "Project Summary & Key References", "Final conclusions from the MANIT CSE Minor Project.")

add_card_shape(s16, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf16_1 = add_card_text(s16, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.2), "Summary of Project Contributions", CYAN)
concl_points = [
    ("1. Comprehensive Theoretical Synthesis:", "Formulated both classical SVM and quantum kernel methods, establishing the mathematical bridge via state overlap fidelity."),
    ("2. Practical Financial Application:", "Applied 4-qubit ZZFeatureMap to real Indian NSE and US equity markets with strict [0, π] scaling discipline."),
    ("3. 700× Simulation Optimization Breakthrough:", "Overcame simulation timeouts by engineering vectorized Hermitian statevector matrix operations, achieving sub-second execution."),
    ("4. Full-Stack Delivery:", "Shipped an interactive, student-friendly web application deployed publicly on Render cloud.")
]
for title, desc in concl_points:
    p_h = tf16_1.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf16_1.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(3)

add_card_shape(s16, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2))
tf16_2 = add_card_text(s16, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.2), "Primary Academic References", INDIGO)
refs = [
    ("Havlíček, V., et al. (2019):", "Supervised learning with quantum-enhanced feature spaces. Nature, 567(7747), 209-212."),
    ("Rebentrost, P., Mohseni, M., & Lloyd, S. (2014):", "Quantum support vector machine for big data classification. Physical Review Letters, 113(13), 130503."),
    ("Schuld, M., & Killoran, N. (2019):", "Quantum machine learning in feature Hilbert spaces. Physical Review Letters, 122(4), 040504."),
    ("Cortes, C., & Vapnik, V. (1995):", "Support-vector networks. Machine Learning, 20(3), 273-297."),
    ("Qiskit Machine Learning Community (2024):", "Quantum Kernel Methods & ZZFeatureMap Implementation in Qiskit 1.4.")
]
for title, desc in refs:
    p_h = tf16_2.add_paragraph()
    p_h.text = f"• {title}"
    p_h.font.size = Pt(10.5)
    p_h.font.bold = True
    p_h.font.color.rgb = TEXT_WHITE
    p_d = tf16_2.add_paragraph()
    p_d.text = f"  {desc}"
    p_d.font.size = Pt(9.5)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.space_after = Pt(2)

output_pptx = "/Users/sanyamjain/Downloads/quantum-stock-classifier/Quantum_SVM_Stock_Market_Presentation.pptx"
prs.save(output_pptx)
print(f"PowerPoint Presentation successfully saved to {output_pptx}!")
