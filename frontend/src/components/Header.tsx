"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Header() {
  const router = useRouter();
  const [role, setRole] = useState("");

  useEffect(() => {
    setRole(localStorage.getItem("role") || "");
  }, []);

  const logout = () => {
    localStorage.clear();
    router.push("/login");
  };

  return (
    <header style={{ background: "#0284c7", color: "white", padding: "12px 20px" }}>
      <div style={{ maxWidth: 900, margin: "0 auto", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <Link href="/" style={{ color: "white", fontWeight: "bold", fontSize: 20 }}>KnowledgeHub</Link>
        <nav style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <Link href="/" style={{ color: "white" }}>Početna</Link>
          {role && <Link href="/collections" style={{ color: "white" }}>Kolekcije</Link>}
          {role && role !== "administrator" && <Link href="/profile" style={{ color: "white" }}>Profil</Link>}
          {role === "autor" && <Link href="/author/dashboard" style={{ color: "white" }}>Autor panel</Link>}
          {role === "administrator" && <Link href="/admin" style={{ color: "white" }}>Admin</Link>}
          {role ? (
            <button onClick={logout} style={{ background: "#dc2626", color: "white", border: "none", padding: "6px 12px", cursor: "pointer" }}>Odjava</button>
          ) : (
            <>
              <Link href="/login" style={{ color: "white" }}>Prijava</Link>
              <Link href="/register" style={{ color: "white" }}>Registracija</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
