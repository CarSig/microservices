import axios from "axios";

// if (!import.meta.env.VITE_API_URL) {
//   throw new Error("VITE_API_URL is not set");
// }

export const api = axios.create({
  baseURL: "/api",
  timeout: 8000,
});

// Optional: log errors nicely
api.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error("API Error:", err.response?.data || err.message);
    throw err;
  }
);
