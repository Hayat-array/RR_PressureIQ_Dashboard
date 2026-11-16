"use client";

export const dynamic = "force-dynamic";

import React, { useState, useMemo, useEffect } from "react";
import initialCandidates from "@/data/candidates.json";
import {
  Trophy,
  User,
  GitCompare,
  Target,
  Users,
  AlertTriangle,
  BookOpen,
  Search,
  Download,
  ShieldAlert,
  Sparkles,
  ChevronRight,
  TrendingUp,
  Activity,
  Layers,
  CheckCircle2,
  AlertCircle
} from "lucide-react";

// --- SVG Radar Chart Component ---
function RadarChart({ datasets, size = 320 }) {
  const center = size / 2;
  const radius = (size / 2) - 45;
  const axes = [
    { label: "Clutch Output", key: "radar_output" },
    { label: "Baseline Uplift", key: "radar_delta" },
    { label: "Sample Depth", key: "radar_sample" },
    { label: "Consistency", key: "radar_consistency" },
    { label: "IPL Big Stage", key: "radar_ipl" },
    { label: "RR Synergy", key: "radar_synergy" },
  ];
  const numAxes = axes.length;
  const angleStep = (Math.PI * 2) / numAxes;

  const circles = [0.25, 0.5, 0.75, 1.0];

  const getCoordinates = (value, index) => {
    const angle = index * angleStep - Math.PI / 2;
    const r = (Math.max(0, Math.min(100, value || 0)) / 100) * radius;
    return {
      x: center + r * Math.cos(angle),
      y: center + r * Math.sin(angle),
    };
  };

  const colors = [
    { stroke: "#E80071", fill: "rgba(232, 0, 113, 0.25)" },
    { stroke: "#06B6D4", fill: "rgba(6, 182, 212, 0.25)" },
    { stroke: "#F59E0B", fill: "rgba(245, 158, 11, 0.25)" },
    { stroke: "#10B981", fill: "rgba(16, 185, 129, 0.25)" },
  ];

  return (
    <svg width={size} height={size} className="mx-auto overflow-visible select-none">
      {/* Background Web */}
      {circles.map((frac, i) => (
        <circle
          key={i}
          cx={center}
          cy={center}
          r={radius * frac}
          fill="none"
          stroke="rgba(255, 255, 255, 0.08)"
          strokeDasharray={frac < 1 ? "3 3" : undefined}
        />
      ))}

      {/* Axis Lines & Labels */}
      {axes.map((axis, i) => {
        const outer = getCoordinates(100, i);
        const labelPos = getCoordinates(118, i);
        return (
          <g key={i}>
            <line
              x1={center}
              y1={center}
              x2={outer.x}
              y2={outer.y}
              stroke="rgba(255, 255, 255, 0.12)"
            />
            <text
              x={labelPos.x}
              y={labelPos.y}
              textAnchor="middle"
              dominantBaseline="middle"
              className="text-[10px] font-medium fill-slate-300"
            >
              {axis.label}
            </text>
          </g>
        );
      })}

      {/* Polygons */}
      {datasets.map((d, dIdx) => {
        const color = colors[dIdx % colors.length];
        const points = axes
          .map((axis, i) => {
            const coord = getCoordinates(d.player[axis.key], i);
            return `${coord.x},${coord.y}`;
          })
          .join(" ");

        return (
          <g key={dIdx}>
            <polygon
              points={points}
              fill={color.fill}
              stroke={color.stroke}
              strokeWidth={2.5}
            />
            {axes.map((axis, i) => {
              const coord = getCoordinates(d.player[axis.key], i);
              return (
                <circle
                  key={i}
                  cx={coord.x}
                  cy={coord.y}
                  r={3.5}
                  fill={color.stroke}
                />
              );
            })}
          </g>
        );
      })}
    </svg>
  );
}

export default function Dashboard() {
  const [candidates, setCandidates] = useState(initialCandidates);
  const [activeTab, setActiveTab] = useState("leaderboard");
  
  // Scouting Filters
  const [roleFilter, setRoleFilter] = useState("All");
  const [originFilter, setOriginFilter] = useState("All");
  const [tierFilter, setTierFilter] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [minBalls, setMinBalls] = useState(30);

  // Player Dossier
  const [selectedPlayerName, setSelectedPlayerName] = useState(initialCandidates[0]?.player_name || "");

  // Compare Studio
  const [compareList, setCompareList] = useState(["Donovan Ferreira", "Shashank Singh"]);

  // Squad Simulator
  const [simBatters, setSimBatters] = useState([
    "Sanju Samson", "Rinku Singh", "Shashank Singh", "Tristan Stubbs", "Riyan Parag", "Dhruv Jurel"
  ]);
  const [simBowlers, setSimBowlers] = useState([
    "Matheesha Pathirana", "Sandeep Sharma", "Trent Boult", "Rashid Khan", "Arshdeep Singh"
  ]);

  // Filtered dataset
  const filteredCandidates = useMemo(() => {
    return candidates.filter((c) => {
      if (roleFilter !== "All" && c.category.toLowerCase() !== roleFilter.toLowerCase()) return false;
      if (originFilter === "Domestic" && c.is_overseas === "Yes") return false;
      if (originFilter === "Overseas" && c.is_overseas === "No") return false;
      if (tierFilter !== "All" && c.auction_tier !== tierFilter) return false;
      if (c.pressure_balls < minBalls) return false;
      if (searchQuery && !c.player_name.toLowerCase().includes(searchQuery.toLowerCase())) return false;
      return true;
    });
  }, [candidates, roleFilter, originFilter, tierFilter, searchQuery, minBalls]);

  // Top 3 Titans
  const topTitans = useMemo(() => {
    return [...filteredCandidates]
      .sort((a, b) => b.model_score - a.model_score)
      .slice(0, 3);
  }, [filteredCandidates]);

  // Current Dossier Player
  const dossierPlayer = useMemo(() => {
    return candidates.find((c) => c.player_name === selectedPlayerName) || candidates[0];
  }, [candidates, selectedPlayerName]);

  // Compare Candidates Data
  const comparePlayers = useMemo(() => {
    return candidates.filter((c) => compareList.includes(c.player_name));
  }, [candidates, compareList]);

  // Squad Simulator Diagnostics
  const simSquad = useMemo(() => {
    const list = [...simBatters, ...simBowlers];
    return candidates.filter((c) => list.includes(c.player_name));
  }, [candidates, simBatters, simBowlers]);

  const overseasCount = useMemo(() => {
    return simSquad.filter((c) => c.is_overseas === "Yes").length;
  }, [simSquad]);

  const totalPurseCost = useMemo(() => {
    return simSquad.reduce((acc, c) => acc + (c.estimated_price_cr || 0), 0);
  }, [simSquad]);

  const tpriScore = useMemo(() => {
    if (!simSquad.length) return 0;
    const avg = simSquad.reduce((acc, c) => acc + (c.model_score || 0), 0) / simSquad.length;
    return (avg * 100).toFixed(1);
  }, [simSquad]);

  // Export CSV Helper
  const exportCSV = (data, filename) => {
    if (!data.length) return;
    const headers = Object.keys(data[0]).join(",");
    const rows = data.map((obj) => Object.values(obj).map((v) => `"${v}"`).join(","));
    const csvContent = "data:text/csv;charset=utf-8," + [headers, ...rows].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top Command Header */}
      <header className="border-b border-white/10 bg-[#070B14]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-[1560px] mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#E80071] to-[#FF4D9E] flex items-center justify-center font-bold text-lg shadow-lg shadow-[#E80071]/30">
              👑
            </div>
            <div>
              <div className="font-extrabold text-base tracking-tight flex items-center gap-2">
                RAJASTHAN ROYALS <span className="text-[#FF70B8] text-xs px-2 py-0.5 rounded-full bg-[#E80071]/20 border border-[#E80071]/40">WAR ROOM 2027</span>
              </div>
              <div className="text-xs text-slate-400">PressureIQ Analytical Decision Engine · SupeRR Selector Round 1</div>
            </div>
          </div>

          <div className="flex items-center gap-6">
            <div className="text-right hidden sm:block">
              <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">PURSE CAP</div>
              <div className="font-display font-bold text-[#F59E0B] text-lg">₹100.00 Cr</div>
            </div>
            <div className="text-right hidden md:block border-l border-white/10 pl-6">
              <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">OVERSEAS SLOTS</div>
              <div className="font-display font-bold text-[#10B981] text-lg">Max 8 (4 in XI)</div>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Strip */}
      <div className="max-w-[1560px] mx-auto px-4 pt-6 pb-2 w-full">
        <div className="hero-glow rounded-2xl p-6 sm:p-8 relative overflow-hidden">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-[#E80071]/20 border border-[#E80071]/40 text-[#FF70B8] mb-2">
                <Sparkles className="w-3.5 h-3.5" /> High-Leverage Scouting Engine
              </div>
              <h1 className="text-2xl sm:text-4xl font-extrabold text-white tracking-tight font-display">
                PressureIQ <span className="text-[#FF70B8]">2027</span> Intelligence
              </h1>
              <p className="text-sm sm:text-base text-slate-300 max-w-2xl mt-1">
                Isolating true clutch match-winners for Rajasthan Royals at the IPL 2027 mega-auction through role-specific pressure definitions and Bayesian shrinkage.
              </p>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => exportCSV(filteredCandidates, "RR_PressureIQ_Master_Roster.csv")}
                className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-[#E80071] to-[#B80059] text-white font-bold text-xs uppercase tracking-wider flex items-center gap-2 shadow-lg shadow-[#E80071]/30 hover:shadow-[#E80071]/50 transition-all cursor-pointer"
              >
                <Download className="w-4 h-4" /> Export CSV Roster
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* KPI Cards Strip */}
      <div className="max-w-[1560px] mx-auto px-4 py-4 w-full grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        <div className="glass-panel p-4">
          <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Active Pool</div>
          <div className="text-2xl font-bold font-display text-white mt-1">{filteredCandidates.length}</div>
          <div className="text-xs text-[#06B6D4] mt-0.5">Filtered candidates</div>
        </div>
        <div className="glass-panel p-4">
          <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Tier 1 Marquee</div>
          <div className="text-2xl font-bold font-display text-[#FF70B8] mt-1">
            {candidates.filter((c) => c.auction_tier?.includes("Marquee")).length}
          </div>
          <div className="text-xs text-slate-400 mt-0.5">Elite clutch match-winners</div>
        </div>
        <div className="glass-panel p-4">
          <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Moneyball Value</div>
          <div className="text-2xl font-bold font-display text-[#10B981] mt-1">
            {candidates.filter((c) => c.auction_tier?.includes("Moneyball")).length}
          </div>
          <div className="text-xs text-slate-400 mt-0.5">High delta · Low spend</div>
        </div>
        <div className="glass-panel p-4">
          <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Pressure Balls</div>
          <div className="text-2xl font-bold font-display text-white mt-1">
            {filteredCandidates.reduce((acc, c) => acc + (c.pressure_balls || 0), 0).toLocaleString()}
          </div>
          <div className="text-xs text-slate-400 mt-0.5">High-leverage sample</div>
        </div>
        <div className="glass-panel p-4 col-span-2 sm:col-span-1">
          <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Avg PressureIQ</div>
          <div className="text-2xl font-bold font-display text-[#38BDF8] mt-1">
            {(filteredCandidates.reduce((acc, c) => acc + (c.model_score || 0), 0) / (filteredCandidates.length || 1)).toFixed(3)}
          </div>
          <div className="text-xs text-slate-400 mt-0.5">Bayesian shrunk index</div>
        </div>
      </div>

      {/* Main Tabs Navigation */}
      <div className="max-w-[1560px] mx-auto px-4 w-full">
        <div className="flex border-b border-white/10 gap-2 overflow-x-auto pb-px scrollbar-none">
          {[
            { id: "leaderboard", label: "Candidate Leaderboard", icon: Trophy },
            { id: "dossier", label: "360° Player Dossier", icon: User },
            { id: "compare", label: "Multi-Player Compare", icon: GitCompare },
            { id: "auction", label: "Auction Intelligence", icon: Target },
            { id: "simulator", label: "Squad Simulator", icon: Users },
            { id: "risk", label: "Risk Matrix", icon: AlertTriangle },
            { id: "methodology", label: "Winning Pitch", icon: BookOpen },
          ].map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 font-display font-semibold text-sm whitespace-nowrap border-b-2 transition-all cursor-pointer ${
                  active
                    ? "border-[#E80071] text-[#FF70B8] bg-[#E80071]/10 rounded-t-lg"
                    : "border-transparent text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Tab Content */}
      <main className="max-w-[1560px] mx-auto px-4 py-6 w-full flex-1">
        {/* TAB 1: LEADERBOARD */}
        {activeTab === "leaderboard" && (
          <div className="space-y-6">
            {/* Top 3 Titans */}
            <div>
              <div className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-2">
                <Trophy className="w-4 h-4 text-[#F59E0B]" /> Top 3 Pressure Titans in Active Pool
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {topTitans.map((titan, i) => (
                  <div key={titan.player_name} className="glass-panel p-5 border-[#E80071]/40 relative overflow-hidden group">
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="flex gap-1.5 flex-wrap">
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[#E80071]/20 border border-[#E80071]/40 text-[#FF70B8]">
                            {titan.auction_tier}
                          </span>
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-500/20 border border-indigo-500/40 text-indigo-300">
                            {titan.country}
                          </span>
                        </div>
                        <h3 className="text-xl font-bold font-display text-white mt-2 group-hover:text-[#FF70B8] transition-colors">
                          {titan.player_name}
                        </h3>
                        <p className="text-xs text-slate-400">{titan.category} · {titan.skill_specialization}</p>
                      </div>
                      <div className="text-right">
                        <div className="text-[10px] uppercase font-bold text-slate-400">PressureIQ</div>
                        <div className="text-2xl font-black font-display text-[#FF70B8]">{titan.model_score.toFixed(3)}</div>
                      </div>
                    </div>
                    <hr className="border-white/5 my-3" />
                    <div className="grid grid-cols-3 gap-2 text-center text-xs">
                      <div>
                        <div className="text-[10px] text-slate-400">OUTPUT</div>
                        <div className="font-bold text-[#06B6D4] font-display text-sm">{titan.pressure_strike_rate_or_economy.toFixed(1)}</div>
                        <div className="text-[9px] text-slate-500">{titan.category === 'Batter' ? 'SR' : 'Econ'}</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-400">UPLIFT</div>
                        <div className={`font-bold font-display text-sm ${titan.change_vs_baseline > 0 ? 'text-[#10B981]' : 'text-red-400'}`}>
                          {titan.change_vs_baseline > 0 ? `+${titan.change_vs_baseline.toFixed(1)}` : titan.change_vs_baseline.toFixed(1)}
                        </div>
                        <div className="text-[9px] text-slate-500">Delta</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-400">CONSISTENCY</div>
                        <div className="font-bold text-[#F59E0B] font-display text-sm">{titan.consistency_pct.toFixed(0)}%</div>
                        <div className="text-[9px] text-slate-500">Match Rate</div>
                      </div>
                    </div>
                    <div className="mt-3 text-xs text-slate-300 bg-black/20 p-2.5 rounded-lg border border-white/5">
                      🎯 <b>RR Fit:</b> {titan.scout_verdict}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Filter Bar */}
            <div className="glass-panel p-4 flex flex-wrap items-center gap-4">
              <div className="flex-1 min-w-[200px] relative">
                <Search className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search candidate name..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-4 py-2 bg-black/30 border border-white/10 rounded-xl text-sm focus:outline-none focus:border-[#E80071]"
                />
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400 font-semibold">Role:</span>
                {["All", "Batter", "Bowler"].map((r) => (
                  <button
                    key={r}
                    onClick={() => setRoleFilter(r)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold cursor-pointer transition-colors ${
                      roleFilter === r ? "bg-[#E80071] text-white" : "bg-white/5 text-slate-400 hover:text-white"
                    }`}
                  >
                    {r}
                  </button>
                ))}
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400 font-semibold">Origin:</span>
                {["All", "Domestic", "Overseas"].map((o) => (
                  <button
                    key={o}
                    onClick={() => setOriginFilter(o)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold cursor-pointer transition-colors ${
                      originFilter === o ? "bg-[#06B6D4] text-white" : "bg-white/5 text-slate-400 hover:text-white"
                    }`}
                  >
                    {o}
                  </button>
                ))}
              </div>
            </div>

            {/* Candidate Table */}
            <div className="glass-panel overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-black/30 text-slate-400 border-b border-white/10 uppercase tracking-wider font-semibold">
                    <tr>
                      <th className="py-3 px-4">Rank</th>
                      <th className="py-3 px-4">Player</th>
                      <th className="py-3 px-4">Role</th>
                      <th className="py-3 px-4">Origin</th>
                      <th className="py-3 px-4 text-right">PressureIQ</th>
                      <th className="py-3 px-4 text-right">Pressure Output</th>
                      <th className="py-3 px-4 text-right">Delta vs Base</th>
                      <th className="py-3 px-4 text-right">Consistency</th>
                      <th className="py-3 px-4 text-right">Balls</th>
                      <th className="py-3 px-4 text-right">Est. Price</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {filteredCandidates.map((c) => (
                      <tr
                        key={c.player_name}
                        onClick={() => {
                          setSelectedPlayerName(c.player_name);
                          setActiveTab("dossier");
                        }}
                        className="hover:bg-white/5 cursor-pointer transition-colors"
                      >
                        <td className="py-3 px-4 font-bold text-slate-400">#{c.rank}</td>
                        <td className="py-3 px-4 font-bold text-white flex items-center gap-2">
                          {c.player_name}
                          {c.is_overseas === "Yes" && (
                            <span className="text-[10px] px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-normal">OS</span>
                          )}
                        </td>
                        <td className="py-3 px-4 text-slate-300">{c.category}</td>
                        <td className="py-3 px-4 text-slate-400">{c.country}</td>
                        <td className="py-3 px-4 text-right font-black font-display text-[#FF70B8]">{c.model_score.toFixed(3)}</td>
                        <td className="py-3 px-4 text-right font-bold text-[#06B6D4] font-display">{c.pressure_strike_rate_or_economy.toFixed(1)}</td>
                        <td className={`py-3 px-4 text-right font-bold ${c.change_vs_baseline > 0 ? "text-[#10B981]" : "text-red-400"}`}>
                          {c.change_vs_baseline > 0 ? `+${c.change_vs_baseline.toFixed(1)}` : c.change_vs_baseline.toFixed(1)}
                        </td>
                        <td className="py-3 px-4 text-right text-slate-300">{c.consistency_pct.toFixed(0)}%</td>
                        <td className="py-3 px-4 text-right text-slate-400">{c.pressure_balls}</td>
                        <td className="py-3 px-4 text-right font-bold text-[#F59E0B]">₹{c.estimated_price_cr?.toFixed(1)} Cr</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: 360° PLAYER DOSSIER */}
        {activeTab === "dossier" && (
          <div className="space-y-6">
            <div className="flex items-center gap-4">
              <span className="text-xs text-slate-400 font-bold uppercase">Select Player to Inspect:</span>
              <select
                value={selectedPlayerName}
                onChange={(e) => setSelectedPlayerName(e.target.value)}
                className="bg-[#0e1424] border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-[#E80071]"
              >
                {candidates.map((c) => (
                  <option key={c.player_name} value={c.player_name}>
                    {c.player_name} ({c.category} · {c.country})
                  </option>
                ))}
              </select>
            </div>

            {/* Dossier Card */}
            <div className="glass-panel p-6 border-[#E80071]/30">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <div className="flex gap-2 mb-2">
                    <span className="px-2.5 py-0.5 rounded text-xs font-bold bg-[#E80071]/20 border border-[#E80071]/40 text-[#FF70B8]">
                      {dossierPlayer.auction_tier}
                    </span>
                    <span className="px-2.5 py-0.5 rounded text-xs font-bold bg-indigo-500/20 border border-indigo-500/40 text-indigo-300">
                      {dossierPlayer.is_overseas === "Yes" ? "Overseas" : "Domestic (India)"}
                    </span>
                    <span className="px-2.5 py-0.5 rounded text-xs font-bold bg-[#10B981]/20 border border-[#10B981]/40 text-[#34D399]">
                      {dossierPlayer.phase_specialization}
                    </span>
                  </div>
                  <h2 className="text-3xl font-extrabold font-display text-white">{dossierPlayer.player_name}</h2>
                  <p className="text-sm text-slate-400 mt-1">
                    {dossierPlayer.country} · {dossierPlayer.category} · {dossierPlayer.skill_specialization} · {dossierPlayer.batting_style} / {dossierPlayer.bowling_style}
                  </p>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-right">
                    <div className="text-xs text-slate-400 font-bold uppercase">EST. AUCTION PRICE</div>
                    <div className="text-2xl font-bold font-display text-[#F59E0B]">₹{dossierPlayer.estimated_price_cr?.toFixed(1)} Cr</div>
                  </div>
                  <div className="text-right border-l border-white/10 pl-6">
                    <div className="text-xs text-slate-400 font-bold uppercase">RR TACTICAL FIT</div>
                    <div className="text-2xl font-bold font-display text-[#FF70B8]">{dossierPlayer.rr_tactical_fit}/100</div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
                {/* Radar Chart */}
                <div className="glass-panel p-5 bg-black/20 flex flex-col items-center justify-center">
                  <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">6-Axis Pressure DNA Radar</div>
                  <RadarChart datasets={[{ player: dossierPlayer }]} size={280} />
                </div>

                {/* Performance Metrics */}
                <div className="glass-panel p-5 bg-black/20 flex flex-col justify-between">
                  <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">Pressure vs Baseline Breakdown</div>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400">High-Pressure Output</span>
                        <span className="font-bold text-[#06B6D4]">{dossierPlayer.pressure_strike_rate_or_economy?.toFixed(2)}</span>
                      </div>
                      <div className="w-full bg-white/5 rounded-full h-2">
                        <div className="bg-[#06B6D4] h-2 rounded-full" style={{ width: `${Math.min(100, (dossierPlayer.pressure_strike_rate_or_economy / 220) * 100)}%` }} />
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400">Non-Pressure Baseline</span>
                        <span className="font-bold text-slate-300">{dossierPlayer.baseline_strike_rate_or_economy?.toFixed(2)}</span>
                      </div>
                      <div className="w-full bg-white/5 rounded-full h-2">
                        <div className="bg-slate-600 h-2 rounded-full" style={{ width: `${Math.min(100, (dossierPlayer.baseline_strike_rate_or_economy / 220) * 100)}%` }} />
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400">Uplift Delta</span>
                        <span className={`font-bold ${dossierPlayer.change_vs_baseline > 0 ? "text-[#10B981]" : "text-red-400"}`}>
                          {dossierPlayer.change_vs_baseline > 0 ? `+${dossierPlayer.change_vs_baseline?.toFixed(2)}` : dossierPlayer.change_vs_baseline?.toFixed(2)}
                        </span>
                      </div>
                    </div>
                    <div className="pt-2 border-t border-white/5 grid grid-cols-2 gap-2 text-center text-xs">
                      <div className="bg-white/5 p-2 rounded-lg">
                        <div className="text-[10px] text-slate-400">IPL PRESSURE BALLS</div>
                        <div className="font-bold text-white text-sm">{dossierPlayer.IPL_pressure_balls}</div>
                      </div>
                      <div className="bg-white/5 p-2 rounded-lg">
                        <div className="text-[10px] text-slate-400">T20I PRESSURE BALLS</div>
                        <div className="font-bold text-white text-sm">{dossierPlayer.T20I_pressure_balls}</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Scout Memo */}
                <div className="glass-panel p-5 bg-black/20 flex flex-col justify-between">
                  <div>
                    <div className="text-xs font-bold uppercase tracking-wider text-[#FF70B8] mb-2">Scout's Tactical Memo</div>
                    <div className="text-sm font-semibold text-white leading-relaxed mb-4">{dossierPlayer.scout_verdict}</div>
                    <div className="bg-white/5 p-3 rounded-xl border border-white/5">
                      <div className="text-[10px] text-slate-400 uppercase font-bold">Assigned Tactical Function</div>
                      <div className="font-bold text-[#FF70B8] text-sm mt-0.5">{dossierPlayer.rr_role_target}</div>
                    </div>
                  </div>
                  <div className="mt-4 pt-3 border-t border-white/5 text-[11px] text-slate-400">
                    🛡️ <b>Risk Index:</b> {dossierPlayer.risk_score}/100 · {dossierPlayer.risk_score < 30 ? "Safe elite commodity." : "Screening caution advised on sample size."}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: COMPARE STUDIO */}
        {activeTab === "compare" && (
          <div className="space-y-6">
            <div className="glass-panel p-4">
              <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Select Candidates to Compare (Max 4):</div>
              <div className="flex flex-wrap gap-2">
                {candidates.slice(0, 15).map((c) => {
                  const selected = compareList.includes(c.player_name);
                  return (
                    <button
                      key={c.player_name}
                      onClick={() => {
                        if (selected) {
                          if (compareList.length > 1) setCompareList(compareList.filter((p) => p !== c.player_name));
                        } else {
                          if (compareList.length < 4) setCompareList([...compareList, c.player_name]);
                        }
                      }}
                      className={`px-3 py-1.5 rounded-lg text-xs font-semibold cursor-pointer transition-all ${
                        selected
                          ? "bg-[#E80071] text-white border border-[#FF70B8]"
                          : "bg-white/5 text-slate-400 hover:text-white"
                      }`}
                    >
                      {c.player_name}
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Overlaid Radar */}
              <div className="glass-panel p-6 flex flex-col items-center justify-center">
                <div className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4">Multi-Candidate Radar Overlay</div>
                <RadarChart datasets={comparePlayers.map((p) => ({ player: p }))} size={320} />
                <div className="flex gap-4 mt-4">
                  {comparePlayers.map((p, idx) => {
                    const colors = ["#E80071", "#06B6D4", "#F59E0B", "#10B981"];
                    return (
                      <div key={p.player_name} className="flex items-center gap-1.5 text-xs font-semibold">
                        <span className="w-3 h-3 rounded-full" style={{ backgroundColor: colors[idx % colors.length] }} />
                        <span>{p.player_name}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Comparative Table */}
              <div className="glass-panel p-6 flex flex-col justify-between">
                <div>
                  <div className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4">Head-to-Head Comparative Duel</div>
                  <div className="space-y-3">
                    {comparePlayers.map((p) => (
                      <div key={p.player_name} className="bg-white/5 p-4 rounded-xl border border-white/5 flex items-center justify-between">
                        <div>
                          <div className="font-bold text-white text-base">{p.player_name}</div>
                          <div className="text-xs text-slate-400">{p.category} · {p.country}</div>
                        </div>
                        <div className="flex gap-6 text-right">
                          <div>
                            <div className="text-[10px] text-slate-400">OUTPUT</div>
                            <div className="font-bold text-[#06B6D4] text-sm">{p.pressure_strike_rate_or_economy.toFixed(1)}</div>
                          </div>
                          <div>
                            <div className="text-[10px] text-slate-400">DELTA</div>
                            <div className={`font-bold text-sm ${p.change_vs_baseline > 0 ? "text-[#10B981]" : "text-red-400"}`}>
                              {p.change_vs_baseline > 0 ? `+${p.change_vs_baseline.toFixed(1)}` : p.change_vs_baseline.toFixed(1)}
                            </div>
                          </div>
                          <div>
                            <div className="text-[10px] text-slate-400">PRESSURE-IQ</div>
                            <div className="font-extrabold text-[#FF70B8] text-sm">{p.model_score.toFixed(3)}</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Verdict Box */}
                <div className="mt-4 p-4 rounded-xl bg-gradient-to-r from-[#E80071]/10 to-transparent border-l-4 border-[#E80071]">
                  <div className="text-xs font-bold uppercase text-[#FF70B8]">Scout's Duel Verdict</div>
                  <div className="text-sm font-semibold text-white mt-1">
                    Primary Backing: {comparePlayers.sort((a, b) => b.model_score - a.model_score)[0]?.player_name}
                  </div>
                  <div className="text-xs text-slate-300 mt-1">
                    Offers superior overall PressureIQ index and proven high-leverage elevation.
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: AUCTION INTELLIGENCE */}
        {activeTab === "auction" && (
          <div className="space-y-6">
            <div className="flex justify-between items-center flex-wrap gap-4">
              <div>
                <h2 className="text-xl font-bold font-display text-white">Rajasthan Royals 2027 Auction Target Board</h2>
                <p className="text-xs text-slate-400">Strategic tier distribution and valuation benchmarks for auction planning.</p>
              </div>
              <button
                onClick={() => exportCSV(candidates, "RR_2027_Auction_Intelligence_Board.csv")}
                className="px-4 py-2 rounded-xl bg-[#E80071] text-white text-xs font-bold uppercase tracking-wider flex items-center gap-2 cursor-pointer shadow-lg shadow-[#E80071]/30"
              >
                <Download className="w-4 h-4" /> Export Auction Board
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {[
                { title: "Tier 1: Marquee Priority", color: "border-[#E80071] text-[#FF70B8]", desc: "Proven big-stage IPL match-winners worth aggressive bidding." },
                { title: "Tier 2: High-Value Moneyball", color: "border-[#10B981] text-[#34D399]", desc: "Undervalued domestic performers with massive delta uplifts." },
                { title: "Tier 3: High-Upside Punts", color: "border-[#F59E0B] text-[#FBBF24]", desc: "High-ceiling backups and late-overs accelerators." },
                { title: "Tier 4: Caution / Trap Risk", color: "border-red-500 text-red-400", desc: "Recognizable names showing negative pressure deltas." },
              ].map((tier, idx) => (
                <div key={idx} className={`glass-panel p-4 border-t-4 ${tier.color}`}>
                  <div className="font-bold text-sm text-white">{tier.title}</div>
                  <div className="text-xs text-slate-400 mt-1">{tier.desc}</div>
                </div>
              ))}
            </div>

            <div className="glass-panel overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-black/30 text-slate-400 border-b border-white/10 uppercase tracking-wider font-semibold">
                    <tr>
                      <th className="py-3 px-4">Player</th>
                      <th className="py-3 px-4">Role</th>
                      <th className="py-3 px-4">Strategic Tier</th>
                      <th className="py-3 px-4">RR Target Function</th>
                      <th className="py-3 px-4 text-right">PressureIQ</th>
                      <th className="py-3 px-4 text-right">Est. Price</th>
                      <th className="py-3 px-4 text-right">RR Synergy</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {candidates
                      .sort((a, b) => b.model_score - a.model_score)
                      .slice(0, 30)
                      .map((c) => (
                        <tr key={c.player_name} className="hover:bg-white/5">
                          <td className="py-3 px-4 font-bold text-white">{c.player_name}</td>
                          <td className="py-3 px-4 text-slate-300">{c.category}</td>
                          <td className="py-3 px-4 font-semibold text-[#FF70B8]">{c.auction_tier}</td>
                          <td className="py-3 px-4 text-slate-400">{c.rr_role_target}</td>
                          <td className="py-3 px-4 text-right font-black font-display text-[#FF70B8]">{c.model_score.toFixed(3)}</td>
                          <td className="py-3 px-4 text-right font-bold text-[#F59E0B]">₹{c.estimated_price_cr?.toFixed(1)} Cr</td>
                          <td className="py-3 px-4 text-right font-bold text-[#06B6D4]">{c.rr_tactical_fit}/100</td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 5: SQUAD SIMULATOR */}
        {activeTab === "simulator" && (
          <div className="space-y-6">
            <div className="flex justify-between items-center flex-wrap gap-4">
              <div>
                <h2 className="text-xl font-bold font-display text-white">RR 2027 Playing XI Combination Simulator</h2>
                <p className="text-xs text-slate-400">Enforces official IPL overseas quota limits, role balance, and purse budget.</p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => {
                    setSimBatters(["Sanju Samson", "Rinku Singh", "Shashank Singh", "Tristan Stubbs", "Riyan Parag", "Dhruv Jurel"]);
                    setSimBowlers(["Matheesha Pathirana", "Sandeep Sharma", "Trent Boult", "Rashid Khan", "Arshdeep Singh"]);
                  }}
                  className="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-xs font-bold text-white transition-colors cursor-pointer"
                >
                  Load Preset: Clutch & Death Wall XI
                </button>
              </div>
            </div>

            {/* Diagnostic Strip */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="glass-panel p-4">
                <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Lineup Size</div>
                <div className="text-2xl font-bold font-display text-white mt-1">{simSquad.length}/11</div>
                <div className="text-xs text-[#06B6D4]">{simSquad.length === 11 ? "Complete Playing XI" : "Incomplete (Target 11)"}</div>
              </div>
              <div className={`glass-panel p-4 ${overseasCount > 4 ? "border-red-500 bg-red-950/20" : ""}`}>
                <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Overseas Players</div>
                <div className={`text-2xl font-bold font-display mt-1 ${overseasCount > 4 ? "text-red-400" : "text-[#10B981]"}`}>
                  {overseasCount}/4 Max
                </div>
                <div className="text-xs text-slate-400">{overseasCount <= 4 ? "IPL Compliant" : "RULE VIOLATION"}</div>
              </div>
              <div className="glass-panel p-4">
                <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Projected Spend</div>
                <div className="text-2xl font-bold font-display text-[#F59E0B] mt-1">₹{totalPurseCost.toFixed(1)} Cr</div>
                <div className="text-xs text-slate-400">₹{(100 - totalPurseCost).toFixed(1)} Cr Remaining</div>
              </div>
              <div className="glass-panel p-4">
                <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Team Pressure Index</div>
                <div className="text-2xl font-bold font-display text-[#FF70B8] mt-1">{tpriScore}/100</div>
                <div className="text-xs text-[#10B981]">Elite Pressure Resistance</div>
              </div>
            </div>

            {/* Alerts */}
            {overseasCount > 4 && (
              <div className="bg-red-900/30 border border-red-500/50 p-4 rounded-xl flex items-center gap-3 text-red-200 text-sm">
                <AlertCircle className="w-5 h-5 flex-shrink-0 text-red-400" />
                <span><b>ROSTER VIOLATION:</b> You have selected {overseasCount} overseas players. IPL regulations strictly limit playing XIs to a maximum of 4 overseas players.</span>
              </div>
            )}

            {/* Squad List */}
            <div className="glass-panel p-6">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4">Simulated Playing XI Roster</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {simSquad.map((player) => (
                  <div key={player.player_name} className="bg-white/5 p-3 rounded-xl border border-white/5 flex items-center justify-between">
                    <div>
                      <div className="font-bold text-white text-sm flex items-center gap-2">
                        {player.player_name}
                        {player.is_overseas === "Yes" && (
                          <span className="text-[10px] px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 font-normal">OS</span>
                        )}
                      </div>
                      <div className="text-xs text-slate-400">{player.category} · {player.rr_role_target}</div>
                    </div>
                    <div className="text-right">
                      <div className="font-bold text-[#F59E0B] text-sm">₹{player.estimated_price_cr?.toFixed(1)} Cr</div>
                      <div className="text-xs font-display text-[#FF70B8]">{player.model_score.toFixed(3)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB 6: RISK MATRIX */}
        {activeTab === "risk" && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold font-display text-white">Multi-Dimensional Player Risk Register</h2>
              <p className="text-xs text-slate-400">Identifies sample size liabilities, baseline regression flags, and domestic transferability barriers.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="glass-panel p-5 border-l-4 border-red-500">
                <div className="font-bold text-sm text-red-400">1. Domestic Transferability Risk</div>
                <div className="text-xs text-slate-300 mt-2">
                  Non-IPL domestic stats carry uncertainty against 145+ kph express pace, world-class mystery spin, and high-intensity crowds.
                </div>
              </div>
              <div className="glass-panel p-5 border-l-4 border-amber-500">
                <div className="font-bold text-sm text-amber-400">2. Small Sample Volatility (n &lt; 100 balls)</div>
                <div className="text-xs text-slate-300 mt-2">
                  Extreme strike rates over few pressure balls rapidly regress to the mean. Bayesian shrinkage (n / (n+100)) is applied.
                </div>
              </div>
              <div className="glass-panel p-5 border-l-4 border-cyan-500">
                <div className="font-bold text-sm text-cyan-400">3. Negative Baseline Regressors</div>
                <div className="text-xs text-slate-300 mt-2">
                  Players whose output drops or economy inflates under pressure compared to their non-pressure performances.
                </div>
              </div>
            </div>

            <div className="glass-panel overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-black/30 text-slate-400 border-b border-white/10 uppercase tracking-wider font-semibold">
                    <tr>
                      <th className="py-3 px-4">Player</th>
                      <th className="py-3 px-4">Role</th>
                      <th className="py-3 px-4">Risk Severity</th>
                      <th className="py-3 px-4 text-right">Risk Score</th>
                      <th className="py-3 px-4 text-right">Pressure Balls</th>
                      <th className="py-3 px-4 text-right">IPL Balls</th>
                      <th className="py-3 px-4">Scout Mitigation</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {candidates
                      .sort((a, b) => b.risk_score - a.risk_score)
                      .slice(0, 15)
                      .map((c) => (
                        <tr key={c.player_name} className="hover:bg-white/5">
                          <td className="py-3 px-4 font-bold text-white">{c.player_name}</td>
                          <td className="py-3 px-4 text-slate-300">{c.category}</td>
                          <td className="py-3 px-4 font-semibold text-red-400">High Screening Flag</td>
                          <td className="py-3 px-4 text-right font-black text-red-400">{c.risk_score}/100</td>
                          <td className="py-3 px-4 text-right text-slate-300">{c.pressure_balls}</td>
                          <td className="py-3 px-4 text-right text-slate-400">{c.IPL_pressure_balls}</td>
                          <td className="py-3 px-4 text-slate-400">Verify IPL pace transferability prior to auction commitment.</td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 7: WINNING PITCH */}
        {activeTab === "methodology" && (
          <div className="glass-panel p-6 sm:p-8 space-y-6">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-[#E80071]/20 border border-[#E80071]/40 text-[#FF70B8] mb-2">
                Executive Briefing
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold font-display text-white">
                Winning Submission Dossier & Methodology
              </h2>
              <p className="text-sm text-slate-300 mt-1">Formulated to win Rajasthan Royals SupeRR Selector Round 1.</p>
            </div>

            <hr className="border-white/10" />

            <div className="space-y-4 text-sm text-slate-300 leading-relaxed">
              <h3 className="text-lg font-bold text-white font-display">1. Executive Summary for Rajasthan Royals Leadership</h3>
              <p>
                Rajasthan Royals' historical campaign data highlights two acute tactical vulnerabilities in high-pressure matches:
              </p>
              <ul className="list-disc pl-5 space-y-1 text-slate-300">
                <li><b>Death-Overs Bowling Leakage (Overs 17–20):</b> While Trent Boult provides gold-standard powerplay wickets, RR has leaked decisive runs in closing overs.</li>
                <li><b>Lower-Middle Order Finishing Reliability (#6–#7):</b> When the top order is challenged, RR requires domestic Indian batters who elevate their strike rate under high Required Run Rates (RRR &gt; 10.5).</li>
              </ul>

              <h3 className="text-lg font-bold text-white font-display pt-2">2. Mathematical Definition of Pressure & Bayesian Shrinkage</h3>
              <p>
                Our PressureIQ model isolates true clutch performance through a strict, multi-tiered framework:
              </p>
              <ul className="list-disc pl-5 space-y-1 text-slate-300">
                <li><b>High-Leverage State Criteria:</b> Batting in overs 16–20 with RRR &gt; 9.5, or early collapse states (&lt; 40/3 in powerplay). Bowling in overs 16–20 defending targets, or defending &lt; 24 runs in final 12 balls.</li>
                <li><b>Bayesian Shrinkage Regularization:</b> Applied via S_adj = (n / (n + 100)) * S_raw + (100 / (n + 100)) * mu_role, penalizing volatile small samples.</li>
                <li><b>Consistency Weighting:</b> Evaluated across appearances with at least 6 high-pressure deliveries.</li>
              </ul>

              <h3 className="text-lg font-bold text-white font-display pt-2">3. Recommended Top Backing for Rajasthan Royals:</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                <div className="bg-black/30 p-4 rounded-xl border border-white/5">
                  <div className="font-bold text-[#FF70B8] text-base">Shashank Singh (Batter · India)</div>
                  <p className="text-xs text-slate-300 mt-1">
                    Highest-ranked domestic Indian finisher with 362 IPL pressure balls, +60.15 delta, and 182.87 SR. The premier domestic Moneyball acquisition.
                  </p>
                </div>
                <div className="bg-black/30 p-4 rounded-xl border border-white/5">
                  <div className="font-bold text-[#06B6D4] text-base">Matheesha Pathirana (Bowler · Sri Lanka)</div>
                  <p className="text-xs text-slate-300 mt-1">
                    Low slinger release creates unmatched yorker execution at 150kph. Permanently seals RR's death-bowling leak.
                  </p>
                </div>
                <div className="bg-black/30 p-4 rounded-xl border border-white/5">
                  <div className="font-bold text-[#10B981] text-base">Donovan Ferreira (Batter · South Africa)</div>
                  <p className="text-xs text-slate-300 mt-1">
                    Phenomenal +80.93 SR delta over baseline, strike rate of 208.4 under pressure with 90.0% consistency. Plugs directly into RR's finishing slot at #6/7.
                  </p>
                </div>
                <div className="bg-black/30 p-4 rounded-xl border border-white/5">
                  <div className="font-bold text-[#F59E0B] text-base">Eshan Malinga (Bowler · Sri Lanka)</div>
                  <p className="text-xs text-slate-300 mt-1">
                    Exceptional value arbitrage. Negative delta on economy (better under pressure than normal) at a fraction of marquee price.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 bg-[#070B14] py-4 text-center text-xs text-slate-500">
        <div>👑 <b>Rajasthan Royals PressureIQ 2027</b> · SupeRR Selector Round 1 Submission War Room</div>
        <div className="mt-1">Deployable to Vercel · Full-Stack React / Next.js & Python FastAPI</div>
      </footer>
    </div>
  );
}
