import "./globals.css";

export const metadata = {
  title: "RR PressureIQ 2027 | Auction Intelligence War Room",
  description: "High-leverage analytical decision engine identifying the most reliable clutch match-winners for Rajasthan Royals at the IPL 2027 mega-auction.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body className="bg-[#070B14] text-[#F3F4F6] min-h-screen antialiased selection:bg-[#E80071] selection:text-white">
        {children}
      </body>
    </html>
  );
}
