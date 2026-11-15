import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen dimensions
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

        # Category Tag
        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN
        p_cat.space_after = Pt(4)

        # Title
        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE
        p_title.space_after = Pt(3)

        # Subtitle
        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title="", title_color=CYAN, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        if title:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = title_color
            p.space_after = Pt(10)
        return tf

    # =========================================================================
    # SLIDE 1: Title Slide (Formal MANIT Presentation)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Accent decorative glow line
    line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(0.15), Inches(5.8))
    line.fill.solid()
    line.fill.fore_color.rgb = CYAN
    line.line.fill.background()

    # Title box
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

    p_main2 = tf1.add_paragraph()
    p_main2.text = "A Quantum Kernel Paradigm for Supervised Classification"
    p_main2.font.size = Pt(22)
    p_main2.font.bold = True
    p_main2.font.color.rgb = INDIGO
    p_main2.space_after = Pt(12)

    p_desc = tf1.add_paragraph()
    p_desc.text = "Benchmarking 4-Qubit ZZFeatureMap Quantum Kernels against Classical RBF SVM on Stock Market Trend Prediction"
    p_desc.font.size = Pt(13)
    p_desc.font.color.rgb = TEXT_MUTED

    # Metadata Cards (Submitted By & Guided By)
    add_card(s1, Inches(1.2), Inches(4.5), Inches(5.4), Inches(2.2), "Submitted By:", CYAN)
    card_sub = s1.shapes[-1].text_frame
    authors = [
        "• Sahil Pal (24112011120)",
        "• Sanyam Jain (24112011119)",
        "• Akshay Khichi (24112011127)",
        "• Prince Nautiyal (24112011124)"
    ]
    for a in authors:
        p = card_sub.add_paragraph()
        p.text = a
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(3)

    add_card(s1, Inches(6.9), Inches(4.5), Inches(5.5), Inches(2.2), "Supervised By:", EMERALD)
    card_guide = s1.shapes[-1].text_frame
    p_g1 = card_guide.add_paragraph()
    p_g1.text = "Dr. Akhtar Rasool"
    p_g1.font.size = Pt(15)
    p_g1.font.bold = True
    p_g1.font.color.rgb = TEXT_WHITE
    p_g1.space_after = Pt(3)

    p_g2 = card_guide.add_paragraph()
    p_g2.text = "Assistant Professor\nDepartment of Computer Science & Engineering\nMANIT Bhopal"
    p_g2.font.size = Pt(11)
    p_g2.font.color.rgb = TEXT_MUTED
    p_g2.space_after = Pt(10)

    p_g3 = card_guide.add_paragraph()
    p_g3.text = "Date of Presentation: 16 November 2026"
    p_g3.font.size = Pt(11)
    p_g3.font.bold = True
    p_g3.font.color.rgb = AMBER

    # =========================================================================
    # SLIDE 2: Presentation Structure / Roadmap
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Agenda", "Presentation Roadmap & Structure", "Comprehensive flow from classical foundations to quantum algorithms and practical financial engineering.")

    agenda_items = [
        ("01", "Classical SVM Foundations", "Maximum-margin hyperplane, primal soft-margin formulation, Lagrangian dual, and Mercer's kernel trick.", CYAN),
        ("02", "The Quantum Leap: Why QML?", "Why SVM is uniquely suited for quantum computers, Hilbert spaces, and exponential dimensional advantage.", INDIGO),
        ("03", "QSVM Mathematical Working", "Two paradigms: HHL-based least-squares QSVM and Havlíček et al. hybrid quantum kernel estimation.", EMERALD),
        ("04", "Feature Maps & Quantum Circuits", "Data encoding to [0, π], ZZFeatureMap 4-qubit circuit, compute-uncompute inversion test.", AMBER),
        ("05", "Application: Stock Market Analysis", "Predicting next-day price direction (UP/DOWN) on Indian & US equities using 5-year Yahoo Finance feeds.", ROSE),
        ("06", "Benchmark Results & Software Demo", "Vectorized 700x simulation speedup, empirical metrics, confusion matrices, Streamlit app, and limitations.", CYAN)
    ]

    for idx, (num, heading, desc, col) in enumerate(agenda_items):
        row = idx // 3
        col_pos = idx % 3
        left = Inches(0.8 + col_pos * 4.0)
        top = Inches(1.9 + row * 2.6)
        
        card_tf = add_card(s2, left, top, Inches(3.7), Inches(2.3), f"{num}. {heading}", col)
        p = card_tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 3: Part 1 - Classical SVM Working & Maximum Margin
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Part 1: Classical Machine Learning", "Classical Support Vector Machine: The Maximum Margin Principle", "Introduced by Cortes & Vapnik (1995) based on Structural Risk Minimization theory.")

    # Left Card: Core Concepts
    c1 = add_card(s3, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0), "Geometric Margin & Support Vectors", CYAN)
    points_c1 = [
        ("Binary Linear Separation:", "Given training data {(x_i, y_i)} with y_i in {-1, +1}, the SVM seeks an optimal decision hyperplane: w·x + b = 0."),
        ("Maximum Margin Objective:", "Instead of any arbitrary separating line, SVM maximizes the geometric margin 2 / ||w|| between classes to achieve the lowest theoretical generalization error."),
        ("Support Vectors:", "Only critical boundary points that lie exactly on the margins (y_i(w·x_i + b) = 1) determine the decision boundary. All interior points can be discarded."),
        ("Soft-Margin Formulation:", "For non-linearly separable data, slack variables ξ_i >= 0 allow controlled violations, balanced by hyperparameter C:")
    ]
    for h, b in points_c1:
        p = c1.add_paragraph()
        p.text = f"{h} "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p_sub = c1.add_paragraph()
        p_sub.text = b
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(6)

    # Right Card: Mathematical Formulation
    c2 = add_card(s3, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0), "Primal Optimization Problem", INDIGO)
    math_primal = (
        "Primal Optimization Formulation:\n"
        "  min  ½ ||w||² + C ∑ ξ_i\n"
        "  s.t. y_i (w·x_i + b) >= 1 - ξ_i,   ξ_i >= 0\n\n"
        "Lagrangian Dual Problem:\n"
        "Using Karush-Kuhn-Tucker (KKT) conditions, we convert the primal into a convex quadratic dual:\n\n"
        "  max_α  ∑ α_i  -  ½ ∑∑ α_i α_j y_i y_j (x_i · x_j)\n"
        "  s.t.   0 <= α_i <= C   and   ∑ α_i y_i = 0\n\n"
        "Key Dual Properties:\n"
        "1. Convex Quadratic Program (QP) with a single global optimum.\n"
        "2. Crucial Observation: Data vectors x_i enter ONLY via inner products (x_i · x_j)!\n"
        "3. Final Decision Function:\n"
        "   f(x) = sign( ∑ α_i y_i (x_i · x) + b )"
    )
    p_m = c2.add_paragraph()
    p_m.text = math_primal
    p_m.font.size = Pt(11)
    p_m.font.name = "Courier New"
    p_m.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 4: Part 1 - The Classical Kernel Trick
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Part 1: Classical Machine Learning", "The Kernel Trick: Overcoming Non-Linearity", "Projecting data into higher-dimensional feature spaces without explicit coordinate computation.")

    c4_1 = add_card(s4, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0), "The Kernel Trick Concept", EMERALD)
    k_points = [
        ("The Challenge:", "Real-world datasets (like financial time series) are rarely linearly separable in their original input space R^N."),
        ("Non-Linear Mapping φ(x):", "We map data into a higher-dimensional feature space H: x -> φ(x), where the data becomes linearly separable."),
        ("The 'Curse of Dimensionality':", "Explicitly calculating coordinates φ(x) in high dimensions is computationally prohibitive and memory-intensive."),
        ("The Kernel Solution:", "Since the dual SVM only requires the inner product ⟨φ(x_i), φ(x_j)⟩, we define a kernel function k(x_i, x_j) that computes this dot product directly in input space!"),
        ("Mercer's Condition:", "Any symmetric, positive semi-definite continuous function k(x, x') defines a valid inner product in some reproducing kernel Hilbert space (RKHS).")
    ]
    for h, b in k_points:
        p = c4_1.add_paragraph()
        p.text = f"{h} "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p_sub = c4_1.add_paragraph()
        p_sub.text = b
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(6)

    c4_2 = add_card(s4, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0), "Common Classical Kernels vs Limitation", AMBER)
    classical_kernels = (
        "Classical Kernel Functions:\n\n"
        "• Linear Kernel: k(x, x') = x · x'\n"
        "  - Direct dot product in original space.\n\n"
        "• Polynomial Kernel: k(x, x') = (x · x' + c)^d\n"
        "  - Captures cross-feature degree interactions.\n\n"
        "• Radial Basis Function (RBF / Gaussian):\n"
        "  k(x, x') = exp( -γ ||x - x'||² )\n"
        "  - Maps into an infinite-dimensional Hilbert space!\n"
        "  - Measures Euclidean distance proximity.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "The Fundamental Classical Bottleneck:\n"
        "1. Classical kernels are limited to functions that can be\n"
        "   evaluated efficiently on classical CPUs.\n"
        "2. Standard RBF treats feature space purely as local\n"
        "   distance balls, missing complex global multi-body\n"
        "   correlations.\n"
        "3. Can quantum mechanics unlock a completely new\n"
        "   class of non-linear kernel functions?"
    )
    p_ck = c4_2.add_paragraph()
    p_ck.text = classical_kernels
    p_ck.font.size = Pt(11)
    p_ck.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 5: Part 2 - The Quantum Leap: Why Bring Quantum to SVM?
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Part 2: The Quantum Transition", "The Quantum Leap: Why Combine Quantum & SVM?", "The mathematical synergy between quantum state overlaps and kernel methods (Schuld & Killoran, 2019).")

    q_reasons = [
        ("1. Perfect Structural Synergy", "SVM depends on data ONLY through inner products k(x_i, x_j). Quantum computers do not naturally output large vectors, but they are natively built to measure quantum state overlaps (inner products) through interference and measurement!"),
        ("2. Exponential Hilbert Space", "An n-qubit quantum register spans an exponentially large 2^n complex Hilbert space. For just n=4 qubits, dimension = 16. For n=20 qubits, dimension = 1,048,576. For n=50 qubits, dimension = 1.1 × 10^15! This provides a massive feature space with very few qubits."),
        ("3. Classically Intractable Kernels", "Havlíček et al. (Nature, 2019) proved that certain parameterised quantum circuits (like ZZFeatureMap) generate kernels that are conjectured to be classically intractable to estimate using classical sampling."),
        ("4. Retaining Convexity (No Barren Plateaus)", "Variational Quantum Classifiers (VQC) suffer from vanishing gradients ('barren plateaus') during parameter training. Hybrid QSVM avoids this entirely: quantum hardware estimates the kernel matrix, while a classical convex QP solver finds the globally optimal hyperplane!")
    ]

    for idx, (title, text) in enumerate(q_reasons):
        x = Inches(0.8 + (idx % 2) * 5.9)
        y = Inches(1.9 + (idx // 2) * 2.5)
        tf = add_card(s5, x, y, Inches(5.6), Inches(2.2), title, CYAN)
        p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 6: Part 2 - Quantum Data Encoding & Feature Maps
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Part 2: Quantum Data Encoding", "Quantum Feature Maps: Mapping Data to Qubits", "How classical real-valued vectors become quantum statevectors |ψ(x)⟩.")

    c6_1 = add_card(s6, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0), "Quantum Feature Map Definition", INDIGO)
    fm_text = (
        "Mathematical Definition:\n"
        "A quantum feature map is a unitary operator U_φ(x) that encodes a classical feature vector x in R^N into an n-qubit quantum state:\n\n"
        "       |ψ(x)⟩ = U_φ(x) |0⟩^⊗n\n\n"
        "State Fidelity as Quantum Kernel:\n"
        "The similarity between two data points x and x' is defined as the transition probability (quantum state overlap):\n\n"
        "       k(x, x') = |⟨ψ(x) | ψ(x')⟩|²\n"
        "               = |⟨0|^⊗n U_φ†(x) U_φ(x') |0⟩^⊗n|²\n\n"
        "Properties of Quantum Kernel:\n"
        "• Bounded in [0, 1]:\n"
        "  - Identical data points: k(x, x) = 1.0\n"
        "  - Orthogonal quantum states: k(x, x') = 0.0\n"
        "• Symmetric: k(x, x') = k(x', x)\n"
        "• Strictly Positive Semi-Definite (Gram Matrix K >= 0)"
    )
    p_fm = c6_1.add_paragraph()
    p_fm.text = fm_text
    p_fm.font.size = Pt(11)
    p_fm.font.color.rgb = TEXT_WHITE

    c6_2 = add_card(s6, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0), "Second-Order Pauli ZZFeatureMap", EMERALD)
    zz_text = (
        "The ZZFeatureMap Circuit Structure (Havlíček et al., 2019):\n\n"
        "U_φ(x) = [ U_Z(x) · H^⊗n ]^t\n\n"
        "Where t = circuit repetitions (depth = 2 in our project):\n\n"
        "1. Hadamard Layer (H^⊗n):\n"
        "   Places all n qubits into uniform superposition:\n"
        "   H|0⟩ = (|0⟩ + |1⟩) / √2\n\n"
        "2. Single-Qubit Rotations (Phase Gates):\n"
        "   Encodes individual feature values:\n"
        "   exp( i ∑ x_i Z_i )   where Z_i is Pauli-Z gate\n\n"
        "3. Two-Qubit Entangling ZZ Gates:\n"
        "   Creates quantum entanglement between adjacent qubits:\n"
        "   exp( i ∑_{i<j} (π - x_i)(π - x_j) Z_i Z_j )\n\n"
        "Implemented on hardware via:\n"
        "   CNOT(i, j) ── R_z(2(π - x_i)(π - x_j)) ── CNOT(i, j)"
    )
    p_zz = c6_2.add_paragraph()
    p_zz.text = zz_text
    p_zz.font.size = Pt(11)
    p_zz.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 7: Part 3 - Two Principal QSVM Paradigms
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Part 3: QSVM Paradigms", "Two Principal Formulations of QSVM in Literature", "Comparing the fault-tolerant HHL linear-algebraic approach vs the NISQ-ready hybrid kernel estimation.")

    c7_1 = add_card(s7, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0), "Paradigm 1: HHL-Based Least Squares QSVM", AMBER)
    hhl_text = (
        "Author: Rebentrost, Mohseni, Lloyd (Phys. Rev. Lett., 2014)\n\n"
        "Core Philosophy:\n"
        "• Recasts Least-Squares SVM (Suykens & Vandewalle, 1999) as a system of linear equations:\n"
        "     [ 0    1^T       ] [ b ]   [ 0 ]\n"
        "     [ 1  K + γ⁻¹ I   ] [ α ] = [ y ]\n\n"
        "• Solves the linear system Ax = b using the HHL quantum matrix inversion algorithm.\n\n"
        "Theoretical Runtime:\n"
        "• O( log(NM) × poly(κ, 1/ε) ) — Exponential speedup in training data size M and features N!\n\n"
        "Real-World Limitations:\n"
        "• Requires Quantum RAM (QRAM) for coherent data loading.\n"
        "• Requires low matrix condition number κ and fault tolerance.\n"
        "• Solution vector α is encoded in quantum amplitudes; reading out full vector takes O(M) time."
    )
    p_hhl = c7_1.add_paragraph()
    p_hhl.text = hhl_text
    p_hhl.font.size = Pt(10.5)
    p_hhl.font.color.rgb = TEXT_WHITE

    c7_2 = add_card(s7, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0), "Paradigm 2: Quantum Kernel Estimation (Our Choice)", CYAN)
    qke_text = (
        "Authors: Havlíček et al. (Nature, 2019) & Schuld & Killoran (PRL, 2019)\n\n"
        "Core Philosophy (Hybrid Quantum-Classical):\n"
        "• Quantum processor acts as an accelerator specifically for kernel evaluation.\n"
        "• Classical computer carries out the convex SVM optimization.\n\n"
        "Step-by-Step Architecture:\n"
        "1. Classical Preprocessing: Clean, scale features to [0, π].\n"
        "2. Quantum Kernel Matrix Estimation: Run parameterised circuit U_φ†(x_i) U_φ(x_j) to fill Gram matrix K.\n"
        "3. Classical Optimization: Standard QP solver finds support vectors α_i and bias b.\n"
        "4. Quantum-Assisted Inference: Compute kernel overlap against support vectors for new test points.\n\n"
        "Why This is the Gold Standard for NISQ:\n"
        "• Requires NO QRAM.\n"
        "• Shallow circuit depth (NISQ hardware friendly).\n"
        "• Guaranteed convex global optimum (no barren plateaus)."
    )
    p_qke = c7_2.add_paragraph()
    p_qke.text = qke_text
    p_qke.font.size = Pt(10.5)
    p_qke.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 8: Part 3 - Quantum Kernel Estimation Circuit
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Part 3: QSVM Circuit Architecture", "The Compute-Uncompute Kernel Estimation Circuit", "Direct overlap measurement via inversion testing without ancilla qubits.")

    c8_1 = add_card(s8, Inches(0.8), Inches(1.9), Inches(6.5), Inches(5.0), "Circuit Operation & Quantum Mechanics", INDIGO)
    circ_text = (
        "Compute-Uncompute (Inversion Test) Architecture:\n\n"
        "|0⟩ ───[  U_φ(x_j)  ]───[  U_φ†(x_i)  ]───[ ∡ Measure ] ──> c_0\n"
        "|0⟩ ───[  U_φ(x_j)  ]───[  U_φ†(x_i)  ]───[ ∡ Measure ] ──> c_1\n"
        "|0⟩ ───[  U_φ(x_j)  ]───[  U_φ†(x_i)  ]───[ ∡ Measure ] ──> c_2\n"
        "|0⟩ ───[  U_φ(x_j)  ]───[  U_φ†(x_i)  ]───[ ∡ Measure ] ──> c_3\n\n"
        "How the Measurement Works:\n"
        "1. The register is initialized to ground state |0000⟩.\n"
        "2. U_φ(x_j) encodes sample x_j into quantum state |ψ(x_j)⟩.\n"
        "3. Inverse unitary U_φ†(x_i) transforms the state by the adjoint of sample x_i.\n"
        "4. All qubits are measured in the computational basis.\n"
        "5. If x_i == x_j, U_φ†(x_i) U_φ(x_j) = Identity (I), returning to |0000⟩ with 100% probability!\n"
        "6. In general: P(|00...0⟩) = |⟨0| U_φ†(x_i) U_φ(x_j) |0⟩|² = k(x_i, x_j)."
    )
    p_ct = c8_1.add_paragraph()
    p_ct.text = circ_text
    p_ct.font.size = Pt(11)
    p_ct.font.name = "Courier New"
    p_ct.font.color.rgb = TEXT_WHITE

    c8_2 = add_card(s8, Inches(7.6), Inches(1.9), Inches(4.9), Inches(5.0), "Advantages over Swap Test", EMERALD)
    swap_comp = (
        "Inversion Test vs SWAP Test Comparison:\n\n"
        "• Qubit Requirements:\n"
        "  - SWAP Test: Needs 2n + 1 qubits (requires two data registers + 1 ancilla qubit).\n"
        "  - Inversion Test: Needs ONLY n qubits! 50% fewer qubits required.\n\n"
        "• Circuit Complexity:\n"
        "  - SWAP Test requires controlled-SWAP (Fredkin) gates, which decompose into expensive 3-qubit gates.\n"
        "  - Inversion Test uses zero ancillas and simple single-qubit basis measurements.\n\n"
        "• Statistical Measurement Shots:\n"
        "  - In shot-based sampling, measuring s shots gives an empirical frequency k_hat.\n"
        "  - Statistical error scales as O(1 / √s).\n"
        "  - For ε = 0.01 precision, s ≈ 10,000 shots per entry."
    )
    p_sc = c8_2.add_paragraph()
    p_sc.text = swap_comp
    p_sc.font.size = Pt(11)
    p_sc.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 9: Part 4 - Project Application: Stock Market Trend Direction
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Part 4: Real-World Financial Engineering", "Project Application: Stock Market Trend Direction Classification", "Formulating next-day equity price movement as a quantum-enhanced supervised learning problem.")

    c9_1 = add_card(s9, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0), "Problem Formulation & Ground Truth", CYAN)
    prob_text = [
        ("The Financial Question:", "Can quantum feature spaces detect non-linear regime shifts and momentum dependencies that classical RBF kernels overlook?"),
        ("Binary Classification Objective:", "Predict whether the closing price of a stock on day (t + 1) will be higher or lower than day (t):"),
        ("Ground-Truth Label:", "• Label = 1 (UP): Close(t+1) > Close(t)\n• Label = 0 (DOWN): Close(t+1) <= Close(t)"),
        ("Live Data Sourcing:", "5 years of historical OHLCV (Open, High, Low, Close, Volume) data pulled dynamically via Yahoo Finance API (`yfinance`)."),
        ("Covered Markets in Our App:", "• Indian Market (NSE): Reliance Industries, TCS, HDFC Bank, SBI, Infosys, ITC, Bharti Airtel, L&T, etc.\n• US Market (NASDAQ/NYSE): Apple, Microsoft, NVIDIA, Google, Amazon, Tesla.")
    ]
    for h, b in prob_text:
        p = c9_1.add_paragraph()
        p.text = f"{h} "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p_sub = c9_1.add_paragraph()
        p_sub.text = b
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(6)

    c9_2 = add_card(s9, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0), "Financial Time Series Challenges", ROSE)
    fin_challenges = (
        "Intrinsic Characteristics of Market Data:\n\n"
        "1. Low Signal-to-Noise Ratio (SNR):\n"
        "   Unlike medical or physical datasets with clean deterministic boundaries, daily market fluctuations contain substantial Brownian random walk noise.\n\n"
        "2. Non-Stationarity:\n"
        "   Statistical distributions shift over time across market regimes (bull, bear, volatile consolidation).\n\n"
        "3. The 'Coin-Toss' Reality (50–55% Baseline):\n"
        "   In quantitative finance, predicting directional moves with >55% out-of-sample accuracy is considered institutional-grade. A naive model guessing the majority class achieves ~52-54%.\n\n"
        "4. No Data Leakage Requirement:\n"
        "   Time series CANNOT be randomly shuffled (k-fold CV fails due to look-ahead bias). Testing must be strictly chronological."
    )
    p_fc = c9_2.add_paragraph()
    p_fc.text = fin_challenges
    p_fc.font.size = Pt(11)
    p_fc.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 10: Part 4 - Feature Engineering & [0, π] Scaling
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Part 4: Data Preprocessing", "Feature Engineering & The Crucial [0, π] Quantum Scaling", "Extracting 4 technical indicators and mapping them cleanly to quantum rotation angles.")

    c10_1 = add_card(s10, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0), "4 Classical Technical Indicators", INDIGO)
    features_list = [
        ("1. RSI (14-Day Relative Strength Index):", "Measures price velocity and momentum. Computes ratio of average gains to average losses over a 14-day rolling window to detect overbought (>70) or oversold (<30) conditions."),
        ("2. MACD Histogram:", "Difference between the MACD Line (12-day EMA − 26-day EMA) and its 9-day EMA signal line. Captures trend acceleration and divergence."),
        ("3. Moving Average Ratio (Close / SMA(20)):", "Relative ratio of current closing price to its 20-day Simple Moving Average. Quantifies short-term mean-reversion pull."),
        ("4. Daily Volume % Change:", "(Volume_t - Volume_{t-1}) / Volume_{t-1}. Captures institutional liquidity shocks and breakout confirmations.")
    ]
    for h, b in features_list:
        p = c10_1.add_paragraph()
        p.text = f"{h} "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p_sub = c10_1.add_paragraph()
        p_sub.text = b
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(6)

    c10_2 = add_card(s10, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0), "Leakage-Free Chronological Split & [0, π] Scaling", AMBER)
    scaling_info = (
        "Dataset Split Strategy (350 Trading Days):\n"
        "• Training Set: First 250 days chronologically.\n"
        "• Out-of-Sample Test Set: Last 100 days chronologically.\n"
        "• Zero Shuffling: Preserves the arrow of time.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Why Scale Specifically to [0, π]? (Crucial Insight)\n\n"
        "• Quantum gates like R_z(θ) and P(θ) apply unitary rotations:\n"
        "     R_z(θ) = diag( e^{-iθ/2},  e^{iθ/2} )\n\n"
        "• These rotations are periodic with period 2π:\n"
        "     R_z(0) == R_z(2π) == Identity\n\n"
        "• If features are unscaled or scaled to standard [0, 1] or arbitrary ranges, phase wrapping (aliasing) occurs: extreme high values wrap to match extreme low values!\n\n"
        "• Scaling strictly to [0, π] ensures monotonic angular separation on the Bloch sphere with NO phase wrapping.\n\n"
        "• IMPORTANT: MinMaxScaler is fitted ONLY on training set to prevent look-ahead data leakage!"
    )
    p_sc = c10_2.add_paragraph()
    p_sc.text = scaling_info
    p_sc.font.size = Pt(10.5)
    p_sc.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 11: Part 5 - 4-Qubit Circuit Implementation
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Part 5: Quantum Circuit Implementation", "4-Qubit Circuit Mapping for Stock Indicators", "Detailed gate construction for the 4 technical features into a 16-dimensional Hilbert space.")

    c11_1 = add_card(s11, Inches(0.8), Inches(1.9), Inches(6.0), Inches(5.0), "Qubit-to-Feature Allocation", CYAN)
    alloc_text = (
        "4-Qubit Register Mapping:\n\n"
        "• Qubit 0 (q_0) <──> x_0 : Normalized RSI (14-day)\n"
        "• Qubit 1 (q_1) <──> x_1 : Normalized MACD Histogram\n"
        "• Qubit 2 (q_2) <──> x_2 : Normalized MA Ratio (Close/SMA20)\n"
        "• Qubit 3 (q_3) <──> x_3 : Normalized Daily Volume Change\n\n"
        "Linear Nearest-Neighbor Entanglement Topology:\n"
        "Instead of all-to-all entanglement (which requires dense CNOT routing and high cross-talk noise), we employ linear hardware connectivity:\n\n"
        "Pair 1: (q_0, q_1) ── Entangles RSI with MACD Momentum\n"
        "Pair 2: (q_1, q_2) ── Entangles MACD with Trend Deviation\n"
        "Pair 3: (q_2, q_3) ── Entangles Trend Deviation with Volume\n\n"
        "This mirrors physical hardware couplings on modern IBM Quantum superconducting processors."
    )
    p_al = c11_1.add_paragraph()
    p_al.text = alloc_text
    p_al.font.size = Pt(11)
    p_al.font.color.rgb = TEXT_WHITE

    c11_2 = add_card(s11, Inches(7.1), Inches(1.9), Inches(5.4), Inches(5.0), "Circuit Depth & Gate Breakdown", INDIGO)
    depth_text = (
        "Per-Repetition Circuit Specification:\n\n"
        "1. Superposition:\n"
        "   H gates on q_0, q_1, q_2, q_3 (4 single-qubit gates)\n\n"
        "2. Single-Qubit Phase Encoding:\n"
        "   P(2x_0), P(2x_1), P(2x_2), P(2x_3) (4 phase gates)\n\n"
        "3. Linear ZZ Interaction Blocks (3 pairs):\n"
        "   For each adjacent pair (i, i+1):\n"
        "   • CNOT(q_i, q_{i+1})\n"
        "   • P(2(π - x_i)(π - x_{i+1})) on target qubit\n"
        "   • CNOT(q_i, q_{i+1})\n"
        "   Total: 6 CNOT gates + 3 Phase gates per layer.\n\n"
        "Total Circuit Depth for 2 Repetitions:\n"
        "• Total Single-Qubit Gates: 16 gates\n"
        "• Total Two-Qubit CNOT Gates: 12 gates\n"
        "• Feature Space Dimension: 2^4 = 16 dimensions"
    )
    p_dp = c11_2.add_paragraph()
    p_dp.text = depth_text
    p_dp.font.size = Pt(11)
    p_dp.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 12: Part 5 - Engineering Optimization: 700x Speedup
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Part 5: Engineering Innovation", "Simulation Optimization: Achieving a 700× Speedup", "Replacing naive sequential circuit sampling with exact vectorized statevector Hermitian inner products.")

    c12_1 = add_card(s12, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0), "The Naive Qiskit Bottleneck", ROSE)
    bottleneck_text = (
        "The Problem with Standard Qiskit ComputeUncompute:\n\n"
        "• To compute the 250×250 training Gram matrix:\n"
        "  - Number of unique pairs = 250 × 249 / 2 = 31,125 pairs!\n"
        "• To compute the 100×250 testing Gram matrix:\n"
        "  - Number of test pairs = 100 × 250 = 25,000 pairs!\n"
        "• Total Individual Circuit Executions: >56,000 circuits!\n\n"
        "Why It Timed Out:\n"
        "1. Standard Qiskit constructed, bound parameters, and\n"
        "   simulated each of the 56,000 circuits sequentially in Python.\n"
        "2. Python interpreter overhead dominated execution.\n"
        "3. Calculation took >5 minutes, triggering server timeouts!\n"
        "4. In addition, shot-based sampling introduced statistical noise."
    )
    p_bn = c12_1.add_paragraph()
    p_bn.text = bottleneck_text
    p_bn.font.size = Pt(11)
    p_bn.font.color.rgb = TEXT_WHITE

    c12_2 = add_card(s12, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0), "Our Vectorized Statevector Solution", EMERALD)
    solution_text = (
        "Our Mathematical Realization:\n\n"
        "For 4 qubits, statevector |ψ(x)⟩ is a complex vector of length 16.\n"
        "The quantum fidelity is identically the Hermitian inner product:\n"
        "      k(x_i, x_j) = |⟨ψ(x_i) | ψ(x_j)⟩|²\n\n"
        "Our 3-Step Vectorized Pipeline:\n"
        "1. Compute the 250 statevectors ONCE (Takes ~0.3s):\n"
        "   Ψ_train matrix shape: (250, 16)\n\n"
        "2. Compute Entire Gram Matrix via NumPy BLAS:\n"
        "   K_train = | Ψ_train · Ψ_train^† |²   (Takes ~0.005s!)\n"
        "   K_test  = | Ψ_test  · Ψ_train^† |²   (Takes ~0.002s!)\n\n"
        "Result:\n"
        "• Total Runtime dropped from >5 minutes to 0.4 seconds!\n"
        "• Over 700× speedup with EXACT zero-shot-noise fidelity!\n"
        "• Passed as precomputed kernel into SVC(kernel='precomputed')."
    )
    p_sol = c12_2.add_paragraph()
    p_sol.text = solution_text
    p_sol.font.size = Pt(11)
    p_sol.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 13: Part 6 - Empirical Results & Head-to-Head Comparison
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Part 6: Results & Evaluation", "Empirical Results: Quantum SVM vs Classical RBF SVM", "Head-to-head comparison across 100 out-of-sample trading days on Indian and US equities.")

    c13_1 = add_card(s13, Inches(0.8), Inches(1.9), Inches(6.0), Inches(5.0), "Experimental Results Table (Representative Equities)", CYAN)
    res_text = (
        "Performance on Representative Equities (100 Test Days):\n\n"
        "1. Reliance Industries Limited (RELIANCE.NS):\n"
        "   • Quantum SVM (QSVC):  Accuracy = 41.0% | F1 = 35.2%\n"
        "   • Classical SVM (RBF): Accuracy = 54.0% | F1 = 58.2%\n"
        "   • Blind Guess Baseline: 52.0% (Majority UP)\n\n"
        "2. Apple Inc. (AAPL):\n"
        "   • Quantum SVM (QSVC):  Accuracy = 50.0% | F1 = 59.7%\n"
        "   • Classical SVM (RBF): Accuracy = 57.0% | F1 = 68.6%\n"
        "   • Blind Guess Baseline: 54.0% (Majority UP)\n\n"
        "3. NVIDIA Corporation (NVDA):\n"
        "   • Quantum SVM (QSVC):  Accuracy = 51.0% | F1 = 49.5%\n"
        "   • Classical SVM (RBF): Accuracy = 53.0% | F1 = 51.0%\n"
        "   • Blind Guess Baseline: 53.0% (Majority DOWN)\n\n"
        "Observation:\n"
        "Both models hover around the 50-55% baseline, consistent with financial market efficiency theory."
    )
    p_res = c13_1.add_paragraph()
    p_res.text = res_text
    p_res.font.size = Pt(11)
    p_res.font.color.rgb = TEXT_WHITE

    c13_2 = add_card(s13, Inches(7.1), Inches(1.9), Inches(5.4), Inches(5.0), "In-Depth Academic Analysis", AMBER)
    analysis_text = (
        "Why Did Classical SVM Edge Ahead in Some Stocks?\n\n"
        "1. Regularization & Noise Handling:\n"
        "   Financial data has a very low signal-to-noise ratio.\n"
        "   Classical RBF's Euclidean distance metric provides\n"
        "   strong local regularization, creating smooth decision\n"
        "   boundaries that naturally resist overfitting noisy candles.\n\n"
        "2. Feature Map Expressivity vs Generalization:\n"
        "   The 4-qubit ZZFeatureMap creates complex non-linear\n"
        "   phase interference patterns in 16D space. On noisy\n"
        "   stock data, high expressivity without specialized inductive\n"
        "   bias can model the noise rather than the signal.\n\n"
        "3. Quantum Advantage Preconditions:\n"
        "   Consistent with Huang et al. (Nature Comm., 2021),\n"
        "   quantum kernels demonstrate advantage when data\n"
        "   originates from quantum physical processes or discrete\n"
        "   algebraic structures, rather than classical time series."
    )
    p_an = c13_2.add_paragraph()
    p_an.text = analysis_text
    p_an.font.size = Pt(11)
    p_an.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 14: Part 6 - Interactive Web Application Architecture
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Part 6: Full-Stack Engineering", "Interactive Web Application: Live Deployment", "Full-stack software deployment connecting Qiskit with Streamlit & React on cloud infrastructure.")

    arch_cards = [
        ("1. Streamlit Full-Stack UI", "Built an interactive research dashboard in Streamlit & Python, featuring full company names (no shortforms), dark mode capstone styling, and Plotly graphics.", CYAN),
        ("2. Interactive 100-Day Chart", "Displays real daily stock prices in ₹ (INR) or $ (USD) with dynamic green prediction dots for correct next-day calls and red dots for mistakes, with model toggling.", INDIGO),
        ("3. 30×30 Quantum Heatmap", "Interactive visualization of the 30×30 training Gram matrix, displaying pairwise quantum state fidelities with cell inspection on hover (diagonal = 1.0).", EMERALD),
        ("4. Cloud Deployment (Render & GitHub)", "Deployed live on Render Cloud Web Service with pinned Python 3.11.9, open CORS, and full GitHub version control (repo: SANYAM-MANIT/quantum-stock-classifier).", AMBER)
    ]

    for idx, (title, desc, col) in enumerate(arch_cards):
        x = Inches(0.8 + (idx % 2) * 5.9)
        y = Inches(1.9 + (idx // 2) * 2.5)
        tf = add_card(s14, x, y, Inches(5.6), Inches(2.2), title, col)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 15: Limitations, Challenges & Future Scope
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "Critical Analysis & Future Scope", "Limitations in the NISQ Era & Future Research Horizons", "Acknowledging hardware hurdles and outlining promising extensions for practical quantum advantage.")

    c15_1 = add_card(s15, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0), "NISQ Hardware Limitations", ROSE)
    lim_points = (
        "1. Decoherence & Gate Noise:\n"
        "   Modern NISQ processors have 2-qubit CNOT gate error rates of 10⁻² to 10⁻³. Inversion tests suffer error accumulation as circuit depth grows.\n\n"
        "2. Statistical Shot Noise:\n"
        "   Estimating each kernel entry via measurement introduces error O(1/√s). For large datasets (M samples), M(M-1)/2 entries require millions of shots!\n\n"
        "3. Exponential Kernel Concentration:\n"
        "   Thanasilp et al. (2022) showed that as qubit count n grows, expressive quantum kernels concentrate exponentially around a constant value, destroying trainability.\n\n"
        "4. Classical Dequantization:\n"
        "   Tang (2019) demonstrated that classical sampling algorithms can match many claimed exponential quantum linear algebra speedups."
    )
    p_lim = c15_1.add_paragraph()
    p_lim.text = lim_points
    p_lim.font.size = Pt(11)
    p_lim.font.color.rgb = TEXT_WHITE

    c15_2 = add_card(s15, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0), "Future Research Horizons", CYAN)
    fut_points = (
        "1. Trainable Quantum Kernels (Kernel Alignment):\n"
        "   Instead of static ZZ parameters, optimize unitary gate rotation angles to maximize alignment with training target labels y_i y_j.\n\n"
        "2. Problem-Informed Inductive Biases:\n"
        "   Designing feature maps specifically tailored to time series and multi-asset correlation structures (Kübler et al., NeurIPS 2021) to prevent kernel concentration.\n\n"
        "3. Fault-Tolerant Scaling (HHL Realization):\n"
        "   As surface codes and logical qubits mature, implement true HHL matrix inversion with QRAM for logarithmic O(log(NM)) runtime.\n\n"
        "4. Multi-Asset Cross-Entropy Classification:\n"
        "   Expanding from single-stock direction to multi-qubit cross-asset portfolio optimization and regime detection."
    )
    p_fut = c15_2.add_paragraph()
    p_fut.text = fut_points
    p_fut.font.size = Pt(11)
    p_fut.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 16: Summary, References & Conclusion
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "Conclusion", "Project Summary & Key References", "Final conclusions from the MANIT CSE Minor Project.")

    c16_1 = add_card(s16, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0), "Key Takeaways & Contributions", EMERALD)
    conc_text = (
        "Key Project Contributions:\n\n"
        "• Successfully built a full-stack quantum machine learning application benchmarking QSVM against Classical RBF SVM.\n\n"
        "• Engineered a 700× vectorized statevector kernel optimization, reducing simulation latency from >5 minutes to 0.4 seconds.\n\n"
        "• Addressed real-world financial data with zero-leakage chronological train/test splits and [0, π] phase scaling.\n\n"
        "• Implemented support for Indian (NSE) and US equities with live Yahoo Finance integration and interactive Streamlit UI.\n\n"
        "• Confirmed that for low-SNR financial data, quantum kernels explore rich Hilbert spaces but classical RBF provides strong noise resistance."
    )
    p_conc = c16_1.add_paragraph()
    p_conc.text = conc_text
    p_conc.font.size = Pt(11)
    p_conc.font.color.rgb = TEXT_WHITE

    c16_2 = add_card(s16, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0), "Primary Academic References", INDIGO)
    refs_text = (
        "Core References:\n\n"
        "[1] Cortes, C. & Vapnik, V. (1995). Support-Vector Networks. Machine Learning, 20(3): 273–297.\n\n"
        "[2] Rebentrost, P., Mohseni, M. & Lloyd, S. (2014). Quantum Support Vector Machine for Big Data Classification. Phys. Rev. Lett., 113: 130503.\n\n"
        "[3] Havlíček, V. et al. (2019). Supervised Learning with Quantum-Enhanced Feature Spaces. Nature, 567: 209–212.\n\n"
        "[4] Schuld, M. & Killoran, N. (2019). Quantum Machine Learning in Feature Hilbert Spaces. Phys. Rev. Lett., 122: 040504.\n\n"
        "[5] Huang, H.-Y. et al. (2021). Power of Data in Quantum Machine Learning. Nature Communications, 12: 2631.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Thank You! Questions & Discussion."
    )
    p_refs = c16_2.add_paragraph()
    p_refs.text = refs_text
    p_refs.font.size = Pt(10.5)
    p_refs.font.color.rgb = TEXT_WHITE

    output_path = "/Users/sanyamjain/Downloads/quantum-stock-classifier/Quantum_SVM_Stock_Market_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    create_deck()
