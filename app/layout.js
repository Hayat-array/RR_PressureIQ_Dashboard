import "./globals.css";

export const metadata = {
  title: "RR PressureIQ 2027 | Auction Intelligence War Room",
  description:
    "High-leverage analytical decision engine identifying the most reliable clutch match-winners for Rajasthan Royals at the IPL 2027 mega-auction.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#070B14] text-[#F3F4F6] min-h-screen antialiased selection:bg-[#E80071] selection:text-white">
        {children}
      </body>
    </html>
  );
}
