# 👑 RR PressureIQ 2027 | Premium Cricket Analytics & Auction Intelligence War Room

An executive-tier cricket scouting and auction intelligence war room engineered for the **Rajasthan Royals "SupeRR Selector" (Round 1: Identify the Most Reliable Players Under Pressure)** competition.

Built with **Streamlit**, **Plotly**, and **Pandas**, formatted in a luxury franchise war-room aesthetic (Rajasthan Royals Pink `#E80071`, Midnight Navy `#0A1128`, and Championship Gold `#F59E0B`).

---

## 🌟 Upgraded Capabilities & Features

### 1. 📂 Dual-Mode Real Data Ingestion
* **Pre-Loaded Official Candidate Pool**: 226 verified international and domestic stars enriched with handedness, tactical specializations, estimated auction valuation brackets, and Rajasthan Royals strategic fit ratings (0–100).
* **Live Unstop Data Pack Dropzone**: Drag and drop any raw domestic league CSV or updated Unstop brief dataset directly from the sidebar. The engine auto-detects schema columns (`player_name`, `category`, `runs`, `balls`, `SR`, `economy`, `delta`, `consistency`) and regenerates the war room on the fly.

### 2. 🧍 360° Interactive Player Scouting Dossiers
* **6-Axis Pressure DNA Radar Chart**:
  * Clutch Output (Pressure SR / Economy)
  * Baseline Uplift (Delta vs Normal Baseline)
  * Sample Depth & Empirical Authority
  * Match Consistency Rate (% high-pressure appearances with positive impact)
  * Big-Stage IPL Exposure
  * Rajasthan Royals Tactical Synergy
* **Comparative Pressure vs Baseline Bar Charts**
* **Scout's Executive Memo**: Explicit breakdown of player superpowers, tactical blindspots, recommended auction bidding ceilings, and specific assigned role in RR's setup.

### 3. ⚖️ Multi-Player Comparison Studio
* Select **up to 4 candidates** simultaneously.
* **Overlaid Radar Comparisons**: Normalized on identical axes to eliminate misleading scale discrepancies.
* **Head-to-Head Comparative Duel Matrix**: Highlights category leaders in pressure strike rate, death economy, sample reliability, and auction price-to-performance efficiency.
* **Algorithmic Scout Verdict**: Recommends the optimal player to prioritize based on franchise balance.

### 4. 🎯 Auction Intelligence Board (4 Strategic Tiers)
* 🌟 **Tier 1: Marquee Priority Targets**: Proven big-stage IPL match-winners worth aggressive bidding.
* 💎 **Tier 2: High-Value Moneyball Picks**: Undervalued domestic performers with massive delta uplifts, high consistency, and budget-friendly price tags.
* ⚡ **Tier 3: High-Upside Punts**: High-ceiling prospects for backup depth and late-overs acceleration.
* ⚠️ **Tier 4: Caution / Overpriced Traps**: Recognizable names that show negative deltas under intense pressure.
* **Target Bid Estimation & Exportable CSV** for franchise war-room printouts.

### 5. 🧩 Squad Combination Simulator (RR 2027 Playing XI Builder)
* Real-world IPL Roster Rules enforcement:
  * **Overseas Player Cap**: Maximum 4 overseas players in the Playing XI (with instant warning alerts if violated).
  * **Role Balance Validation**: 6 Batters / All-Rounders + 5 Bowling Options (with Wicketkeeper checks).
* Live Calculated Performance Gauges:
  * **Team Pressure Resistance Index (TPRI)** (0–100).
  * **Projected Total XI Outlay** vs ₹100.00 Cr Auction Purse Cap.
* **Pre-Configured Franchise Blueprints**: One-click presets for *"The RR 2027 Clutch & Death Wall XI"* and *"The High-Value Domestic Core XI"*.
* **One-Click Squad Export** to CSV.

### 6. ⚠️ Player Risk Register & 2x2 Quadrant Matrix
* **Risk vs Reward Quadrant Scatter**:
  * *Quadrant 1 (Top Left)*: Proven Low-Risk Superstars.
  * *Quadrant 2 (Top Right)*: High-Reward Punts.
  * *Quadrant 3 (Bottom Left)*: Steady Floor Accumulators.
  * *Quadrant 4 (Bottom Right)*: Fragile Traps.
* Granular risk diagnostics: Sample Size Penalties ($n < 100$ balls), Negative Baseline Regressors, and Domestic-to-IPL Transferability Risks.

### 7. 📘 The Winning Methodology & Pitch
* Complete executive brief explaining the mathematical formulation of PressureIQ:
  * High-Leverage State Criteria (Overs 16–20, RRR > 9.5, Powerplay collapse $< 40/3$).
  * Bayesian Shrinkage Regularization ($S_{adj} = \frac{n}{n+100} S_{raw} + \frac{100}{n+100} \mu$).
  * Why our top picks (**Donovan Ferreira**, **Shashank Singh**, **Matheesha Pathirana**, **Eshan Malinga**) address Rajasthan Royals' specific historical vulnerabilities.

---

## 🚀 How to Run Locally

1. Install Python 3.10 or newer.
2. Open terminal in this directory:
   ```bash
   cd e:\RR_PressureIQ_Dashboard
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

---

## 🌐 How to Deploy to Streamlit Community Cloud (Free & Instant)

1. Create a new GitHub repository (e.g. `RR-PressureIQ-2027`).
2. Push or upload these files to GitHub:
   * `app.py`
   * `requirements.txt`
   * `README.md`
   * `.streamlit/` (contains `config.toml`)
   * `data/` (contains all CSVs and methodology PDF)
3. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
4. Click **New app**, select your repository, set branch to `main`, and main file path to `app.py`.
5. Click **Deploy!**
6. Copy your public URL (e.g. `https://rr-pressureiq-2027.streamlit.app`) and submit it in the Unstop dashboard link field.

---

## 🏆 How to Win the Unstop Rajasthan Royals Competition

To score in the top 1% of submissions:
1. **Highlight the Tactical Fit for RR**: Don't just present raw data; explain *where Rajasthan Royals bleed*. RR's primary historical pain points are:
   - Death bowling leakage in overs 17–20 (solved by Matheesha Pathirana and Eshan Malinga).
   - High-RRR finishing at #6/7 when Samson or Parag depart (solved by Shashank Singh and Donovan Ferreira).
2. **Defend Domestic Transferability**: Explicitly address why domestic league metrics must be discounted when facing 145+ kph express pace in the IPL, and demonstrate how Bayesian shrinkage penalizes noisy small samples.
3. **Show Purse Discipline**: Demonstrate that by picking high-value domestic performers (like Shashank Singh or Donovan Ferreira at ₹3–6 Cr), RR preserves ₹12–15 Cr to acquire an elite death specialist (like Pathirana or Bumrah).
