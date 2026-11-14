import time
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

# Verify Qiskit 1.x and Qiskit Machine Learning imports with helpful error reporting
try:
    from qiskit.circuit.library import ZZFeatureMap
    from qiskit.quantum_info import Statevector
    from qiskit.primitives import StatevectorSampler
    from qiskit_machine_learning.kernels import FidelityQuantumKernel
    from qiskit_machine_learning.algorithms import QSVC
    from qiskit_machine_learning.state_fidelities import ComputeUncompute
except ImportError as e:
    raise ImportError(
        "Failed to import Qiskit or Qiskit Machine Learning modules. "
        "Ensure qiskit>=1.2,<2.0 and qiskit-machine-learning>=0.8,<0.9 are installed. "
        f"Original error: {str(e)}"
    )

FEATURE_COLS = ["rsi_14", "macd_hist", "ma_ratio", "vol_change"]


def compute_metrics(y_true, y_pred, train_time_sec: float):
    """Computes classification metrics and formats confusion matrix as a 2x2 list."""
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1]).tolist()
    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "confusion_matrix": cm,
        "training_time": round(float(train_time_sec), 3),
    }


def run_comparison_pipeline(df_recent, ticker: str):
    """
    Executes the chronological train/test split, scales features to [0, pi]
    without data leakage, trains both QSVM and Classical RBF-SVM, computes
    the 30x30 quantum kernel matrix for visualization, and packages all results.
    """
    # 1. Chronological split: first 250 for training, last 100 for testing (no shuffling!)
    train_df = df_recent.iloc[:250].copy()
    test_df = df_recent.iloc[250:350].copy()

    X_train_raw = train_df[FEATURE_COLS].values
    y_train = train_df["label"].values

    X_test_raw = test_df[FEATURE_COLS].values
    y_test = test_df["label"].values

    # 2. Scaling: Why scale to [0, pi]?
    # Quantum feature maps like ZZFeatureMap encode classical data into quantum
    # states using rotation gates (e.g., RZ(x), P(x)). Because quantum rotations
    # are periodic with period 2*pi, scaling features to [0, pi] prevents phase
    # wrapping (aliasing where distinct extreme values map to the same quantum angle)
    # and ensures monotonic angular separation on the Bloch sphere.
    # IMPORTANT: Fit ONLY on the training set to avoid look-ahead data leakage.
    scaler = MinMaxScaler(feature_range=(0, np.pi))
    X_train = scaler.fit_transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)

    # 3. Quantum Support Vector Machine (QSVM)
    # - ZZFeatureMap(feature_dimension=4, reps=2, entanglement="linear"):
    #   Maps the 4 classical features into a 4-qubit Hilbert space. It applies
    #   Hadamard gates to create superposition, single-qubit phase rotations proportional
    #   to individual features, and two-qubit ZZ entangling gates between adjacent
    #   qubits ("linear" topology) parameterized by pairwise feature products
    #   (pi - x_i)(pi - x_j). Repeating this layer twice (reps=2) builds non-linear
    #   quantum feature interactions that are intractable to simulate classically at scale.
    # - FidelityQuantumKernel & Vectorized Statevector Evaluation:
    #   Measures similarity between feature vectors x_i and x_j by computing the
    #   exact quantum state fidelity |<0| U^dagger(x_i) U(x_j) |0>|^2 = |<psi(x_i)|psi(x_j)>|^2.
    #   By generating the 4-qubit statevectors directly and computing the Gram matrix
    #   via vectorized inner products, we achieve mathematically exact zero-shot-noise
    #   fidelities instantaneously (seconds vs. 5+ minutes).
    feature_map = ZZFeatureMap(
        feature_dimension=4,
        reps=2,
        entanglement="linear",
    )

    qsvm_start = time.perf_counter()
    svs_train = np.array([Statevector.from_instruction(feature_map.assign_parameters(row)).data for row in X_train])
    svs_test = np.array([Statevector.from_instruction(feature_map.assign_parameters(row)).data for row in X_test])

    K_train = np.abs(svs_train @ svs_train.conj().T) ** 2
    K_test = np.abs(svs_test @ svs_train.conj().T) ** 2

    qsvc = SVC(kernel="precomputed")
    qsvc.fit(K_train, y_train)
    qsvm_preds = qsvc.predict(K_test)
    qsvm_time = time.perf_counter() - qsvm_start

    qsvm_metrics = compute_metrics(y_test, qsvm_preds, qsvm_time)

    # 4. Classical Support Vector Machine (RBF Kernel) baseline on identical scaled data
    svm_start = time.perf_counter()
    classical_svc = SVC(kernel="rbf", C=1.0, gamma="scale")
    classical_svc.fit(X_train, y_train)
    svm_preds = classical_svc.predict(X_test)
    svm_time = time.perf_counter() - svm_start

    svm_metrics = compute_metrics(y_test, svm_preds, svm_time)

    # 5. Majority-class baseline accuracy on the test set
    # Find the most frequent class in the training set (or test set majority baseline)
    # Reporting test set majority-class baseline accuracy as requested:
    unique_classes, counts = np.unique(y_test, return_counts=True)
    majority_class = int(unique_classes[np.argmax(counts)])
    majority_baseline_acc = round(float(np.max(counts) / len(y_test)), 4)

    # 6. Quantum Kernel Matrix for the first 30 training samples (30x30 heatmap)
    kernel_matrix_30x30 = np.round(K_train[:30, :30], 4).tolist()

    # 7. Class balance summary
    train_up = int(np.sum(y_train == 1))
    train_down = int(np.sum(y_train == 0))
    test_up = int(np.sum(y_test == 1))
    test_down = int(np.sum(y_test == 0))

    # 8. Package recent_prices (last 100 test days with dates, close prices, actual & predictions)
    recent_prices = []
    for idx, (dt, row) in enumerate(test_df.iterrows()):
        date_str = dt.strftime("%Y-%m-%d") if hasattr(dt, "strftime") else str(dt)[:10]
        actual_label = int(y_test[idx])
        q_pred = int(qsvm_preds[idx])
        c_pred = int(svm_preds[idx])
        recent_prices.append({
            "date": date_str,
            "close": round(float(row["Close"]), 2),
            "actual_label": actual_label,
            "qsvm_pred": q_pred,
            "qsvm_correct": bool(q_pred == actual_label),
            "svm_pred": c_pred,
            "svm_correct": bool(c_pred == actual_label),
        })

    return {
        "ticker": ticker.strip().upper(),
        "data_points": {
            "total": int(len(df_recent)),
            "train": int(len(train_df)),
            "test": int(len(test_df)),
        },
        "class_balance": {
            "train_up": train_up,
            "train_down": train_down,
            "train_up_pct": round(train_up / len(y_train), 4),
            "test_up": test_up,
            "test_down": test_down,
            "test_up_pct": round(test_up / len(y_test), 4),
            "majority_test_class": "UP (1)" if majority_class == 1 else "DOWN (0)",
        },
        "qsvm": qsvm_metrics,
        "svm": svm_metrics,
        "majority_baseline": majority_baseline_acc,
        "kernel_matrix_30x30": kernel_matrix_30x30,
        "recent_prices": recent_prices,
        "cached": False,
    }
