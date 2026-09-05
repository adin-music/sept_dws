import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: "AI Knowledge Sharing",
  description: "Platforma za dijeljenje znanja",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="bs">
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
