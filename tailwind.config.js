/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        rr: {
          pink: "#E80071",
          "pink-light": "#FF4D9E",
          "pink-dark": "#B80059",
          navy: "#0A1128",
          dark: "#070B14",
          card: "rgba(13, 20, 36, 0.75)",
          gold: "#F59E0B",
          emerald: "#10B981",
          cyan: "#06B6D4",
        },
      },
      fontFamily: {
        sans: ["Plus Jakarta Sans", "system-ui", "sans-serif"],
        display: ["Space Grotesk", "sans-serif"],
      },
    },
  },
  plugins: [],
};
