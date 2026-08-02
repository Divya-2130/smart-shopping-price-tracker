/**
 * src/pages/NotificationsPage.js
 * ---------------------------------
 * Shows the history of price-drop alerts sent to this user.
 */
import React, { useEffect, useState } from "react";
import api from "../api/api";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    api.get("notifications/").then((res) => setNotifications(res.data));
  }, []);

  return (
    <div>
      <h2>Notifications</h2>
      {notifications.length === 0 && <p>No notifications yet.</p>}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {notifications.map((n) => (
          <li key={n.id} style={styles.item}>
            <p>{n.message}</p>
            <small style={{ color: "#777" }}>{new Date(n.sent_at).toLocaleString()}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}

const styles = {
  item: {
    background: "#fff",
    border: "1px solid #e0e0e0",
    borderRadius: "8px",
    padding: "12px 16px",
    marginBottom: "10px",
  },
};
