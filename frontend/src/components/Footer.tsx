import Link from "next/link";

export default function Footer() {
  return (
    <footer style={{ background: "#1a1a1a", color: "#aaa", padding: 20, marginTop: 40, textAlign: "center" }}>
      <p>KnowledgeHub - platforma za dijeljenje znanja</p>
      <p>
        <Link href="/about" style={{ color: "#aaa", marginRight: 10 }}>O nama</Link>
        <Link href="/contact" style={{ color: "#aaa" }}>Kontakt</Link>
      </p>
    </footer>
  );
}
