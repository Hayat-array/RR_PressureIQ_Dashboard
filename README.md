<<<<<<< HEAD
# 👑 RR PressureIQ 2027 | Premium Cricket Analytics & Auction Intelligence War Room

An executive-tier cricket scouting and auction intelligence war room engineered for the **Rajasthan Royals "SupeRR Selector" (Round 1: Identify the Most Reliable Players Under Pressure)** competition.

This repository now provides a **modern Next.js 14 + React + Python (FastAPI)** architecture ready for instant deployment on **Vercel** (with backwards-compatible Streamlit support).

---

## 🏗️ Architecture: Next.js + React + Python on Vercel

```
RR_PressureIQ_Dashboard/
├── app/                              # Next.js App Router (React)
│   ├── layout.js                     # Root layout & Google Fonts
│   ├── globals.css                   # Tailwind dark luxury war-room styling
│   └── page.js                       # 7-Tab Interactive War Room UI
├── api/                              # Python Backend Serverless Functions
│   └── index.py                      # FastAPI REST API (/api/candidates, /api/squad-simulate)
├── public/                           # Static assets & offline JSON fallbacks
│   └── data/candidates.json          # Instant zero-latency pre-rendered dataset
├── data/                             # Raw CSV & methodology documents
│   ├── RR_PressureIQ_Enriched_Candidates.csv
│   ├── RR_PressureIQ_Full_Candidate_Rankings.csv
│   └── SupeRR_Round1_Methodology_Report.pdf
├── vercel.json                       # Vercel serverless routing configuration
├── next.config.mjs                   # Next.js API rewrites
├── tailwind.config.js                # Official Rajasthan Royals brand theme
├── package.json                      # Next.js & React dependencies
└── requirements.txt                  # Python dependencies for FastAPI backend
```

---

## ⚡ How to Run Locally

### 1. Run the Next.js Frontend
```bash
npm run dev
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser.

### 2. (Optional) Run Python FastAPI Backend locally
```bash
npm run dev:python
```
FastAPI runs on **`http://127.0.0.1:8000`** with interactive API docs at **`http://127.0.0.1:8000/docs`**.

---

## 🚀 How to Deploy to Vercel (Instant & Free)

### Option A: Via GitHub (Recommended)
1. Push this repository to GitHub:
   ```bash
   git add .
   git commit -m "feat: upgraded RR PressureIQ with Next.js, React and Python API"
   git push origin main
   ```
2. Go to [vercel.com](https://vercel.com/) and click **Add New Project**.
3. Import your GitHub repository.
4. Vercel automatically detects Next.js:
   * **Framework Preset:** Next.js
   * **Root Directory:** `./`
5. Click **Deploy**!
6. Copy your live Vercel URL (e.g. `https://rr-pressureiq-2027.vercel.app`) and submit it on Unstop!

### Option B: Via Vercel CLI
```bash
npm i -g vercel
vercel
```

---

## 🌟 Upgraded Dashboard Features

1. **🏆 Candidate Leaderboard & Spotlight**: Top 3 Pressure Titans, delta vs baseline, and searchable 226-player roster.
2. **🧍 360° Player Dossier**: 6-Axis SVG Pressure DNA Radar, baseline comparison bars, and tactical scout memos.
3. **⚖️ Multi-Player Comparison Studio**: Select up to 4 players simultaneously with overlaid multi-radar charts and head-to-head verdicts.
4. **🎯 Auction Intelligence Board**: 4 Strategic Tiers (Marquee Priority, Moneyball Value, High-Upside Punts, Trap Risks) with purse planning.
5. **🧩 Squad Combination Simulator**: 11-player Playing XI builder with real IPL rules (max 4 overseas enforcement, TPRI calculation, preset lineups).
6. **⚠️ Player Risk Matrix**: Identifies sample size liabilities, domestic-to-IPL transferability risks, and baseline regressors.
7. **📘 The Winning Pitch Deck**: Academic and mathematical framework answering the Rajasthan Royals Unstop brief.
=======
# RR_PressureIQ_Dashboard
>>>>>>> origin/main
