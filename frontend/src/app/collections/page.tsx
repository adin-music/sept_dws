"use client";

import { useEffect, useState } from "react";
import { API_BASE } from "@/lib/api";

export default function CollectionsPage() {
  const [collections, setCollections] = useState<any[]>([]);
  const [name, setName] = useState("");
  const userId = typeof window !== "undefined" ? localStorage.getItem("userId") : null;

  const load = () => {
    if (!userId) return;
    fetch(`${API_BASE}/api/collections/user/${userId}`).then((r) => r.json()).then(setCollections);
  };

  useEffect(() => { load(); }, []);

  const create = async () => {
    if (!userId || !name) return;
    await fetch(`${API_BASE}/api/collections`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: parseInt(userId), name }),
    });
    setName("");
    load();
  };

  if (!userId) return <p style={{ padding: 20 }}>Morate biti prijavljeni.</p>;

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <h1>Kolekcije</h1>
      <p style={{ fontSize: 14, color: "#666" }}>Klik na Sačuvaj dodaje objavu u kolekciju Moje kolekcije.</p>
      <div style={{ marginBottom: 16 }}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Naziv kolekcije" style={{ padding: 8, marginRight: 8 }} />
        <button onClick={create}>Kreiraj</button>
      </div>
      {collections.map((c) => (
        <div key={c.id} style={{ border: "1px solid #ddd", padding: 12, marginBottom: 8 }}>
          <b>{c.name}</b> (ID: {c.id})
          <p>Broj objava: {c.items_count}</p>
          <p style={{ fontSize: 12 }}>ID objava: {c.post_ids?.join(", ") || "-"}</p>
        </div>
      ))}
    </div>
  );
}
