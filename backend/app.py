import copy
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from data import fetch_and_prepare_data
from models import run_comparison_pipeline

app = Flask(__name__)

# Enable CORS for Vite default dev server (http://localhost:5173) and local aliases
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ]
        }
    },
)

# In-memory cache keyed by uppercase ticker symbol
RESULTS_CACHE = {}


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/api/run", methods=["POST"])
def run_classifier():
    payload = request.get_json(silent=True)
    if not payload or "ticker" not in payload:
        return jsonify({
            "message": "Missing required field 'ticker' in JSON request body."
        }), 400

    ticker = str(payload.get("ticker", "")).strip().upper()
    if not ticker or len(ticker) > 25:
        return jsonify({
            "message": "Please provide a valid stock ticker symbol (e.g., RELIANCE.NS, TCS.NS, AAPL)."
        }), 400

    # Return cached result immediately if available
    if ticker in RESULTS_CACHE:
        cached_resp = copy.deepcopy(RESULTS_CACHE[ticker])
        cached_resp["cached"] = True
        return jsonify(cached_resp), 200

    try:
        df_recent = fetch_and_prepare_data(ticker)
        result = run_comparison_pipeline(df_recent, ticker)
        RESULTS_CACHE[ticker] = copy.deepcopy(result)
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"message": str(ve)}), 400
    except ImportError as ie:
        return jsonify({"message": f"Quantum library configuration error: {str(ie)}"}), 500
    except RuntimeError as re_err:
        return jsonify({"message": str(re_err)}), 502
    except Exception as exc:
        return jsonify({
            "message": f"Unexpected server error while processing '{ticker}': {str(exc)}"
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
