# QuantumTrade Lab: Quantum Stock Trend Classifier (QSVM vs Classical SVM)

An end-to-end full-stack educational and research application that predicts whether a stock closes **UP (1)** or **DOWN (0)** the next trading day using a **4-Qubit Quantum Support Vector Machine (QSVM)** with an entangled `ZZFeatureMap` and benchmarks it side-by-side against a **Classical RBF-Kernel SVM**.

Supports **Indian Equities (NSE)** with actual full company names (e.g. *Reliance Industries Limited*, *Tata Consultancy Services*, *HDFC Bank*, *State Bank of India*, *Infosys*) in **₹ (INR)** and **US Equities** (*Apple*, *Microsoft*, *NVIDIA*, *Google*, *Amazon*, *Tesla*) in **$ (USD)**.

> **Disclaimer:** Day-to-day stock market direction contains substantial stochastic noise. Realistic next-day direction accuracy hovers near 50–55%. This project is an academic comparative study of quantum vs. classical machine learning on financial time series, not financial advice.

---

## Key Features

- **Live Market Data:** Fetches 5 years of daily OHLCV prices from Yahoo Finance via `yfinance`.
- **4 Classical Technical Features:**
  - **RSI (14-day):** Momentum oscillator for overbought/oversold conditions.
  - **MACD Histogram:** Difference between (12-day EMA − 26-day EMA) and the 9-day signal line.
  - **Moving Average Ratio:** `Close / SMA(20)` measuring distance from the prevailing trend.
  - **Volume Change:** Daily percentage change in trading volume.
- **Leakage-Free Chronological Split & $[0, \pi]$ Scaling:**
  - Strict chronological split: **250 trading days for training**, **100 days for testing** (no shuffling/look-ahead bias).
  - Scaled strictly to $[0, \pi]$ on training data only to map features to distinct quantum rotation angles without $2\pi$ phase aliasing.
- **4-Qubit Quantum Feature Map (`ZZFeatureMap`):**
  - Linear nearest-neighbor entanglement parameterized by pairwise feature products $(\pi - x_i)(\pi - x_j)$.
- **Vectorized Fast Statevector Kernel:**
  - Calculates exact quantum state fidelities $|\langle \psi(x_i) | \psi(x_j) \rangle|^2$ via vectorized inner products, completing in ~1.5 seconds locally without cloud queues or IBM Quantum API keys.
- **Full-Featured Interactive Web UI:**
  - Market switcher (🇮🇳 NSE Indian Equities vs. 🇺🇸 US Equities).
  - Search by company name, sector filter chips, and custom ticker support.
  - Head-to-Head Comparison Table & Model Showdown banner.
  - Interactive 100-day price history chart with directional prediction dots (green = correct, red = mistake).
  - Model Scorecards (Confusion Matrix breakdown).
  - 30×30 Quantum Kernel Similarity Heatmap with sample inspector.
  - Project Architecture & Methodology visualizer.

---

## Folder Structure

```text
quantum-stock-classifier/
├── backend/
│   ├── app.py              # Flask REST API server (port 5001)
│   ├── data.py             # yfinance data retrieval & indicator calculation
│   ├── models.py           # 4-qubit QSVM & Classical SVM benchmarking
│   └── requirements.txt    # Python dependencies (Qiskit 1.x, scikit-learn, etc.)
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       ├── stocks.js       # Curated Indian & US equities with full names & sectors
│       └── components/
│           ├── AccuracyChart.jsx
│           ├── ConfusionMatrices.jsx
│           ├── KernelHeatmap.jsx
│           ├── MetricsComparison.jsx
│           ├── PricePredictionChart.jsx
│           └── ProjectMethodology.jsx
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites
- **Python 3.10+** (Python 3.11 recommended)
- **Node.js 18+** and `npm`

### 1. Backend Setup (Flask + Qiskit 1.x)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

The Flask API will start at `http://localhost:5001`.
- Health check: `GET http://localhost:5001/api/health` -> `{"status": "ok"}`
- Run pipeline: `POST http://localhost:5001/api/run` with `{"ticker": "RELIANCE.NS"}` or `{"ticker": "AAPL"}`

*(Note: Port 5001 is used by default to prevent port conflicts with macOS ControlCenter / AirPlay on port 5000).*

### 2. Frontend Setup (React + Vite + Tailwind CSS)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Tech Stack

- **Quantum Computing:** Qiskit 1.4 (`qiskit`, `qiskit-machine-learning`, `qiskit-aer`)
- **Machine Learning:** Scikit-Learn (`SVC`, `MinMaxScaler`, metrics)
- **Financial Data:** `yfinance`, `pandas`, `numpy`
- **Backend Server:** Flask, Flask-CORS
- **Frontend Framework:** React 18, Vite, Tailwind CSS, Recharts
