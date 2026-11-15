import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from data import fetch_and_prepare_data
from models import run_comparison_pipeline

# ---------------------------------------------------------
# Page Configuration & Dark Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="QuantumTrade Lab | Stock QSVM",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, human-crafted college capstone styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 1.2rem;
    }
    .project-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        background-color: rgba(99, 102, 241, 0.15);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
    }
    .metric-title {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
    }
    .metric-val {
        font-size: 1.6rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }
    .callout-box {
        background-color: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.85rem;
        color: #fde68a;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Curated Stock Lists with Actual Full Names (No Shortforms)
# ---------------------------------------------------------
INDIAN_STOCKS = {
    "Reliance Industries Limited": {"symbol": "RELIANCE.NS", "sector": "Energy & Telecom"},
    "Tata Consultancy Services (TCS)": {"symbol": "TCS.NS", "sector": "IT Services"},
    "HDFC Bank Limited": {"symbol": "HDFCBANK.NS", "sector": "Banking"},
    "Infosys Limited": {"symbol": "INFY.NS", "sector": "IT Services"},
    "ICICI Bank Limited": {"symbol": "ICICIBANK.NS", "sector": "Banking"},
    "State Bank of India (SBI)": {"symbol": "SBIN.NS", "sector": "Public Sector Bank"},
    "Bharti Airtel Limited": {"symbol": "BHARTIARTL.NS", "sector": "Telecom"},
    "ITC Limited": {"symbol": "ITC.NS", "sector": "Consumer Goods"},
    "Larsen & Toubro Limited (L&T)": {"symbol": "LT.NS", "sector": "Infrastructure"},
    "Hindustan Unilever Limited": {"symbol": "HINDUNILVR.NS", "sector": "FMCG"},
    "Bajaj Finance Limited": {"symbol": "BAJFINANCE.NS", "sector": "Financial Services"},
    "Maruti Suzuki India Limited": {"symbol": "MARUTI.NS", "sector": "Automotive"},
    "Titan Company Limited": {"symbol": "TITAN.NS", "sector": "Consumer & Luxury"},
    "Sun Pharmaceutical Industries": {"symbol": "SUNPHARMA.NS", "sector": "Healthcare"},
    "Wipro Limited": {"symbol": "WIPRO.NS", "sector": "IT Services"},
    "Kotak Mahindra Bank": {"symbol": "KOTAKBANK.NS", "sector": "Banking"},
    "Tata Consumer Products": {"symbol": "TATACONSUM.NS", "sector": "Consumer Goods"}
}

US_STOCKS = {
    "Apple Inc.": {"symbol": "AAPL", "sector": "Consumer Tech"},
    "Microsoft Corporation": {"symbol": "MSFT", "sector": "Software & Cloud"},
    "NVIDIA Corporation": {"symbol": "NVDA", "sector": "Semiconductors & AI"},
    "Alphabet Inc. (Google)": {"symbol": "GOOGL", "sector": "Internet & Search"},
    "Amazon.com Inc.": {"symbol": "AMZN", "sector": "E-Commerce & Cloud"},
    "Tesla Inc.": {"symbol": "TSLA", "sector": "Electric Vehicles"}
}


# ---------------------------------------------------------
# Cached Computation Engine
# ---------------------------------------------------------
@st.cache_data(show_spinner=False, ttl=3600)
def get_prediction_results(ticker_symbol: str):
    """Fetches real historical market data and runs QSVM vs Classical SVM comparison."""
    df_recent = fetch_and_prepare_data(ticker_symbol)
    results = run_comparison_pipeline(df_recent, ticker_symbol)
    return results


# ---------------------------------------------------------
# Sidebar Controls & Stock Selection
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Select Market & Company")
    market_choice = st.radio(
        "Market Category",
        ["🇮🇳 Indian Equities (NSE)", "🇺🇸 US Equities (NASDAQ/NYSE)", "🔍 Custom Stock Ticker"],
        index=0
    )

    selected_ticker = ""
    company_display_name = ""
    sector_name = ""
    is_indian = False

    if market_choice == "🇮🇳 Indian Equities (NSE)":
        is_indian = True
        company_display_name = st.selectbox(
            "Select Company (Full Official Name)",
            options=list(INDIAN_STOCKS.keys()),
            index=0
        )
        selected_ticker = INDIAN_STOCKS[company_display_name]["symbol"]
        sector_name = INDIAN_STOCKS[company_display_name]["sector"]

    elif market_choice == "🇺🇸 US Equities (NASDAQ/NYSE)":
        is_indian = False
        company_display_name = st.selectbox(
            "Select Company (Full Official Name)",
            options=list(US_STOCKS.keys()),
            index=0
        )
        selected_ticker = US_STOCKS[company_display_name]["symbol"]
        sector_name = US_STOCKS[company_display_name]["sector"]

    else:
        custom_sym = st.text_input("Enter Ticker Symbol", value="INFY.NS").strip().upper()
        selected_ticker = custom_sym
        company_display_name = custom_sym
        sector_name = "Custom Asset"
        is_indian = custom_sym.endswith(".NS") or custom_sym.endswith(".BO")

    currency_symbol = "₹" if is_indian else "$"

    st.markdown("---")
    st.markdown(
        f"""
        **Selected Stock Info:**
        - **Ticker:** `{selected_ticker}`
        - **Sector:** {sector_name}
        - **Currency:** {currency_symbol} ({'INR' if is_indian else 'USD'})
        - **Data Feed:** Yahoo Finance (5-Year Daily OHLCV)
        """
    )
    st.markdown("---")
    st.markdown(
        """
        **B.Tech Capstone Project**  
        *Department of Computer Science & Engineering*  
        Built using Qiskit 1.4, Scikit-learn, and Streamlit.
        """
    )

# ---------------------------------------------------------
# Main Page Header
# ---------------------------------------------------------
st.markdown('<span class="project-badge">College Capstone Project Demo</span>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">QuantumTrade Lab: Quantum Stock Trend Classifier</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Comparative Analysis of a <strong>4-Qubit Quantum Support Vector Machine (QSVM)</strong> '
    'against a <strong>Classical RBF-Kernel SVM</strong> on real stock price movements.</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="callout-box">'
    '<strong>💡 Friendly Student Note:</strong> Stock market prices have substantial daily random noise. Real next-day prediction '
    'accuracy typically hovers near 50–55% (like a coin flip). This project explores how 4-qubit quantum statevector '
    'feature maps compare to classical machine learning on financial time series, not for financial trading.'
    '</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Run Model & Fetch Data
# ---------------------------------------------------------
if not selected_ticker:
    st.warning("Please choose or enter a valid stock ticker symbol.")
    st.stop()

with st.spinner(f"Fetching real market prices and running quantum simulation for {company_display_name}..."):
    try:
        data = get_prediction_results(selected_ticker)
    except Exception as e:
        st.error(f"Error fetching data or running simulation for {selected_ticker}: {str(e)}")
        st.stop()

# Extract Results
qsvm = data["qsvm"]
svm = data["svm"]
baseline = data["majority_baseline"]
balance = data["class_balance"]
prices = data["recent_prices"]
kernel_mat = np.array(data["kernel_matrix_30x30"])
latest_close = prices[-1]["close"]

# ---------------------------------------------------------
# Overview Cards & Head-to-Head Banner
# ---------------------------------------------------------
col_info1, col_info2, col_info3 = st.columns([2, 1, 1])
with col_info1:
    st.subheader(f"📊 {company_display_name}")
    st.caption(f"Ticker: {selected_ticker} • Sector: {sector_name} • 350 Total Trading Days (250 Train / 100 Out-of-Sample Test)")
with col_info2:
    st.metric(label="Latest Close Price", value=f"{currency_symbol}{latest_close:,.2f}")
with col_info3:
    st.metric(label="Market UP Trend (Test)", value=f"{balance['test_up_pct']*100:.1f}%", help="Percentage of the 100 test days that closed UP")

st.markdown("---")

# Winner Determination
q_acc = qsvm["accuracy"] * 100
c_acc = svm["accuracy"] * 100
diff = abs(q_acc - c_acc)

if q_acc > c_acc:
    st.success(f"🏆 **Model Showdown Winner:** **Quantum SVM** edged ahead by **+{diff:.1f}% accuracy** on {company_display_name} ({q_acc:.1f}% vs {c_acc:.1f}%).")
elif c_acc > q_acc:
    st.info(f"🏆 **Model Showdown Winner:** **Classical SVM** achieved **+{diff:.1f}% higher accuracy** on {company_display_name} ({c_acc:.1f}% vs {q_acc:.1f}%).")
else:
    st.info(f"🤝 **Model Showdown:** Both Quantum and Classical models achieved **identical accuracy ({q_acc:.1f}%)** on {company_display_name}.")

# Metric Columns
mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)
with mcol1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Quantum Accuracy</div>'
        f'<div class="metric-val" style="color: #818cf8;">{q_acc:.1f}%</div></div>',
        unsafe_allow_html=True
    )
with mcol2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Classical Accuracy</div>'
        f'<div class="metric-val" style="color: #34d399;">{c_acc:.1f}%</div></div>',
        unsafe_allow_html=True
    )
with mcol3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Blind Guess Baseline</div>'
        f'<div class="metric-val" style="color: #fbbf24;">{baseline*100:.1f}%</div></div>',
        unsafe_allow_html=True
    )
with mcol4:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Quantum F1 Score</div>'
        f'<div class="metric-val" style="color: #c084fc;">{qsvm["f1"]*100:.1f}%</div></div>',
        unsafe_allow_html=True
    )
with mcol5:
    st.markdown(
        f'<div class="metric-card"><div class="metric-title">Quantum Run Time</div>'
        f'<div class="metric-val" style="color: #38bdf8;">{qsvm["training_time"]:.2f}s</div></div>',
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Interactive Tabbed Visualizations
# ---------------------------------------------------------
tab_chart, tab_acc, tab_matrix, tab_heatmap, tab_methodology = st.tabs([
    "📈 Daily Prices & Next-Day Hits",
    "📊 Accuracy Benchmark",
    "🎯 Scorecards (Confusion Matrix)",
    "🧬 30x30 Quantum Similarity Heatmap",
    "🔬 Project Methodology & Circuit"
])

# ---------------------------------------------------------
# Tab 1: Interactive Price & Prediction Chart
# ---------------------------------------------------------
with tab_chart:
    st.markdown("#### Test Set Closing Prices & Directional Predictions (Last 100 Days)")
    st.caption("Each point represents one trading day. 🟢 **Green marker** = Model guessed right • 🔴 **Red marker** = Model guessed wrong.")

    chart_model = st.radio(
        "Display Prediction Markers For:",
        ["Quantum SVM (QSVC)", "Classical SVM (RBF)"],
        horizontal=True
    )
    is_q_active = (chart_model == "Quantum SVM (QSVC)")

    df_plot = pd.DataFrame(prices)
    df_plot["correct"] = df_plot["qsvm_correct"] if is_q_active else df_plot["svm_correct"]
    df_plot["pred_label"] = df_plot["qsvm_pred"] if is_q_active else df_plot["svm_pred"]
    df_plot["pred_text"] = df_plot["pred_label"].apply(lambda x: "UP 📈" if x == 1 else "DOWN 📉")
    df_plot["actual_text"] = df_plot["actual_label"].apply(lambda x: "UP 📈" if x == 1 else "DOWN 📉")
    df_plot["status"] = df_plot["correct"].apply(lambda x: "Correct Prediction ✅" if x else "Wrong Prediction ❌")

    fig_price = go.Figure()

    # Price Line
    fig_price.add_trace(go.Scatter(
        x=df_plot["date"],
        y=df_plot["close"],
        mode="lines",
        name="Closing Price",
        line=dict(color="#94a3b8", width=2),
        hoverinfo="skip"
    ))

    # Correct points (Green)
    df_correct = df_plot[df_plot["correct"] == True]
    fig_price.add_trace(go.Scatter(
        x=df_correct["date"],
        y=df_correct["close"],
        mode="markers",
        name="Correct Guess (Green)",
        marker=dict(color="#10b981", size=8, line=dict(color="#0f172a", width=1.5)),
        customdata=np.stack((df_correct["actual_text"], df_correct["pred_text"], df_correct["status"]), axis=-1),
        hovertemplate="<b>Date:</b> %{x}<br><b>Price:</b> " + currency_symbol + "%{y:.2f}<br><b>Actual Next Day:</b> %{customdata[0]}<br><b>Predicted:</b> %{customdata[1]}<br><span style='color:#10b981'>%{customdata[2]}</span><extra></extra>"
    ))

    # Wrong points (Red)
    df_wrong = df_plot[df_plot["correct"] == False]
    fig_price.add_trace(go.Scatter(
        x=df_wrong["date"],
        y=df_wrong["close"],
        mode="markers",
        name="Wrong Guess (Red)",
        marker=dict(color="#f43f5e", size=8, line=dict(color="#0f172a", width=1.5)),
        customdata=np.stack((df_wrong["actual_text"], df_wrong["pred_text"], df_wrong["status"]), axis=-1),
        hovertemplate="<b>Date:</b> %{x}<br><b>Price:</b> " + currency_symbol + "%{y:.2f}<br><b>Actual Next Day:</b> %{customdata[0]}<br><b>Predicted:</b> %{customdata[1]}<br><span style='color:#f43f5e'>%{customdata[2]}</span><extra></extra>"
    ))

    fig_price.update_layout(
        template="plotly_dark",
        paper_bgcolor="#090d16",
        plot_bgcolor="#090d16",
        height=450,
        margin=dict(l=20, r=20, t=30, b=30),
        xaxis=dict(title="Trading Date", gridcolor="#1e293b", showgrid=True),
        yaxis=dict(title=f"Close Price ({currency_symbol})", gridcolor="#1e293b", showgrid=True),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_price, use_container_width=True)

# ---------------------------------------------------------
# Tab 2: Accuracy Comparison Bar Chart
# ---------------------------------------------------------
with tab_acc:
    st.markdown("#### Test Accuracy Benchmark vs Random Baseline (%)")
    st.caption("How each model scored on the 100 out-of-sample trading days compared against a 50% random coin flip.")

    acc_df = pd.DataFrame({
        "Model": ["Quantum SVM (QSVC)", "Classical SVM (RBF)", "Blind Guessing Baseline", "Random Coin Flip"],
        "Accuracy (%)": [q_acc, c_acc, baseline * 100, 50.0],
        "Color": ["#818cf8", "#34d399", "#fbbf24", "#64748b"]
    })

    fig_bar = px.bar(
        acc_df,
        x="Model",
        y="Accuracy (%)",
        color="Model",
        color_discrete_map={
            "Quantum SVM (QSVC)": "#6366f1",
            "Classical SVM (RBF)": "#10b981",
            "Blind Guessing Baseline": "#f59e0b",
            "Random Coin Flip": "#64748b"
        },
        text=acc_df["Accuracy (%)"].apply(lambda v: f"{v:.1f}%")
    )

    fig_bar.add_hline(y=50, line_dash="dash", line_color="#94a3b8", annotation_text="50% Coin Flip", annotation_position="top right")

    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="#090d16",
        plot_bgcolor="#090d16",
        height=400,
        margin=dict(l=20, r=20, t=30, b=30),
        yaxis=dict(range=[0, 100], title="Accuracy (%)", gridcolor="#1e293b"),
        showlegend=False
    )
    fig_bar.update_traces(textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Performance Table
    st.markdown("##### Detailed Metric Breakdown")
    comp_table = pd.DataFrame({
        "Performance Metric": [
            "Accuracy (Overall Correct Guesses)",
            "Precision (When model guessed UP, was it UP?)",
            "Recall (Out of all real UP days, how many caught?)",
            "F1 Score (Balanced Metric)",
            "Simulation / Training Time"
        ],
        "Quantum SVM": [
            f"{q_acc:.1f}%",
            f"{qsvm['precision']*100:.1f}%",
            f"{qsvm['recall']*100:.1f}%",
            f"{qsvm['f1']*100:.1f}%",
            f"{qsvm['training_time']:.2f}s"
        ],
        "Classical SVM": [
            f"{c_acc:.1f}%",
            f"{svm['precision']*100:.1f}%",
            f"{svm['recall']*100:.1f}%",
            f"{svm['f1']*100:.1f}%",
            f"{svm['training_time']:.2f}s"
        ]
    })
    st.table(comp_table)

# ---------------------------------------------------------
# Tab 3: Model Scorecards (Confusion Matrix)
# ---------------------------------------------------------
with tab_matrix:
    st.markdown("#### Model Scorecards (Confusion Matrix across 100 Test Days)")
    st.caption("Detailed matrix of predicted directions vs actual price directions.")

    mat_col1, mat_col2 = st.columns(2)

    def render_cm_display(cm, title, accent_color):
        tn, fp = cm[0][0], cm[0][1]
        fn, tp = cm[1][0], cm[1][1]
        total_correct = tn + tp
        st.markdown(f"##### {title}")
        st.caption(f"Score: **{total_correct}/100 Correct Predictions**")

        cm_df = pd.DataFrame(
            [
                [f"✅ {tn} (True DOWN)", f"❌ {fp} (False UP)"],
                [f"❌ {fn} (False DOWN)", f"✅ {tp} (True UP)"]
            ],
            index=["Actual DOWN", "Actual UP"],
            columns=["Predicted DOWN", "Predicted UP"]
        )
        st.table(cm_df)

    with mat_col1:
        render_cm_display(qsvm["confusion_matrix"], "⚛️ Quantum SVM (4-Qubit Circuit)", "#818cf8")

    with mat_col2:
        render_cm_display(svm["confusion_matrix"], "💻 Classical SVM (RBF Kernel)", "#34d399")

# ---------------------------------------------------------
# Tab 4: 30x30 Quantum Similarity Heatmap
# ---------------------------------------------------------
with tab_heatmap:
    st.markdown("#### 30×30 Quantum Kernel Similarity Heatmap")
    st.caption(
        "Each cell (i, j) shows the exact quantum state fidelity |⟨ψ(x_i)|ψ(x_j)⟩|² "
        "between training days i and j in the 4-qubit ZZFeatureMap Hilbert space. Diagonal is always 1.0 (Day compared to itself)."
    )

    fig_heat = px.imshow(
        kernel_mat,
        labels=dict(x="Training Day j", y="Training Day i", color="Quantum Overlap"),
        x=[f"Day {k+1}" for k in range(30)],
        y=[f"Day {k+1}" for k in range(30)],
        color_continuous_scale="Viridis",
        zmin=0.0,
        zmax=1.0
    )
    fig_heat.update_layout(
        template="plotly_dark",
        paper_bgcolor="#090d16",
        plot_bgcolor="#090d16",
        height=520,
        margin=dict(l=20, r=20, t=30, b=30)
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ---------------------------------------------------------
# Tab 5: Project Methodology & Quantum Circuit
# ---------------------------------------------------------
with tab_methodology:
    st.markdown("#### Project Pipeline & Architecture")
    st.markdown(
        """
        Our project pipeline transforms raw stock price time series into 4-qubit quantum states:
        
        1. **Live Data Collection (`yfinance`):**
           - Downloads 5 years of daily OHLCV prices for the selected stock.
        
        2. **Technical Feature Engineering (`pandas`):**
           - **RSI (14-day):** Momentum oscillator for overbought/oversold boundaries.
           - **MACD Histogram:** Difference between (12-day EMA − 26-day EMA) and the 9-day signal line.
           - **Moving Average Ratio:** `Close / SMA(20)` measuring distance from the prevailing trend.
           - **Volume Change:** Daily percentage change in trading volume.
        
        3. **Chronological Train/Test Split (No Leakage):**
           - Most recent 350 trading days: **First 250 days for training**, **last 100 days for testing**.
           - Scaled strictly to $[0, \pi]$ using `MinMaxScaler` fit **only on training data** to prevent $2\pi$ periodic rotation wrapping.
        
        4. **4-Qubit Quantum Feature Map (`ZZFeatureMap`):**
           - Maps each 4D feature vector into 4 qubits using Hadamard gates and linear $ZZ$ entangling gates parameterized by pairwise feature interactions $(\pi - x_i)(\pi - x_j)$.
        
        5. **Statevector Quantum Kernel & Classification:**
           - Computes exact quantum state fidelities $|\langle \psi(x_i) | \psi(x_j) \rangle|^2$ using vectorized Hermitian inner products.
           - Trains a Support Vector Machine to find the optimal separating hyperplane in the 16-dimensional quantum Hilbert space.
        """
    )

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    "<center><small style='color: #64748b;'>"
    "B.Tech Computer Science & Engineering Final Year Capstone Project • Powered by Qiskit & Yahoo Finance"
    "</small></center>",
    unsafe_allow_html=True
)
