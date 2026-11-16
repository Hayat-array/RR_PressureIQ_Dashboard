import os
import json
import math
from pathlib import Path
from typing import List, Optional
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="RR PressureIQ 2027 API", version="1.0.0")

# Enable CORS for Next.js development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ENRICHED_CSV = DATA_DIR / "RR_PressureIQ_Enriched_Candidates.csv"
FULL_CSV = DATA_DIR / "RR_PressureIQ_Full_Candidate_Rankings.csv"

def load_data():
    if ENRICHED_CSV.exists():
        df = pd.read_csv(ENRICHED_CSV, encoding="utf-8")
    elif FULL_CSV.exists():
        df = pd.read_csv(FULL_CSV, encoding="utf-8-sig")
        df.columns = [c.replace("\ufeff", "") for c in df.columns]
    else:
        raise FileNotFoundError("Candidate dataset not found in data/ directory.")
    df.columns = [c.strip().replace("\ufeff", "") for c in df.columns]
    # Replace NaN with appropriate defaults
    df = df.fillna({
        "country": "India",
        "is_overseas": "No",
        "estimated_price_cr": 4.0,
        "rr_tactical_fit": 80,
        "auction_tier": "Tier 2: High-Value Moneyball",
        "risk_score": 25,
        "scout_verdict": "Solid clutch prospect."
    })
    return df

try:
    df_global = load_data()
except Exception as e:
    df_global = pd.DataFrame()

@app.get("/api/health")
def health():
    return {"status": "ok", "total_candidates": len(df_global)}

@app.get("/api/candidates")
def get_candidates(
    role: Optional[str] = None,
    origin: Optional[str] = None,
    tier: Optional[str] = None,
    search: Optional[str] = None,
    min_balls: int = 0,
    min_matches: int = 0
):
    df = df_global.copy()
    if df.empty:
        return {"data": []}
    
    if role and role.lower() in ["batter", "bowler"]:
        df = df[df["category"].str.lower() == role.lower()]
        
    if origin:
        if origin.lower() == "domestic":
            df = df[df["is_overseas"] == "No"]
        elif origin.lower() == "overseas":
            df = df[df["is_overseas"] == "Yes"]
            
    if tier and tier != "All Tiers":
        df = df[df["auction_tier"] == tier]
        
    if search:
        df = df[df["player_name"].str.contains(search, case=False, na=False)]
        
    df = df[(df["pressure_balls"] >= min_balls) & (df["pressure_matches"] >= min_matches)]
    df = df.sort_values("model_score", ascending=False)
    
    records = df.to_dict(orient="records")
    return {"total": len(records), "data": records}

@app.get("/api/player/{player_name}")
def get_player(player_name: str):
    match = df_global[df_global["player_name"].str.lower() == player_name.lower()]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found.")
    return match.iloc[0].to_dict()

@app.get("/api/top-titans")
def get_top_titans(role: Optional[str] = None):
    df = df_global.copy()
    if role and role.lower() in ["batter", "bowler"]:
        df = df[df["category"].str.lower() == role.lower()]
    top = df.sort_values("model_score", ascending=False).head(3)
    return {"data": top.to_dict(orient="records")}

class SquadSimRequest(BaseModel):
    selected_players: List[str]

@app.post("/api/squad-simulate")
def simulate_squad(req: SquadSimRequest):
    sub = df_global[df_global["player_name"].isin(req.selected_players)]
    
    total_selected = len(sub)
    overseas_count = len(sub[sub["is_overseas"] == "Yes"])
    batters_count = len(sub[sub["category"].str.lower() == "batter"])
    bowlers_count = len(sub[sub["category"].str.lower() == "bowler"])
    total_cost = float(sub["estimated_price_cr"].sum()) if "estimated_price_cr" in sub.columns else 0.0
    avg_score = float(sub["model_score"].mean()) if total_selected > 0 else 0.0
    tpri = round(avg_score * 100, 1)
    
    is_valid = (total_selected == 11) and (overseas_count <= 4)
    violations = []
    if overseas_count > 4:
        violations.append(f"Exceeded maximum overseas slots ({overseas_count}/4).")
    if total_selected != 11:
        violations.append(f"Squad size is {total_selected}/11.")
        
    return {
        "total_selected": total_selected,
        "overseas_count": overseas_count,
        "batters_count": batters_count,
        "bowlers_count": bowlers_count,
        "total_cost_cr": round(total_cost, 2),
        "remaining_purse_cr": round(100.0 - total_cost, 2),
        "tpri": tpri,
        "is_valid": is_valid,
        "violations": violations,
        "lineup": sub.to_dict(orient="records")
    }
