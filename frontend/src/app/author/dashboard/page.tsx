"use client";

import { useEffect, useState } from "react";
import { API_BASE, CATEGORIES } from "@/lib/api";

export default function AuthorDashboard() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [category, setCategory] = useState("tehnologija");
  const [file, setFile] = useState<File | null>(null);
  const [myPosts, setMyPosts] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [showForm, setShowForm] = useState(false);

  const userId = typeof window !== "undefined" ? localStorage.getItem("userId") : null;
  const username = typeof window !== "undefined" ? localStorage.getItem("username") : null;

  const loadPosts = () => {
    if (!username) return;
    fetch(`${API_BASE}/api/posts/user/${username}`).then((r) => r.json()).then(setMyPosts);
  };

  useEffect(() => {
    loadPosts();
    if (userId) {
      fetch(`${API_BASE}/api/author/stats/${userId}`).then((r) => r.json()).then(setStats);
    }
  }, []);

  const createPost = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userId) return;
    const fd = new FormData();
    fd.append("title", title);
    fd.append("content", content);
    fd.append("author_id", userId);
    fd.append("category", category);
    fd.append("content_type", "clanak");
    if (file) fd.append("file", file);
    await fetch(`${API_BASE}/api/posts`, { method: "POST", body: fd });
    setTitle("");
    setContent("");
    setFile(null);
    setShowForm(false);
    loadPosts();
  };

  const deletePost = (postId: number) => {
    if (!userId || !confirm("Obrisati objavu?")) return;
    fetch(`${API_BASE}/api/posts/${postId}?user_id=${userId}`, { method: "DELETE" }).then(() => loadPosts());
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 20 }}>
      <h1>Autor panel</h1>

      {stats && (
        <div style={{ marginBottom: 20, padding: 12, background: "#f0f9ff" }}>
          <p>Objave: {stats.posts_count} | Pregledi: {stats.total_views} | Lajkovi: {stats.total_likes}</p>
        </div>
      )}

      <button onClick={() => setShowForm(!showForm)} style={{ padding: "8px 16px", marginBottom: 16 }}>
        {showForm ? "Zatvori formu" : "Nova objava"}
      </button>

      {showForm && (
        <form onSubmit={createPost} style={{ border: "1px solid #ddd", padding: 16, marginBottom: 20 }}>
          <p><input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Naslov" required style={{ width: "100%", padding: 8 }} /></p>
          <p><textarea value={content} onChange={(e) => setContent(e.target.value)} placeholder="Sadržaj" required rows={4} style={{ width: "100%", padding: 8 }} /></p>
          <p>
            <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ width: "100%", padding: 8 }}>
              {CATEGORIES.filter((c) => c.value).map((c) => (
                <option key={c.value} value={c.value}>{c.label}</option>
              ))}
            </select>
          </p>
          <p><input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} /></p>
          <button type="submit" style={{ padding: "8px 16px", background: "#0284c7", color: "white", border: "none" }}>Objavi</button>
        </form>
      )}

      <h2>Moje objave</h2>
      {myPosts.map((p) => (
        <div key={p.id} style={{ border: "1px solid #ddd", padding: 12, marginBottom: 8 }}>
          <b>{p.title}</b>
          <p>{p.content}</p>
          {p.file_path && <p><a href={`${API_BASE}/${p.file_path}`} target="_blank">Prilog</a></p>}
          <button onClick={() => deletePost(p.id)} style={{ color: "red" }}>Obriši</button>
        </div>
      ))}
    </div>
  );
}
