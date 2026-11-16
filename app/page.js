"use client";

import React, { useState, useMemo } from "react";
import initialCandidates from "@/data/candidates.json";
import {
  ListFilter,
  User,
  GitCompare,
  Layers,
  Users,
  AlertCircle,
  FileText,
  Search,
  Download,
  CheckCircle2,
  SlidersHorizontal,
  ChevronRight,
  TrendingUp,
  Circle
} from "lucide-react";

// --- Clean High-Precision SVG Radar Chart ---
function RadarChart({ datasets, size = 300 }) {
  const center = size / 2;
  const radius = size / 2 - 44;
  const axes = [
    { label: "Clutch output", key: "radar_output" },
    { label: "Baseline delta", key: "radar_delta" },
    { label: "Sample size", key: "radar_sample" },
    { label: "Consistency", key: "radar_consistency" },
    { label: "IPL sample", key: "radar_ipl" },
    { label: "Squad fit", key: "radar_synergy" },
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
    { stroke: "#E80071", fill: "rgba(232, 0, 113, 0.18)" },
    { stroke: "#38BDF8", fill: "rgba(56, 189, 248, 0.18)" },
    { stroke: "#F59E0B", fill: "rgba(245, 158, 11, 0.18)" },
    { stroke: "#10B981", fill: "rgba(16, 185, 129, 0.18)" },
  ];

  return (
    <svg width={size} height={size} className="mx-auto overflow-visible select-none">
      {/* Background Rings */}
      {circles.map((frac, i) => (
        <circle
          key={i}
          cx={center}
          cy={center}
          r={radius * frac}
          fill="none"
          stroke="rgba(255, 255, 255, 0.08)"
          strokeWidth={frac === 1 ? 1 : 0.75}
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
              stroke="rgba(255, 255, 255, 0.1)"
              strokeWidth={0.75}
            />
            <text
              x={labelPos.x}
              y={labelPos.y}
              textAnchor="middle"
              dominantBaseline="middle"
              className="text-[11px] font-medium fill-slate-400"
            >
              {axis.label}
            </text>
          </g>
        );
      })}

      {/* Radar Polygons */}
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
              strokeWidth={1.75}
            />
            {axes.map((axis, i) => {
              const coord = getCoordinates(d.player[axis.key], i);
              return (
                <circle
                  key={i}
                  cx={coord.x}
                  cy={coord.y}
                  r={3}
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
  const [candidates] = useState(initialCandidates);
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
    <div className="min-h-screen flex flex-col surface-base">
      {/* Quiet Top Navigation Header */}
      <header className="border-b border-subtle bg-[#090C12]/95 sticky top-0 z-40">
        <div className="max-w-[1520px] mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="font-semibold text-sm tracking-tight text-white">
              Rajasthan Royals
            </span>
            <span className="text-slate-600">/</span>
            <span className="text-xs text-slate-400 font-medium">PressureIQ 2027</span>
            <span className="flex items-center gap-1.5 px-2 py-0.5 rounded text-[11px] font-medium bg-[#131924] text-slate-300 border border-subtle ml-2">
              <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]" />
              Auction decision support
            </span>
          </div>

          <div className="flex items-center gap-6 text-xs text-slate-400">
            <div>
              <span className="text-slate-500 mr-2">Purse cap</span>
              <span className="font-mono text-slate-200 font-medium">₹100.00 Cr</span>
            </div>
            <div className="h-4 w-px bg-white/10 hidden sm:block" />
            <div className="hidden sm:block">
              <span className="text-slate-500 mr-2">Overseas limit</span>
              <span className="font-mono text-slate-200 font-medium">4 in XI</span>
            </div>
          </div>
        </div>
      </header>

      {/* Quiet Product Context Title */}
      <div className="max-w-[1520px] mx-auto px-6 pt-6 pb-4 w-full">
        <div className="flex flex-col md:flex-row md:items-baseline justify-between gap-2 border-b border-subtle pb-5">
          <div>
            <h1 className="text-xl font-semibold text-white tracking-tight">
              Player reliability under pressure
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-2xl">
              Performance in high-leverage match states (overs 16–20 and collapse situations) compared to individual non-pressure baselines for the 2027 auction.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => exportCSV(filteredCandidates, "RR_PressureIQ_Candidates.csv")}
              className="h-8 px-3 rounded-lg surface-raised text-slate-300 hover:text-white text-xs font-medium flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <Download className="w-3.5 h-3.5 text-slate-400" /> Export CSV
            </button>
          </div>
        </div>
      </div>

      {/* Structured Stats Summary Strip */}
      <div className="max-w-[1520px] mx-auto px-6 py-2 w-full grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="surface-raised rounded-xl p-4">
          <div className="text-xs text-slate-400 font-normal">Active candidates</div>
          <div className="text-2xl font-mono text-white font-medium mt-1">{filteredCandidates.length}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">Across domestic & international pools</div>
        </div>
        <div className="surface-raised rounded-xl p-4">
          <div className="text-xs text-slate-400 font-normal">Pressure sample</div>
          <div className="text-2xl font-mono text-white font-medium mt-1">
            {filteredCandidates.reduce((acc, c) => acc + (c.pressure_balls || 0), 0).toLocaleString()}
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">Deliveries in high-leverage states</div>
        </div>
        <div className="surface-raised rounded-xl p-4">
          <div className="text-xs text-slate-400 font-normal">Mean PressureIQ score</div>
          <div className="text-2xl font-mono text-white font-medium mt-1">
            {(filteredCandidates.reduce((acc, c) => acc + (c.model_score || 0), 0) / (filteredCandidates.length || 1)).toFixed(3)}
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">Bayesian shrinkage adjusted</div>
        </div>
        <div className="surface-raised rounded-xl p-4">
          <div className="text-xs text-slate-400 font-normal">Priority targets</div>
          <div className="text-2xl font-mono text-[#E80071] font-medium mt-1">
            {candidates.filter((c) => c.auction_tier?.includes("Marquee") || c.auction_tier?.includes("Moneyball")).length}
          </div>
          <div className="text-[11px] text-slate-500 mt-0.5">Tier 1 and Tier 2 recommendations</div>
        </div>
      </div>

      {/* Quiet Navigation Tabs */}
      <div className="max-w-[1520px] mx-auto px-6 w-full pt-4">
        <div className="flex border-b border-subtle gap-1 overflow-x-auto scrollbar-none">
          {[
            { id: "leaderboard", label: "Rankings", icon: ListFilter },
            { id: "dossier", label: "Player dossier", icon: User },
            { id: "compare", label: "Player comparison", icon: GitCompare },
            { id: "auction", label: "Auction recommendations", icon: Layers },
            { id: "simulator", label: "Squad simulator", icon: Users },
            { id: "risk", label: "Risk analysis", icon: AlertCircle },
            { id: "methodology", label: "Methodology", icon: FileText },
          ].map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-2.5 text-xs font-medium border-b-2 transition-colors cursor-pointer ${
                  active
                    ? "border-[#E80071] text-white"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${active ? "text-[#E80071]" : "text-slate-500"}`} />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Tab Content */}
      <main className="max-w-[1520px] mx-auto px-6 py-6 w-full flex-1">
        {/* TAB 1: CANDIDATE RANKINGS */}
        {activeTab === "leaderboard" && (
          <div className="space-y-4">
            {/* Filter Bar */}
            <div className="surface-raised rounded-xl p-3 flex flex-wrap items-center gap-3">
              <div className="flex-1 min-w-[200px] relative">
                <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-500" />
                <input
                  type="text"
                  placeholder="Search player name"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-8 pr-3 py-1.5 bg-[#090C12] border border-subtle rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-slate-500"
                />
              </div>
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] text-slate-500 mr-1">Role:</span>
                {["All", "Batter", "Bowler"].map((r) => (
                  <button
                    key={r}
                    onClick={() => setRoleFilter(r)}
                    className={`px-2.5 py-1 rounded-md text-xs font-medium cursor-pointer transition-colors ${
                      roleFilter === r
                        ? "bg-[#1E2638] text-white"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    {r}
                  </button>
                ))}
              </div>
              <div className="h-4 w-px bg-white/10 hidden sm:block" />
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] text-slate-500 mr-1">Origin:</span>
                {["All", "Domestic", "Overseas"].map((o) => (
                  <button
                    key={o}
                    onClick={() => setOriginFilter(o)}
                    className={`px-2.5 py-1 rounded-md text-xs font-medium cursor-pointer transition-colors ${
                      originFilter === o
                        ? "bg-[#1E2638] text-white"
                        : "text-slate-400 hover:text-white"
                    }`}
                  >
                    {o}
                  </button>
                ))}
              </div>
            </div>

            {/* Candidate Table */}
            <div className="surface-raised rounded-xl overflow-hidden border border-subtle">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#090C12] text-slate-400 border-b border-subtle font-medium">
                    <tr>
                      <th className="py-2.5 px-4 w-14">Rank</th>
                      <th className="py-2.5 px-4">Player</th>
                      <th className="py-2.5 px-4">Role</th>
                      <th className="py-2.5 px-4">Origin</th>
                      <th className="py-2.5 px-4 text-right">Pressure output</th>
                      <th className="py-2.5 px-4 text-right">Baseline delta</th>
                      <th className="py-2.5 px-4 text-right">Consistency</th>
                      <th className="py-2.5 px-4 text-right">Balls</th>
                      <th className="py-2.5 px-4 text-right">Score</th>
                      <th className="py-2.5 px-4 text-right">Est. price</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-subtle">
                    {filteredCandidates.map((c) => (
                      <tr
                        key={c.player_name}
                        onClick={() => {
                          setSelectedPlayerName(c.player_name);
                          setActiveTab("dossier");
                        }}
                        className="hover:bg-[#131A28] cursor-pointer transition-colors"
                      >
                        <td className="py-2.5 px-4 font-mono text-slate-500">#{c.rank}</td>
                        <td className="py-2.5 px-4 font-medium text-white">
                          {c.player_name}
                          {c.is_overseas === "Yes" && (
                            <span className="text-[10px] ml-1.5 px-1 rounded bg-[#172033] text-slate-400 font-mono">
                              OS
                            </span>
                          )}
                        </td>
                        <td className="py-2.5 px-4 text-slate-400">{c.category}</td>
                        <td className="py-2.5 px-4 text-slate-400">{c.country}</td>
                        <td className="py-2.5 px-4 text-right font-mono font-medium text-slate-200">
                          {c.pressure_strike_rate_or_economy.toFixed(1)}
                        </td>
                        <td
                          className={`py-2.5 px-4 text-right font-mono font-medium ${
                            c.change_vs_baseline > 0 ? "text-[#10B981]" : "text-rose-400"
                          }`}
                        >
                          {c.change_vs_baseline > 0
                            ? `+${c.change_vs_baseline.toFixed(1)}`
                            : c.change_vs_baseline.toFixed(1)}
                        </td>
                        <td className="py-2.5 px-4 text-right font-mono text-slate-300">
                          {c.consistency_pct.toFixed(0)}%
                        </td>
                        <td className="py-2.5 px-4 text-right font-mono text-slate-400">{c.pressure_balls}</td>
                        <td className="py-2.5 px-4 text-right font-mono font-medium text-[#E80071]">
                          {c.model_score.toFixed(3)}
                        </td>
                        <td className="py-2.5 px-4 text-right font-mono text-slate-300">
                          ₹{c.estimated_price_cr?.toFixed(1)} Cr
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: PLAYER DOSSIER */}
        {activeTab === "dossier" && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 surface-raised rounded-xl p-3">
              <span className="text-xs text-slate-400 font-medium">Player profile:</span>
              <select
                value={selectedPlayerName}
                onChange={(e) => setSelectedPlayerName(e.target.value)}
                className="bg-[#090C12] border border-subtle rounded-lg px-3 py-1.5 text-xs text-white focus:outline-none focus:border-slate-500"
              >
                {candidates.map((c) => (
                  <option key={c.player_name} value={c.player_name}>
                    {c.player_name} ({c.category} · {c.country})
                  </option>
                ))}
              </select>
            </div>

            {/* Dossier Card */}
            <div className="surface-raised rounded-xl p-6 border border-subtle">
              <div className="flex flex-col md:flex-row md:items-baseline justify-between gap-4 border-b border-subtle pb-5">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-[#141C2B] text-slate-300 border border-subtle">
                      {dossierPlayer.auction_tier}
                    </span>
                    <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-[#141C2B] text-slate-400 border border-subtle">
                      {dossierPlayer.is_overseas === "Yes" ? "Overseas" : "Domestic"}
                    </span>
                    <span className="px-2 py-0.5 rounded text-[11px] font-medium bg-[#141C2B] text-slate-400 border border-subtle">
                      {dossierPlayer.phase_specialization}
                    </span>
                  </div>
                  <h2 className="text-2xl font-semibold text-white tracking-tight">{dossierPlayer.player_name}</h2>
                  <p className="text-xs text-slate-400 mt-1">
                    {dossierPlayer.country} · {dossierPlayer.category} · {dossierPlayer.skill_specialization} · {dossierPlayer.batting_style} / {dossierPlayer.bowling_style}
                  </p>
                </div>
                <div className="flex items-center gap-6">
                  <div>
                    <div className="text-[11px] text-slate-500 font-normal">Valuation</div>
                    <div className="font-mono text-lg font-medium text-white">₹{dossierPlayer.estimated_price_cr?.toFixed(1)} Cr</div>
                  </div>
                  <div className="border-l border-subtle pl-6">
                    <div className="text-[11px] text-slate-500 font-normal">RR tactical fit</div>
                    <div className="font-mono text-lg font-medium text-[#E80071]">{dossierPlayer.rr_tactical_fit}/100</div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6">
                {/* Radar Chart */}
                <div className="surface-base rounded-xl p-4 flex flex-col items-center justify-center border border-subtle">
                  <div className="text-xs font-medium text-slate-400 mb-2">Pressure DNA profile</div>
                  <RadarChart datasets={[{ player: dossierPlayer }]} size={270} />
                </div>

                {/* Performance Metrics */}
                <div className="surface-base rounded-xl p-5 flex flex-col justify-between border border-subtle">
                  <div className="text-xs font-medium text-slate-400 mb-3">Pressure vs baseline comparison</div>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400">High-pressure output</span>
                        <span className="font-mono text-white font-medium">{dossierPlayer.pressure_strike_rate_or_economy?.toFixed(2)}</span>
                      </div>
                      <div className="w-full bg-[#1A2234] rounded-full h-1.5">
                        <div className="bg-[#E80071] h-1.5 rounded-full" style={{ width: `${Math.min(100, (dossierPlayer.pressure_strike_rate_or_economy / 220) * 100)}%` }} />
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400">Non-pressure baseline</span>
                        <span className="font-mono text-slate-400">{dossierPlayer.baseline_strike_rate_or_economy?.toFixed(2)}</span>
                      </div>
                      <div className="w-full bg-[#1A2234] rounded-full h-1.5">
                        <div className="bg-slate-500 h-1.5 rounded-full" style={{ width: `${Math.min(100, (dossierPlayer.baseline_strike_rate_or_economy / 220) * 100)}%` }} />
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400">Baseline uplift delta</span>
                        <span className={`font-mono font-medium ${dossierPlayer.change_vs_baseline > 0 ? "text-[#10B981]" : "text-rose-400"}`}>
                          {dossierPlayer.change_vs_baseline > 0 ? `+${dossierPlayer.change_vs_baseline?.toFixed(2)}` : dossierPlayer.change_vs_baseline?.toFixed(2)}
                        </span>
                      </div>
                    </div>
                    <div className="pt-3 border-t border-subtle grid grid-cols-2 gap-2 text-center text-xs">
                      <div className="bg-[#0F141F] p-2 rounded-lg border border-subtle">
                        <div className="text-[10px] text-slate-500">IPL PRESSURE BALLS</div>
                        <div className="font-mono text-white text-sm mt-0.5">{dossierPlayer.IPL_pressure_balls}</div>
                      </div>
                      <div className="bg-[#0F141F] p-2 rounded-lg border border-subtle">
                        <div className="text-[10px] text-slate-500">T20I PRESSURE BALLS</div>
                        <div className="font-mono text-white text-sm mt-0.5">{dossierPlayer.T20I_pressure_balls}</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Scout Memo */}
                <div className="surface-base rounded-xl p-5 flex flex-col justify-between border border-subtle">
                  <div>
                    <div className="text-xs font-medium text-slate-400 mb-2">Scouting memo</div>
                    <p className="text-xs text-slate-200 leading-relaxed mb-4">{dossierPlayer.scout_verdict}</p>
                    <div className="bg-[#0F141F] p-3 rounded-lg border border-subtle">
                      <div className="text-[10px] text-slate-500 uppercase font-medium">Assigned tactical function</div>
                      <div className="text-xs font-medium text-[#E80071] mt-0.5">{dossierPlayer.rr_role_target}</div>
                    </div>
                  </div>
                  <div className="mt-4 pt-3 border-t border-subtle text-[11px] text-slate-500">
                    Risk screening score: <span className="font-mono text-slate-300">{dossierPlayer.risk_score}/100</span> · {dossierPlayer.risk_score < 30 ? "Standard verification" : "Check domestic-to-IPL pace transferability"}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: COMPARE STUDIO */}
        {activeTab === "compare" && (
          <div className="space-y-4">
            <div className="surface-raised rounded-xl p-4">
              <div className="text-xs font-medium text-slate-400 mb-2.5">Select candidates to compare (up to 4):</div>
              <div className="flex flex-wrap gap-2">
                {candidates.slice(0, 16).map((c) => {
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
                      className={`px-3 py-1 rounded-md text-xs font-medium cursor-pointer transition-colors ${
                        selected
                          ? "bg-[#E80071] text-white"
                          : "surface-base text-slate-400 hover:text-white border border-subtle"
                      }`}
                    >
                      {c.player_name}
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {/* Overlaid Radar */}
              <div className="surface-raised rounded-xl p-5 flex flex-col items-center justify-center border border-subtle">
                <div className="text-xs font-medium text-slate-400 mb-3">Normalized multi-candidate radar</div>
                <RadarChart datasets={comparePlayers.map((p) => ({ player: p }))} size={300} />
                <div className="flex gap-4 mt-4">
                  {comparePlayers.map((p, idx) => {
                    const colors = ["#E80071", "#38BDF8", "#F59E0B", "#10B981"];
                    return (
                      <div key={p.player_name} className="flex items-center gap-1.5 text-xs text-slate-300">
                        <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: colors[idx % colors.length] }} />
                        <span>{p.player_name}</span>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Comparative Table */}
              <div className="surface-raised rounded-xl p-5 flex flex-col justify-between border border-subtle">
                <div>
                  <div className="text-xs font-medium text-slate-400 mb-3">Head-to-head metrics</div>
                  <div className="space-y-2">
                    {comparePlayers.map((p) => (
                      <div key={p.player_name} className="surface-base p-3 rounded-lg border border-subtle flex items-center justify-between">
                        <div>
                          <div className="font-medium text-white text-xs">{p.player_name}</div>
                          <div className="text-[11px] text-slate-500">{p.category} · {p.country}</div>
                        </div>
                        <div className="flex gap-5 text-right font-mono text-xs">
                          <div>
                            <div className="text-[10px] text-slate-500">OUTPUT</div>
                            <div className="text-slate-200">{p.pressure_strike_rate_or_economy.toFixed(1)}</div>
                          </div>
                          <div>
                            <div className="text-[10px] text-slate-500">DELTA</div>
                            <div className={p.change_vs_baseline > 0 ? "text-[#10B981]" : "text-rose-400"}>
                              {p.change_vs_baseline > 0 ? `+${p.change_vs_baseline.toFixed(1)}` : p.change_vs_baseline.toFixed(1)}
                            </div>
                          </div>
                          <div>
                            <div className="text-[10px] text-slate-500">SCORE</div>
                            <div className="text-[#E80071] font-medium">{p.model_score.toFixed(3)}</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mt-4 p-3 rounded-lg bg-[#0F141F] border border-subtle">
                  <div className="text-[11px] font-medium text-slate-400">Scout decision recommendation</div>
                  <div className="text-xs font-medium text-white mt-1">
                    Primary target: {comparePlayers.sort((a, b) => b.model_score - a.model_score)[0]?.player_name}
                  </div>
                  <div className="text-[11px] text-slate-400 mt-0.5">
                    Demonstrates higher sample reliability and superior output delta versus personal baseline.
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: AUCTION INTELLIGENCE */}
        {activeTab === "auction" && (
          <div className="space-y-4">
            <div className="surface-raised rounded-xl p-4 border border-subtle flex justify-between items-center">
              <div>
                <h2 className="text-sm font-semibold text-white">Auction tier recommendations</h2>
                <p className="text-xs text-slate-400 mt-0.5">Target categorization based on performance under pressure and sample credibility.</p>
              </div>
              <button
                onClick={() => exportCSV(candidates, "RR_Auction_Board.csv")}
                className="h-8 px-3 rounded-lg surface-base border border-subtle text-slate-300 hover:text-white text-xs font-medium flex items-center gap-1.5 transition-colors cursor-pointer"
              >
                <Download className="w-3.5 h-3.5 text-slate-400" /> Export board
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
              {[
                { title: "Tier 1: Marquee priority", count: candidates.filter((c) => c.auction_tier?.includes("Marquee")).length, desc: "High sample depth with verified IPL clutch impact." },
                { title: "Tier 2: Moneyball value", count: candidates.filter((c) => c.auction_tier?.includes("Moneyball")).length, desc: "High baseline delta elevation with efficient valuation." },
                { title: "Tier 3: High-upside punts", count: candidates.filter((c) => c.auction_tier?.includes("Punt")).length, desc: "High-ceiling backups and late-innings accelerators." },
                { title: "Tier 4: Caution / review", count: candidates.filter((c) => c.auction_tier?.includes("Trap")).length, desc: "Candidates showing negative delta under pressure." },
              ].map((tier, idx) => (
                <div key={idx} className="surface-raised rounded-xl p-3.5 border border-subtle">
                  <div className="text-xs font-medium text-white">{tier.title}</div>
                  <div className="font-mono text-xl font-medium text-slate-200 mt-1">{tier.count}</div>
                  <div className="text-[11px] text-slate-500 mt-1">{tier.desc}</div>
                </div>
              ))}
            </div>

            <div className="surface-raised rounded-xl overflow-hidden border border-subtle">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#090C12] text-slate-400 border-b border-subtle font-medium">
                    <tr>
                      <th className="py-2.5 px-4">Player</th>
                      <th className="py-2.5 px-4">Role</th>
                      <th className="py-2.5 px-4">Tier</th>
                      <th className="py-2.5 px-4">Assigned function</th>
                      <th className="py-2.5 px-4 text-right">PressureIQ</th>
                      <th className="py-2.5 px-4 text-right">Est. price</th>
                      <th className="py-2.5 px-4 text-right">Synergy</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-subtle">
                    {candidates
                      .sort((a, b) => b.model_score - a.model_score)
                      .slice(0, 25)
                      .map((c) => (
                        <tr key={c.player_name} className="hover:bg-[#131A28]">
                          <td className="py-2.5 px-4 font-medium text-white">{c.player_name}</td>
                          <td className="py-2.5 px-4 text-slate-400">{c.category}</td>
                          <td className="py-2.5 px-4 text-slate-300">{c.auction_tier}</td>
                          <td className="py-2.5 px-4 text-slate-400">{c.rr_role_target}</td>
                          <td className="py-2.5 px-4 text-right font-mono font-medium text-[#E80071]">{c.model_score.toFixed(3)}</td>
                          <td className="py-2.5 px-4 text-right font-mono text-slate-200">₹{c.estimated_price_cr?.toFixed(1)} Cr</td>
                          <td className="py-2.5 px-4 text-right font-mono text-slate-400">{c.rr_tactical_fit}/100</td>
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
          <div className="space-y-4">
            <div className="surface-raised rounded-xl p-4 border border-subtle flex justify-between items-center">
              <div>
                <h2 className="text-sm font-semibold text-white">Playing XI combination simulator</h2>
                <p className="text-xs text-slate-400 mt-0.5">Validate roster compliance against IPL rules (4 overseas maximum) and purse limits.</p>
              </div>
              <button
                onClick={() => {
                  setSimBatters(["Sanju Samson", "Rinku Singh", "Shashank Singh", "Tristan Stubbs", "Riyan Parag", "Dhruv Jurel"]);
                  setSimBowlers(["Matheesha Pathirana", "Sandeep Sharma", "Trent Boult", "Rashid Khan", "Arshdeep Singh"]);
                }}
                className="h-8 px-3 rounded-lg surface-base border border-subtle text-slate-300 hover:text-white text-xs font-medium cursor-pointer transition-colors"
              >
                Load preset: Balanced clutch XI
              </button>
            </div>

            {/* Diagnostic Strip */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="surface-raised rounded-xl p-3.5 border border-subtle">
                <div className="text-xs text-slate-400">Lineup count</div>
                <div className="font-mono text-xl font-medium text-white mt-1">{simSquad.length} / 11</div>
                <div className="text-[11px] text-slate-500 mt-0.5">{simSquad.length === 11 ? "Complete XI" : "Needs 11 players"}</div>
              </div>
              <div className={`surface-raised rounded-xl p-3.5 border border-subtle ${overseasCount > 4 ? "border-rose-500/50" : ""}`}>
                <div className="text-xs text-slate-400">Overseas players</div>
                <div className={`font-mono text-xl font-medium mt-1 ${overseasCount > 4 ? "text-rose-400" : "text-white"}`}>
                  {overseasCount} / 4
                </div>
                <div className="text-[11px] text-slate-500 mt-0.5">{overseasCount <= 4 ? "Compliant" : "Exceeds overseas limit"}</div>
              </div>
              <div className="surface-raised rounded-xl p-3.5 border border-subtle">
                <div className="text-xs text-slate-400">Projected XI spend</div>
                <div className="font-mono text-xl font-medium text-white mt-1">₹{totalPurseCost.toFixed(1)} Cr</div>
                <div className="text-[11px] text-slate-500 mt-0.5">₹{(100 - totalPurseCost).toFixed(1)} Cr remaining purse</div>
              </div>
              <div className="surface-raised rounded-xl p-3.5 border border-subtle">
                <div className="text-xs text-slate-400">Team pressure index</div>
                <div className="font-mono text-xl font-medium text-[#E80071] mt-1">{tpriScore}/100</div>
                <div className="text-[11px] text-slate-500 mt-0.5">Mean lineup pressure rating</div>
              </div>
            </div>

            {/* Squad List */}
            <div className="surface-raised rounded-xl p-4 border border-subtle">
              <div className="text-xs font-medium text-slate-400 mb-3">Simulated lineup positions</div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {simSquad.map((player) => (
                  <div key={player.player_name} className="surface-base p-2.5 rounded-lg border border-subtle flex items-center justify-between">
                    <div>
                      <div className="font-medium text-white text-xs flex items-center gap-1.5">
                        {player.player_name}
                        {player.is_overseas === "Yes" && (
                          <span className="text-[10px] px-1 rounded bg-[#172033] text-slate-400 font-mono">OS</span>
                        )}
                      </div>
                      <div className="text-[11px] text-slate-500">{player.category} · {player.rr_role_target}</div>
                    </div>
                    <div className="text-right font-mono text-xs">
                      <div className="text-slate-300">₹{player.estimated_price_cr?.toFixed(1)} Cr</div>
                      <div className="text-slate-500 text-[11px]">{player.model_score.toFixed(3)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* TAB 6: RISK ANALYSIS */}
        {activeTab === "risk" && (
          <div className="space-y-4">
            <div className="surface-raised rounded-xl p-4 border border-subtle">
              <h2 className="text-sm font-semibold text-white">Candidate risk register</h2>
              <p className="text-xs text-slate-400 mt-0.5">Screens sample-size sensitivity, domestic transferability barriers, and baseline regressors.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="surface-raised rounded-xl p-3.5 border border-subtle">
                <div className="text-xs font-medium text-slate-300">1. Domestic transferability</div>
                <div className="text-[11px] text-slate-400 mt-1">
                  Performances outside the IPL require adjustment for pace volume (145+ kph) and bowler quality.
                </div>
              </div>
              <div className="surface-raised rounded-xl p-3.5 border border-subtle">
                <div className="text-xs font-medium text-slate-300">2. Small sample sensitivity</div>
                <div className="text-[11px] text-slate-400 mt-1">
                  Deliveries under 100 pressure balls receive Bayesian shrinkage regularization to prevent sample distortion.
                </div>
              </div>
              <div className="surface-raised rounded-xl p-3.5 border border-subtle">
                <div className="text-xs font-medium text-slate-300">3. Baseline regression</div>
                <div className="text-[11px] text-slate-400 mt-1">
                  Flags candidates whose output drops or economy inflates during high-leverage match states.
                </div>
              </div>
            </div>

            <div className="surface-raised rounded-xl overflow-hidden border border-subtle">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#090C12] text-slate-400 border-b border-subtle font-medium">
                    <tr>
                      <th className="py-2.5 px-4">Player</th>
                      <th className="py-2.5 px-4">Role</th>
                      <th className="py-2.5 px-4 text-right">Risk score</th>
                      <th className="py-2.5 px-4 text-right">Pressure balls</th>
                      <th className="py-2.5 px-4 text-right">IPL balls</th>
                      <th className="py-2.5 px-4">Screening observation</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-subtle">
                    {candidates
                      .sort((a, b) => b.risk_score - a.risk_score)
                      .slice(0, 15)
                      .map((c) => (
                        <tr key={c.player_name} className="hover:bg-[#131A28]">
                          <td className="py-2.5 px-4 font-medium text-white">{c.player_name}</td>
                          <td className="py-2.5 px-4 text-slate-400">{c.category}</td>
                          <td className="py-2.5 px-4 text-right font-mono font-medium text-slate-300">{c.risk_score}/100</td>
                          <td className="py-2.5 px-4 text-right font-mono text-slate-400">{c.pressure_balls}</td>
                          <td className="py-2.5 px-4 text-right font-mono text-slate-400">{c.IPL_pressure_balls}</td>
                          <td className="py-2.5 px-4 text-slate-400">Review against high-speed bowling prior to auction commitment</td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 7: METHODOLOGY */}
        {activeTab === "methodology" && (
          <div className="surface-raised rounded-xl p-6 border border-subtle space-y-5 text-xs text-slate-300 leading-relaxed">
            <div>
              <h2 className="text-base font-semibold text-white">Analytical methodology & model definition</h2>
              <p className="text-slate-400 mt-0.5">Formulated for the Rajasthan Royals SupeRR Selector challenge.</p>
            </div>

            <div className="border-t border-subtle pt-4 space-y-3">
              <h3 className="text-xs font-semibold text-white uppercase tracking-wider">1. Tactical alignment with Rajasthan Royals requirements</h3>
              <p>
                Franchise data reveals two core tactical requirements for the 2027 auction cycle:
              </p>
              <ul className="list-disc pl-4 space-y-1 text-slate-400">
                <li><b>Death-overs bowling control (overs 16–20):</b> Sealing late-innings boundary leakage to protect totals.</li>
                <li><b>Lower-middle order finishing reliability (#6–#7):</b> Domestic Indian batters capable of accelerating under required run rates exceeding 10.5.</li>
              </ul>
            </div>

            <div className="border-t border-subtle pt-4 space-y-3">
              <h3 className="text-xs font-semibold text-white uppercase tracking-wider">2. Definition of pressure states</h3>
              <p className="text-slate-400">
                A delivery is classified as high-pressure when meeting any of the following game conditions:
              </p>
              <ul className="list-disc pl-4 space-y-1 text-slate-400">
                <li><b>Batting pressure:</b> Overs 16–20 during chases with RRR &gt; 9.5, or early collapse states (&lt; 40/3 in powerplay).</li>
                <li><b>Bowling pressure:</b> Overs 16–20 defending totals, or defending &lt; 24 runs in the final 12 deliveries.</li>
                <li><b>Bayesian shrinkage:</b> Scores are adjusted using S_adj = (n / (n + 100)) * S_raw + (100 / (n + 100)) * mu to penalize small samples.</li>
              </ul>
            </div>

            <div className="border-t border-subtle pt-4 space-y-3">
              <h3 className="text-xs font-semibold text-white uppercase tracking-wider">3. Primary player recommendations</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2">
                <div className="surface-base p-3.5 rounded-lg border border-subtle">
                  <div className="font-medium text-white">Shashank Singh (Batter · India)</div>
                  <div className="text-[11px] text-slate-400 mt-1">
                    362 IPL pressure balls with +60.15 delta over baseline and 182.87 strike rate. Addresses lower-order finishing at accessible valuation.
                  </div>
                </div>
                <div className="surface-base p-3.5 rounded-lg border border-subtle">
                  <div className="font-medium text-white">Matheesha Pathirana (Bowler · Sri Lanka)</div>
                  <div className="text-[11px] text-slate-400 mt-1">
                    Low round-arm release delivering 150kph yorkers. Addresses death-overs boundary prevention.
                  </div>
                </div>
                <div className="surface-base p-3.5 rounded-lg border border-subtle">
                  <div className="font-medium text-white">Donovan Ferreira (Batter · South Africa)</div>
                  <div className="text-[11px] text-slate-400 mt-1">
                    +80.93 strike rate delta with 90% consistency across pressure appearances. High-velocity finisher option.
                  </div>
                </div>
                <div className="surface-base p-3.5 rounded-lg border border-subtle">
                  <div className="font-medium text-white">Eshan Malinga (Bowler · Sri Lanka)</div>
                  <div className="text-[11px] text-slate-400 mt-1">
                    Value pick with negative pressure economy delta (improved execution under pressure).
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Quiet Footer */}
      <footer className="border-t border-subtle py-4 text-center text-xs text-slate-500">
        Rajasthan Royals PressureIQ 2027 · Decision-support tool for IPL auction planning
      </footer>
    </div>
  );
}
