"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { API_BASE } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch(`${API_BASE}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Greška pri prijavi");
        return;
      }
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("role", data.role);
      localStorage.setItem("username", data.username);
      localStorage.setItem("userId", String(data.user_id));
      localStorage.setItem("userEmail", data.email);

      if (data.role === "administrator") router.push("/admin");
      else if (data.role === "autor") router.push("/author/dashboard");
      else router.push("/");
    } catch {
      setError(`Backend nije dostupan. Pokreni backend na ${API_BASE}`);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "50px auto", padding: 20 }}>
      <h1>Prijava</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <p><input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Korisničko ime" required style={{ width: "100%", padding: 8 }} /></p>
        <p><input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Lozinka" required style={{ width: "100%", padding: 8 }} /></p>
        <button type="submit" style={{ padding: "8px 16px", background: "#0284c7", color: "white", border: "none" }}>Prijavi se</button>
      </form>
      <p style={{ marginTop: 12 }}>Nemaš nalog? <Link href="/register">Registracija</Link></p>
    </div>
  );
}
