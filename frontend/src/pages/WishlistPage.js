/**
 * src/pages/WishlistPage.js
 * ----------------------------
 * Shows every product the user has saved to their wishlist.
 */
import React, { useEffect, useState } from "react";
import api from "../api/api";
import ProductCard from "../components/ProductCard";

export default function WishlistPage() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    api.get("wishlist/").then((res) => setItems(res.data));
  }, []);

  const handleRemoved = (productId) => {
    setItems((prev) => prev.filter((item) => item.product.id !== productId));
  };

  return (
    <div>
      <h2>My Wishlist</h2>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "16px" }}>
        {items.map((item) => (
          <ProductCard key={item.id} product={item.product} showRemove onRemoved={handleRemoved} />
        ))}
      </div>
      {items.length === 0 && <p>Your wishlist is empty.</p>}
    </div>
  );
}
