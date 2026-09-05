"use client";

import { useEffect, useState } from "react";
import PostFeed from "@/components/PostFeed";
import { API_BASE } from "@/lib/api";

export default function AdminPage() {
  const [tab, setTab] = useState("pregled");
  const [stats, setStats] = useState<any>({});
  const [users, setUsers] = useState<any[]>([]);
  const [messages, setMessages] = useState<any[]>([]);
  const [recentPosts, setRecentPosts] = useState<any[]>([]);
  const [reply, setReply] = useState("");
  const [selectedMsg, setSelectedMsg] = useState<any>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/admin/stats`).then((r) => r.json()).then(setStats);
  }, []);

  const loadUsers = () => {
    fetch(`${API_BASE}/api/admin/users`).then((r) => r.json()).then(setUsers);
  };

  const loadMessages = () => {
    fetch(`${API_BASE}/api/admin/messages/unanswered`).then((r) => r.json()).then(setMessages);
  };

  const loadRecent = () => {
    fetch(`${API_BASE}/api/admin/posts/recent`).then((r) => r.json()).then(setRecentPosts);
  };

  const deleteUser = (id: number) => {
    if (!confirm("Obrisati korisnika?")) return;
    fetch(`${API_BASE}/api/admin/users/${id}`, { method: "DELETE" }).then(() => loadUsers());
  };

  const sendReply = () => {
    if (!selectedMsg || !reply) return;
    fetch(`${API_BASE}/api/admin/messages/${selectedMsg.id}/reply`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reply_text: reply }),
    }).then(() => {
      setSelectedMsg(null);
      setReply("");
      loadMessages();
    });
  };

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 20 }}>
      <h1>Admin panel</h1>

      <div style={{ marginBottom: 20 }}>
        <button onClick={() => setTab("pregled")} style={{ marginRight: 8 }}>Pregled</button>
        <button onClick={() => { setTab("recent"); loadRecent(); }} style={{ marginRight: 8 }}>Nove objave</button>
        <button onClick={() => setTab("objave")} style={{ marginRight: 8 }}>Sve objave</button>
        <button onClick={() => { setTab("korisnici"); loadUsers(); }} style={{ marginRight: 8 }}>Korisnici</button>
        <button onClick={() => { setTab("poruke"); loadMessages(); }}>Poruke</button>
      </div>

      {tab === "pregled" && (
        <div>
          <p>Objave (24h): {stats.recent_posts || 0}</p>
          <p>Ukupno objava: {stats.total_posts || 0}</p>
          <p>Korisnici: {stats.total_users || 0}</p>
          <p>Nepročitane poruke: {stats.unread_messages || 0}</p>
        </div>
      )}

      {tab === "recent" && recentPosts.map((p) => (
        <div key={p.id} style={{ border: "1px solid #ddd", padding: 8, marginBottom: 8 }}>
          <b>{p.title}</b>
          <p>{p.content}</p>
        </div>
      ))}

      {tab === "objave" && <PostFeed />}

      {tab === "korisnici" && users.map((u) => (
        <div key={u.id} style={{ border: "1px solid #ddd", padding: 8, marginBottom: 8, display: "flex", justifyContent: "space-between" }}>
          <span>{u.username} - {u.email} - {u.role}</span>
          <button onClick={() => deleteUser(u.id)} style={{ color: "red" }}>Obriši</button>
        </div>
      ))}

      {tab === "poruke" && (
        <div>
          {messages.map((m) => (
            <div key={m.id} style={{ border: "1px solid #ddd", padding: 8, marginBottom: 8, cursor: "pointer" }} onClick={() => setSelectedMsg(m)}>
              <b>{m.email}</b>
              <p>{m.message}</p>
            </div>
          ))}
          {selectedMsg && (
            <div style={{ border: "2px solid #0284c7", padding: 12, marginTop: 12 }}>
              <p><b>Od:</b> {selectedMsg.email}</p>
              <p>{selectedMsg.message}</p>
              <textarea value={reply} onChange={(e) => setReply(e.target.value)} rows={3} style={{ width: "100%" }} />
              <button onClick={sendReply} style={{ marginTop: 8 }}>Pošalji odgovor</button>
              <button onClick={() => setSelectedMsg(null)} style={{ marginLeft: 8 }}>Zatvori</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
