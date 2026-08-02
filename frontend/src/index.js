/**
 * src/index.js
 * -------------
 * The starting point of the React app. It finds the <div id="root">
 * in index.html and renders our <App /> component inside it.
 */
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
