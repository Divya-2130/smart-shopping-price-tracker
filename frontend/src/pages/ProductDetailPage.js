/**
 * src/pages/ProductDetailPage.js
 * ---------------------------------
 * Shows one product's details plus its price history as a line chart
 * (using the 'recharts' library), and a button to start tracking it.
 */
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";
import api from "../api/api";

export default function ProductDetailPage() {
  const { id } = useParams();
  const [tracked, setTracked] = useState(null);
  const [targetPrice, setTargetPrice] = useState("");

  useEffect(() => {
    // Pull the tracked version of this product (if already tracked) to show history
    api.get("tracking/my-tracked/").then((res) => {
      const match = res.data.find((t) => t.product.id === Number(id));
      if (match) setTracked(match);
    });
  }, [id]);

  const handleTrack = async () => {
    const response = await api.post("tracking/track/", {
      product_id: id,
      target_price: targetPrice || null,
    });
    setTracked(response.data);
    alert("Now tracking this product!");
  };

  const chartData = tracked
    ? tracked.price_history.map((p) => ({
        date: new Date(p.recorded_at).toLocaleDateString(),
        price: parseFloat(p.price),
      }))
    : [];

  return (
    <div>
      <h2>Product Details</h2>

      {tracked ? (
        <>
          <h3>{tracked.product.name}</h3>
          <p>Current Price: ₹{tracked.product.price}</p>

          <h4>Price History</h4>
          <ResponsiveContainer width="100%" height={260}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="price" stroke="#1a1a2e" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </>
      ) : (
        <div>
          <p>You are not tracking this product yet.</p>
          <input
            type="number"
            placeholder="Notify me if price drops below (optional)"
            value={targetPrice}
            onChange={(e) => setTargetPrice(e.target.value)}
            style={{ padding: "8px", marginRight: "10px" }}
          />
          <button onClick={handleTrack} style={{ padding: "8px 16px" }}>
            Track this product
          </button>
        </div>
      )}
    </div>
  );
}
