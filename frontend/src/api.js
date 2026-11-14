import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:5001";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json"
  },
  timeout: 180000 // 3 minutes timeout for quantum kernel evaluation
});

export async function runStockClassifier(ticker) {
  try {
    const response = await apiClient.post("/api/run", { ticker });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data && error.response.data.message) {
      throw new Error(error.response.data.message);
    }
    if (error.code === "ECONNABORTED") {
      throw new Error("The quantum simulation timed out. Please try again.");
    }
    throw new Error(
      "Unable to reach the backend server at http://localhost:5000. Ensure Flask is running."
    );
  }
}

export async function checkBackendHealth() {
  const response = await apiClient.get("/api/health");
  return response.data;
}
