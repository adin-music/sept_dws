"use client";

import { useEffect, useState } from "react";
import { API_BASE } from "@/lib/api";

export default function ProfilePage() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");
  const [posts, setPosts] = useState<any[]>([]);

  useEffect(() => {
    const id = localStorage.getItem("userId");
    setUsername(localStorage.getItem("username") || "");
    setEmail(localStorage.getItem("userEmail") || "");
    setRole(localStorage.getItem("role") || "");
    if (id && localStorage.getItem("role") === "autor") {
      fetch(`${API_BASE}/api/posts/author/${id}`).then((r) => r.json()).then(setPosts);
    }
  }, []);

  const deletePost = (postId: number) => {
    const userId = localStorage.getItem("userId");
    if (!confirm("Obrisati objavu?")) return;
    fetch(`${API_BASE}/api/posts/${postId}?user_id=${userId}`, { method: "DELETE" }).then(() => {
      setPosts(posts.filter((p) => p.id !== postId));
    });
  };

  return (
    <div style={{ maxWidth: 600, margin: "0 auto", padding: 20 }}>
      <h1>Profil</h1>
      <p>Korisničko ime: {username}</p>
      <p>Email: {email}</p>
      <p>Uloga: {role}</p>

      {posts.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <h2>Moje objave</h2>
          {posts.map((p) => (
            <div key={p.id} style={{ border: "1px solid #ddd", padding: 8, marginBottom: 8 }}>
              <b>{p.title}</b>
              <p>{p.content}</p>
              <button onClick={() => deletePost(p.id)} style={{ color: "red" }}>Obriši</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
