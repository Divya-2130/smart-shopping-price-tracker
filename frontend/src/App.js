/**
 * src/App.js
 * -----------
 * This is the "traffic controller" of the frontend — it decides which
 * page component to show based on the URL, and renders the shared
 * navigation bar on every page.
 */
import React from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import SearchPage from "./pages/SearchPage";
import ProductDetailPage from "./pages/ProductDetailPage";
import WishlistPage from "./pages/WishlistPage";
import NotificationsPage from "./pages/NotificationsPage";

function NavBar() {
  return (
    <nav style={styles.nav}>
      <Link to="/" style={styles.brand}>🛒 Smart Shopping</Link>
      <div style={styles.links}>
        <Link to="/">Search</Link>
        <Link to="/wishlist">Wishlist</Link>
        <Link to="/notifications">Notifications</Link>
        <Link to="/login">Login</Link>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <div className="container">
        <Routes>
          <Route path="/" element={<SearchPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/product/:id" element={<ProductDetailPage />} />
          <Route path="/wishlist" element={<WishlistPage />} />
          <Route path="/notifications" element={<NotificationsPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "14px 24px",
    background: "#1a1a2e",
    color: "#fff",
  },
  brand: { fontWeight: "bold", fontSize: "18px", color: "#fff" },
  links: { display: "flex", gap: "18px" },
};
