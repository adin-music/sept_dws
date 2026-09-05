"use client";

import { useEffect, useState } from "react";
import { API_BASE } from "@/lib/api";

type Post = {
  id: number;
  title: string;
  content: string;
  author_username?: string;
  likes_count?: number;
  file_path?: string;
};

type Comment = {
  id: number;
  username?: string;
  text: string;
};

export default function PostFeed({ mode = "all", category = "" }: { mode?: string; category?: string }) {
  const [posts, setPosts] = useState<Post[]>([]);
  const [comments, setComments] = useState<{ [key: number]: Comment[] }>({});
  const [loading, setLoading] = useState(true);
  const [comment, setComment] = useState<{ [key: number]: string }>({});

  const loadPosts = () => {
    setLoading(true);
    const userId = localStorage.getItem("userId");
    let url = `${API_BASE}/api/posts`;

    if (mode === "recommended" && userId) {
      url = `${API_BASE}/api/recommendations/${userId}`;
    } else if (mode === "saved" && userId) {
      url = `${API_BASE}/api/posts/saved/${userId}`;
    } else if (category) {
      url = `${API_BASE}/api/posts?category=${category}`;
    }

    fetch(url)
      .then((r) => r.json())
      .then(async (data) => {
        const list = Array.isArray(data) ? data : [];
        setPosts(list);
        const allComments: { [key: number]: Comment[] } = {};
        for (const p of list) {
          const cRes = await fetch(`${API_BASE}/api/posts/${p.id}/comments`);
          if (cRes.ok) allComments[p.id] = await cRes.json();
        }
        setComments(allComments);
      })
      .catch(() => setPosts([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadPosts();
  }, [mode, category]);

  const like = (postId: number) => {
    const userId = localStorage.getItem("userId");
    if (!userId) {
      alert("Morate biti prijavljeni");
      return;
    }
    fetch(`${API_BASE}/api/posts/${postId}/like`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: parseInt(userId) }),
    }).then(() => loadPosts());
  };

  const save = async (postId: number) => {
    const userId = localStorage.getItem("userId");
    if (!userId) {
      alert("Morate biti prijavljeni");
      return;
    }
    await fetch(`${API_BASE}/api/posts/${postId}/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: parseInt(userId) }),
    });
    alert("Objava je u Moje kolekcije");
    loadPosts();
  };

  const sendComment = (postId: number) => {
    const userId = localStorage.getItem("userId");
    const text = comment[postId];
    if (!userId || !text) return;
    fetch(`${API_BASE}/api/posts/${postId}/comment`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: parseInt(userId), text }),
    }).then(() => {
      setComment({ ...comment, [postId]: "" });
      loadPosts();
    });
  };

  if (loading) return <p>Učitavanje...</p>;
  if (posts.length === 0) return <p>Nema objava.</p>;

  return (
    <div>
      {posts.map((post) => (
        <div key={post.id} style={{ border: "1px solid #ddd", padding: 16, marginBottom: 12, background: "white" }}>
          <p style={{ fontSize: 12, color: "#666" }}>{post.author_username}</p>
          <h3>{post.title}</h3>
          <p>{post.content}</p>
          {post.file_path && (
            <p>
              <a href={`${API_BASE}/${post.file_path}`} target="_blank" rel="noreferrer">Otvori prilog</a>
            </p>
          )}
          <p style={{ fontSize: 12 }}>Lajkovi: {post.likes_count || 0}</p>
          <button onClick={() => like(post.id)} style={{ marginRight: 8 }}>Lajk</button>
          <button onClick={() => save(post.id)}>Sačuvaj u kolekcije</button>
          <div style={{ marginTop: 8 }}>
            <input
              value={comment[post.id] || ""}
              onChange={(e) => setComment({ ...comment, [post.id]: e.target.value })}
              placeholder="Komentar..."
              style={{ padding: 4, marginRight: 8 }}
            />
            <button onClick={() => sendComment(post.id)}>Pošalji</button>
          </div>
          {(comments[post.id] || []).map((c) => (
            <p key={c.id} style={{ fontSize: 12, marginTop: 4 }}>
              <b>{c.username}:</b> {c.text}
            </p>
          ))}
        </div>
      ))}
    </div>
  );
}
