"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { API_BASE } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("citalac");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch(`${API_BASE}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password, role }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(typeof data.detail === "string" ? data.detail : "Greška pri registraciji");
        return;
      }
      router.push("/login");
    } catch {
      setError(`Backend nije dostupan. Pokreni: uvicorn main:app --reload (${API_BASE})`);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "50px auto", padding: 20 }}>
      <h1>Registracija</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <p><input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Korisničko ime" required style={{ width: "100%", padding: 8 }} /></p>
        <p><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required style={{ width: "100%", padding: 8 }} /></p>
        <p><input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Lozinka" required style={{ width: "100%", padding: 8 }} /></p>
        <p>
          <select value={role} onChange={(e) => setRole(e.target.value)} style={{ width: "100%", padding: 8 }}>
            <option value="citalac">Čitalac</option>
            <option value="autor">Autor</option>
          </select>
        </p>
        <button type="submit" style={{ padding: "8px 16px", background: "#0284c7", color: "white", border: "none" }}>Registruj se</button>
      </form>
      <p style={{ marginTop: 12 }}>Već imaš nalog? <Link href="/login">Prijava</Link></p>
    </div>
  );
}
