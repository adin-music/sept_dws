"use client";

import { useEffect, useState } from "react";
import PostFeed from "@/components/PostFeed";
import { API_BASE, CATEGORIES } from "@/lib/api";

export default function HomePage() {
  const [tab, setTab] = useState("all");
  const [category, setCategory] = useState("");
  const [trending, setTrending] = useState<any[]>([]);
  const [myInterests, setMyInterests] = useState<string[]>([]);

  useEffect(() => {
    fetch(`${API_BASE}/api/trending?period=24h`)
      .then((r) => r.json())
      .then((d) => setTrending(Array.isArray(d) ? d.slice(0, 5) : []));

    const userId = localStorage.getItem("userId");
    if (userId) {
      fetch(`${API_BASE}/api/follow/interests/${userId}`)
        .then((r) => r.json())
        .then((d) => setMyInterests(d.categories || []));
    }
  }, []);

  const toggleInterest = (cat: string) => {
    const userId = localStorage.getItem("userId");
    if (!userId) {
      alert("Morate biti prijavljeni");
      return;
    }
    let next = [...myInterests];
    if (next.includes(cat)) {
      next = next.filter((c) => c !== cat);
    } else {
      next.push(cat);
    }
    fetch(`${API_BASE}/api/follow/interests`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: parseInt(userId), categories: next }),
    }).then(() => setMyInterests(next));
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 20 }}>
      <h1>Objave</h1>

      <div style={{ border: "1px solid #ddd", padding: 12, marginBottom: 16, background: "#f9f9f9" }}>
        <h3>Moji interesi</h3>
        {CATEGORIES.filter((c) => c.value).map((c) => (
          <button
            key={c.value}
            onClick={() => toggleInterest(c.value)}
            style={{
              marginRight: 8,
              marginBottom: 8,
              padding: "6px 10px",
              background: myInterests.includes(c.value) ? "#0284c7" : "#eee",
              color: myInterests.includes(c.value) ? "white" : "black",
              border: "1px solid #ccc",
            }}
          >
            {c.label}
          </button>
        ))}
      </div>

      {trending.length > 0 && (
        <div style={{ border: "1px solid #ddd", padding: 12, marginBottom: 20, background: "#f9f9f9" }}>
          <h2>Trending (24h)</h2>
          {trending.map((p, i) => (
            <p key={p.id}>{i + 1}. {p.title} - {p.author_username}</p>
          ))}
        </div>
      )}

      <button onClick={() => setTab("all")} style={{ marginRight: 8, padding: "6px 12px" }}>Sve</button>
      <button onClick={() => setTab("recommended")} style={{ marginRight: 8, padding: "6px 12px" }}>Preporučeno</button>
      <button onClick={() => setTab("saved")} style={{ padding: "6px 12px" }}>Sačuvano</button>

      <div style={{ marginTop: 12 }}>
        <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ padding: 8 }}>
          {CATEGORIES.map((c) => (
            <option key={c.value || "all"} value={c.value}>{c.label}</option>
          ))}
        </select>
      </div>

      <div style={{ marginTop: 20 }}>
        <PostFeed mode={tab} category={category} />
      </div>
    </div>
  );
}
