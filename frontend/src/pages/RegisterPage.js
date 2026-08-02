import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

export default function RegisterPage() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    phone_number: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      await api.post("auth/register/", {
        username: form.username,
        email: form.email,
        password: form.password,
        phone_number: form.phone_number,
      });
      navigate("/login");
    } catch (err) {
      if (err.response && err.response.data) {
        const messages = Object.values(err.response.data).flat().join(" ");
        setError(messages);
      } else {
        setError("Registration failed. Please try again.");
      }
    }
  };

  return (
    <div style={{ maxWidth: "360px", margin: "40px auto" }}>
      <h2>Create Account</h2>
      <form onSubmit={handleSubmit}>
        <input
          name="username"
          placeholder="Username"
          value={form.username}
          onChange={handleChange}
          required
          style={inputStyle}
        />
        <input
          name="email"
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
          style={inputStyle}
        />

        <div style={{ position: "relative" }}>
          <input
            name="password"
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            required
            autoComplete="new-password"
            style={{ ...inputStyle, paddingRight: "50px" }}
          />
          <span
            onClick={() => setShowPassword(!showPassword)}
            style={{
              position: "absolute",
              right: "12px",
              top: "12px",
              cursor: "pointer",
              fontSize: "13px",
              color: "#555",
            }}
          >
            {showPassword ? "Hide" : "Show"}
          </span>
        </div>

        <input
          name="confirmPassword"
          type={showPassword ? "text" : "password"}
          placeholder="Confirm Password"
          value={form.confirmPassword}
          onChange={handleChange}
          required
          autoComplete="new-password"
          style={inputStyle}
        />

        <input
          name="phone_number"
          placeholder="Phone (for SMS alerts)"
          value={form.phone_number}
          onChange={handleChange}
          style={inputStyle}
        />

        {error && <p style={{ color: "red" }}>{error}</p>}

        <button
          type="submit"
          style={{
            width: "100%",
            padding: "10px",
            background: "#1a1a2e",
            color: "#fff",
            border: "none",
            borderRadius: "6px",
          }}
        >
          Register
        </button>
      </form>
    </div>
  );
}

const inputStyle = {
  display: "block",
  width: "100%",
  padding: "10px",
  marginBottom: "12px",
  boxSizing: "border-box",
  borderRadius: "6px",
  border: "1px solid #ccc",
};