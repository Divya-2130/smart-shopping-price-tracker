/**
 * src/pages/SearchPage.js
 * -------------------------
 * The homepage. User types a product name, we call GET /api/products/search/,
 * and render a ProductCard for each result.
 */
import React, { useState } from "react";
import api from "../api/api";
import ProductCard from "../components/ProductCard";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    try {
      const response = await api.get(`products/search/?q=${encodeURIComponent(query)}`);
      setResults(response.data.results);
    } catch (err) {
      alert("Search failed. Make sure you are logged in.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Search Products</h2>
      <form onSubmit={handleSearch} style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="e.g. iPhone 15"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{ flex: 1, padding: "10px", borderRadius: "6px", border: "1px solid #ccc" }}
        />
        <button type="submit" style={{ padding: "10px 20px", background: "#1a1a2e", color: "#fff", border: "none", borderRadius: "6px" }}>
          Search
        </button>
      </form>

      {loading && <p>Loading...</p>}

      <div style={{ display: "flex", flexWrap: "wrap", gap: "16px" }}>
        {results.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}
