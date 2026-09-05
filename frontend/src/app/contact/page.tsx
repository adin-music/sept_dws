"use client";

import { useState } from "react";
import { API_BASE } from "@/lib/api";

export default function ContactPage() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const fd = new FormData();
    fd.append("email", email);
    fd.append("message", message);
    const res = await fetch(`${API_BASE}/api/contact`, { method: "POST", body: fd });
    if (res.ok) {
      setSent(true);
      setEmail("");
      setMessage("");
    }
  };

  return (
    <div style={{ maxWidth: 500, margin: "0 auto", padding: 20 }}>
      <h1>Kontakt</h1>
      {sent && <p style={{ color: "green" }}>Poruka poslana!</p>}
      <form onSubmit={handleSubmit}>
        <p><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required style={{ width: "100%", padding: 8 }} /></p>
        <p><textarea value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Poruka" required rows={5} style={{ width: "100%", padding: 8 }} /></p>
        <button type="submit" style={{ padding: "8px 16px" }}>Pošalji</button>
      </form>
    </div>
  );
}
