/**
 * src/api/api.js
 * ---------------
 * A single, shared Axios instance. Every page/component imports THIS
 * instead of calling axios directly, so:
 *   - the backend base URL is defined in one place
 *   - the JWT auth token is automatically attached to every request
 */
import axios from "axios";

const api = axios.create({
  baseURL: "https://smart-shopping-price-tracker.onrender.com/api/",
});

// Runs before every request — attaches the saved login token, if any
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
