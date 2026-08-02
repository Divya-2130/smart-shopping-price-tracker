/**
 * src/components/ProductCard.js
 * -------------------------------
 * A reusable "card" that shows one product's image, name, price, and
 * seller. Used on the Search page and Wishlist page. Being its own
 * component means we write this UI once and reuse it everywhere.
 */
import React from "react";
import { Link } from "react-router-dom";
import api from "../api/api";

export default function ProductCard({ product, showRemove, onRemoved }) {
  const addToWishlist = async () => {
    await api.post("wishlist/", { product_id: product.id });
    alert("Added to wishlist!");
  };

  const removeFromWishlist = async () => {
    await api.delete(`wishlist/?product_id=${product.id}`);
    if (onRemoved) onRemoved(product.id);
  };

  return (
    <div style={styles.card}>
      <img src={product.image_url} alt={product.name} style={styles.image} />
      <h4 style={styles.name}>{product.name}</h4>
      <p style={styles.seller}>{product.seller}</p>
      <p style={styles.price}>₹{product.price}</p>

      <div style={styles.actions}>
        <Link to={`/product/${product.id}`} style={styles.detailBtn}>View</Link>
        {showRemove ? (
          <button onClick={removeFromWishlist} style={styles.removeBtn}>♥ Remove</button>
        ) : (
          <button onClick={addToWishlist} style={styles.wishlistBtn}>♡ Wishlist</button>
        )}
      </div>
    </div>
  );
}

const styles = {
  card: {
    border: "1px solid #e0e0e0",
    borderRadius: "10px",
    padding: "14px",
    width: "220px",
    background: "#fff",
  },
  image: { width: "100%", height: "140px", objectFit: "contain" },
  name: { fontSize: "14px", margin: "8px 0 4px" },
  seller: { fontSize: "12px", color: "#777" },
  price: { fontSize: "16px", fontWeight: "bold", color: "#1a1a2e" },
  actions: { display: "flex", justifyContent: "space-between", marginTop: "10px" },
  detailBtn: { fontSize: "12px", color: "#2b6cb0" },
  wishlistBtn: { fontSize: "12px", background: "none", border: "1px solid #ccc", borderRadius: "6px", padding: "4px 8px" },
  removeBtn: { fontSize: "12px", background: "none", border: "1px solid #e53e3e", color: "#e53e3e", borderRadius: "6px", padding: "4px 8px" },
};
