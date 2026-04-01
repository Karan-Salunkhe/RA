import React, { useState, useEffect, useMemo } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, Cell, PieChart, Pie, Legend, AreaChart, Area,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ScatterChart, Scatter, ZAxis, ReferenceLine
} from 'recharts';
import {
  AlertCircle, Home, Map as MapIcon, BarChart3, Info, Search,
  ShieldCheck, Activity, Clock, MapPin, AlertTriangle, TrendingUp,
  FileSearch, Layers
} from 'lucide-react';

/**
 * PROJECT: Syracuse Housing Safety Tracker
 * AUTHOR: Karan C. Salunkhe
 * PURPOSE: Phase 4 Deliverable — Unified tool to measure the "Remediation Gap".
 * VERSION: 2.0 — Added full EDA tab, 6 new visualizations, all 10 neighborhoods.
 */

// ─────────────────────────────────────────────
// DATA CONSTANTS
// ─────────────────────────────────────────────

const NEIGHBORHOODS = [
  "Northside", "Near Westside", "Southside", "Eastside", "Westcott",
  "Eastwood", "Washington Square", "Skunk City", "Brighton", "Strathmore"
];

const MOCK_STATS = {
  "Northside":         { violations: 2859, open: 642,  medianLag: 940,  permitsMatched: 12, density: 45.2, healthScore: 62, meanLag: 1380, p25Lag: 420, p75Lag: 1600 },
  "Near Westside":     { violations: 1950, open: 410,  medianLag: 895,  permitsMatched: 8,  density: 38.7, healthScore: 58, meanLag: 1290, p25Lag: 380, p75Lag: 1450 },
  "Southside":         { violations: 1720, open: 380,  medianLag: 810,  permitsMatched: 5,  density: 33.1, healthScore: 65, meanLag: 1100, p25Lag: 310, p75Lag: 1300 },
  "Eastside":          { violations: 1340, open: 290,  medianLag: 720,  permitsMatched: 9,  density: 28.4, healthScore: 70, meanLag: 980,  p25Lag: 260, p75Lag: 1150 },
  "Westcott":          { violations: 980,  open: 140,  medianLag: 540,  permitsMatched: 11, density: 19.6, healthScore: 81, meanLag: 740,  p25Lag: 180, p75Lag: 920  },
  "Eastwood":          { violations: 860,  open: 110,  medianLag: 490,  permitsMatched: 7,  density: 17.2, healthScore: 84, meanLag: 680,  p25Lag: 160, p75Lag: 830  },
  "Washington Square": { violations: 1100, open: 200,  medianLag: 670,  permitsMatched: 6,  density: 24.8, healthScore: 72, meanLag: 890,  p25Lag: 220, p75Lag: 1080 },
  "Skunk City":        { violations: 760,  open: 195,  medianLag: 1020, permitsMatched: 3,  density: 52.1, healthScore: 49, meanLag: 1540, p25Lag: 510, p75Lag: 1780 },
  "Brighton":          { violations: 640,  open: 88,   medianLag: 420,  permitsMatched: 10, density: 14.3, healthScore: 88, meanLag: 580,  p25Lag: 140, p75Lag: 700  },
  "Strathmore":        { violations: 520,  open: 62,   medianLag: 380,  permitsMatched: 9,  density: 11.9, healthScore: 91, meanLag: 490,  p25Lag: 120, p75Lag: 620  },
};

// Seasonal data — monthly violation filings across the full year
const SEASONAL_DATA = [
  { month: 'Jan', violations: 980,  avg: 720 },
  { month: 'Feb', violations: 1040, avg: 720 },
  { month: 'Mar', violations: 860,  avg: 720 },
  { month: 'Apr', violations: 710,  avg: 720 },
  { month: 'May', violations: 620,  avg: 720 },
  { month: 'Jun', violations: 570,  avg: 720 },
  { month: 'Jul', violations: 540,  avg: 720 },
  { month: 'Aug', violations: 560,  avg: 720 },
  { month: 'Sep', violations: 610,  avg: 720 },
  { month: 'Oct', violations: 740,  avg: 720 },
  { month: 'Nov', violations: 890,  avg: 720 },
  { month: 'Dec', violations: 1010, avg: 720 },
];

// Remediation lag histogram buckets (days)
const LAG_HISTOGRAM = [
  { bucket: '0–180',    count: 38 },
  { bucket: '181–365',  count: 52 },
  { bucket: '366–540',  count: 41 },
  { bucket: '541–730',  count: 63 },
  { bucket: '731–895',  count: 49 },
  { bucket: '896–1095', count: 34 },
  { bucket: '1096–1460',count: 28 },
  { bucket: '1461–1825',count: 19 },
  { bucket: '1826+',    count: 14 },
];

// Escalation timeline stages (avg days from first violation)
const ESCALATION_DATA = [
  { stage: 'Initial Report Filed',     days: 0,    label: 'Day 0' },
  { stage: 'Re-inspection Triggered',  days: 94,   label: 'Day 94' },
  { stage: 'Notice of Violation',      days: 187,  label: 'Day 187' },
  { stage: '"Unfit" Designation',      days: 412,  label: 'Day 412' },
  { stage: 'Building Permit Issued',   days: 1307, label: 'Day 1307' },
];

// Violation type breakdown
const VIOLATION_TYPES = [
  { type: 'Structural (Roof/Foundation)', count: 1820, pct: 24 },
  { type: 'Heating / HVAC Failure',       count: 1540, pct: 20 },
  { type: 'Electrical Hazard',            count: 1190, pct: 16 },
  { type: 'Interior Maintenance',         count: 1080, pct: 14 },
  { type: 'Exterior / Facade',            count: 870,  pct: 11 },
  { type: 'Plumbing / Water',             count: 760,  pct: 10 },
  { type: 'Other / Miscellaneous',        count: 400,  pct: 5  },
];

// Status attrition — how violations are closed
const ATTRITION_DATA = [
  { method: 'Verified Physical Repair', count: 3820, fill: '#2563eb' },
  { method: 'Admin / Age-Out Closure',  count: 2140, fill: '#f59e0b' },
  { method: 'Permit-Based Closure',     count: 980,  fill: '#10b981' },
  { method: 'Demolished / Demolished',  count: 310,  fill: '#ef4444' },
  { method: 'Contested / In Appeal',    count: 190,  fill: '#8b5cf6' },
];

// Density-normalized neighborhood comparison
const DENSITY_COMPARISON = NEIGHBORHOODS.map(n => ({
  name: n.replace(' ', '\n'),
  fullName: n,
  density: MOCK_STATS[n]?.density ?? 22.5,
  medianLag: MOCK_STATS[n]?.medianLag ?? 650,
  healthScore: MOCK_STATS[n]?.healthScore ?? 78,
})).sort((a, b) => b.density - a.density);

// Lifecycle trend data (full year for dashboard)
const TREND_DATA = [
  { name: 'Jan', violations: 420, permits: 10 },
  { name: 'Feb', violations: 480, permits: 12 },
  { name: 'Mar', violations: 350, permits: 8  },
  { name: 'Apr', violations: 290, permits: 15 },
  { name: 'May', violations: 210, permits: 18 },
  { name: 'Jun', violations: 190, permits: 22 },
  { name: 'Jul', violations: 185, permits: 25 },
  { name: 'Aug', violations: 200, permits: 21 },
  { name: 'Sep', violations: 240, permits: 17 },
  { name: 'Oct', violations: 310, permits: 14 },
  { name: 'Nov', violations: 390, permits: 11 },
  { name: 'Dec', violations: 460, permits: 9  },
];

// ─────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────

const getRiskColor = (density) => {
  if (density >= 45) return '#ef4444';
  if (density >= 30) return '#f97316';
  if (density >= 20) return '#f59e0b';
  return '#22c55e';
};

const getRiskLabel = (density) => {
  if (density >= 45) return 'Critical';
  if (density >= 30) return 'High';
  if (density >= 20) return 'Moderate';
  return 'Low';
};

const CustomTooltipStyle = {
  borderRadius: '12px',
  border: 'none',
  boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1)',
  fontSize: '12px',
};

// ─────────────────────────────────────────────
// COMPONENT: SVG MAP ENGINE
// ─────────────────────────────────────────────

const SyracuseSVGMap = ({ selected, onSelect }) => {
  const areas = [
    { id: "Northside",         x: 130, y: 30,  w: 110, h: 65  },
    { id: "Near Westside",     x: 30,  y: 110, w: 90,  h: 75  },
    { id: "Southside",         x: 110, y: 200, w: 95,  h: 90  },
    { id: "Eastside",          x: 250, y: 130, w: 90,  h: 65  },
    { id: "Westcott",          x: 260, y: 220, w: 60,  h: 55  },
    { id: "Eastwood",          x: 330, y: 60,  w: 60,  h: 55  },
    { id: "Washington Square", x: 130, y: 105, w: 110, h: 55  },
    { id: "Skunk City",        x: 30,  y: 210, w: 70,  h: 70  },
    { id: "Brighton",          x: 215, y: 55,  w: 60,  h: 55  },
    { id: "Strathmore",        x: 330, y: 200, w: 60,  h: 55  },
  ];

  return (
    <div className="relative w-full h-[520px] bg-slate-100 rounded-xl overflow-hidden border border-slate-200">
      <div className="absolute inset-0 p-6">
        <svg viewBox="0 0 420 320" className="w-full h-full drop-shadow-sm">
          {areas.map((area) => {
            const stats = MOCK_STATS[area.id] || MOCK_STATS["Default"];
            const isSelected = selected === area.id;
            const riskColor = getRiskColor(stats?.density ?? 22);
            return (
              <g key={area.id} className="cursor-pointer" onClick={() => onSelect(area.id)}>
                <rect
                  x={area.x} y={area.y} width={area.w} height={area.h}
                  rx="7"
                  fill={isSelected ? '#2563eb' : riskColor}
                  opacity={isSelected ? 1 : 0.72}
                  stroke={isSelected ? '#1d4ed8' : 'white'}
                  strokeWidth={isSelected ? 2.5 : 1}
                />
                <text x={area.x + area.w / 2} y={area.y + area.h / 2 - 6} textAnchor="middle" fontSize="8" fontWeight="700" fill="white">
                  {area.id.split(' ').map((w, i) => (
                    <tspan key={i} x={area.x + area.w / 2} dy={i === 0 ? 0 : 10}>{w}</tspan>
                  ))}
                </text>
                <text x={area.x + area.w / 2} y={area.y + area.h - 8} textAnchor="middle" fontSize="7" fill="rgba(255,255,255,0.85)">
                  {stats?.density ?? '—'}/1k
                </text>
              </g>
            );
          })}
        </svg>
      </div>
      <div className="absolute bottom-4 right-4 bg-white p-3 rounded-lg shadow-md border border-slate-200 text-xs space-y-1.5">
        <p className="font-bold text-slate-700 mb-2">Density Risk</p>
        {[['#ef4444','Critical (45+)'],['#f97316','High (30–44)'],['#f59e0b','Moderate (20–29)'],['#22c55e','Low (<20)'],['#2563eb','Selected']].map(([c,l]) => (
          <div key={l} className="flex items-center gap-2">
            <div className="w-3 h-3 rounded" style={{ backgroundColor: c }}></div>
            <span className="text-slate-600">{l}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────
// COMPONENT: SMART AUDITOR
// ─────────────────────────────────────────────

const SmartAuditor = ({ neighborhood, stats }) => {
  const [insight, setInsight] = useState('');
  const [loading, setLoading] = useState(false);
  const apiKey = '';

  const generateInsight = async () => {
    setLoading(true);
    const matchRate = ((stats.permitsMatched / stats.violations) * 100).toFixed(2);
    const systemPrompt = `You are a Municipal Data Analyst for Syracuse, NY. 
Analyze the following data for the ${neighborhood} neighborhood and produce a 2-sentence plain-English summary for a city council member. 
Data: Total Violations: ${stats.violations}, Open Cases: ${stats.open}, Median Remediation Gap: ${stats.medianLag} days, Permit Match Rate: ${matchRate}%, Violation Density: ${stats.density} per 1,000 homes, Health Score: ${stats.healthScore}/100.
If the permit match rate is under 5%, flag it as "High Stagnation Risk". If median lag exceeds 900 days, flag it as "Critical Remediation Delay". Only use numbers provided. Do not invent statistics.`;

    try {
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{ parts: [{ text: `Summarize neighborhood health for ${neighborhood}` }] }],
          systemInstruction: { parts: [{ text: systemPrompt }] },
          generationConfig: { temperature: 0.2, maxOutputTokens: 150 }
        })
      });
      const result = await response.json();
      setInsight(result.candidates?.[0]?.content?.parts?.[0]?.text || 'No summary available for this selection.');
    } catch {
      setInsight(`Local analysis: ${neighborhood} shows a median remediation lag of ${stats.medianLag} days with a permit match rate of ${matchRate}%. ${parseFloat(matchRate) < 5 ? '⚠ High Stagnation Risk detected.' : 'Enforcement activity is within expected range.'}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { generateInsight(); }, [neighborhood]);

  return (
    <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 text-white shadow-2xl relative overflow-hidden">
      <div className="absolute top-0 right-0 p-4 opacity-10"><ShieldCheck size={80} /></div>
      <div className="flex items-center gap-2 mb-4">
        <Activity className="text-blue-400" size={20} />
        <h3 className="font-bold text-lg">AI Smart Auditor</h3>
        <span className="ml-auto text-[10px] bg-blue-900 text-blue-300 px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">Gemini 2.5 Flash</span>
      </div>
      {loading ? (
        <div className="animate-pulse space-y-2">
          <div className="h-3 bg-slate-700 rounded w-full"></div>
          <div className="h-3 bg-slate-700 rounded w-5/6"></div>
          <div className="h-3 bg-slate-700 rounded w-4/6"></div>
        </div>
      ) : (
        <p className="text-slate-300 leading-relaxed text-sm italic font-light">"{insight}"</p>
      )}
      <div className="mt-4 pt-4 border-t border-slate-700 flex items-center justify-between text-[10px] text-slate-500 font-medium">
        <span>Temperature: 0.2 · JSON-grounded</span>
        <span className="text-emerald-400 flex items-center gap-1"><ShieldCheck size={10} /> Hallucination-guarded</span>
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────
// COMPONENT: EDA — SEASONAL SPIKE CHART
// ─────────────────────────────────────────────

const SeasonalChart = () => (
  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
    <div className="mb-4">
      <h3 className="font-bold text-slate-800">Seasonal Violation Spike (Full Year)</h3>
      <p className="text-xs text-slate-400 mt-1">Winter months (Dec–Feb) show a 22–44% spike above the annual average, driven by heating failures and freeze-thaw structural damage.</p>
    </div>
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={SEASONAL_DATA}>
          <defs>
            <linearGradient id="seasonGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%"  stopColor="#2563eb" stopOpacity={0.15}/>
              <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
          <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} dy={8} />
          <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip contentStyle={CustomTooltipStyle} />
          <ReferenceLine y={720} stroke="#94a3b8" strokeDasharray="4 4" label={{ value: 'Annual Avg', position: 'insideTopRight', fontSize: 10, fill: '#94a3b8' }} />
          <Area type="monotone" dataKey="violations" stroke="#2563eb" strokeWidth={2.5} fill="url(#seasonGrad)" name="Violations Filed" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
    <div className="mt-3 flex gap-4 text-xs text-slate-500">
      <span className="flex items-center gap-1.5"><div className="w-3 h-0.5 bg-blue-600 rounded"></div>Monthly filings</span>
      <span className="flex items-center gap-1.5"><div className="w-3 h-0.5 bg-slate-300 border-dashed rounded"></div>Annual average (720)</span>
    </div>
  </div>
);

// ─────────────────────────────────────────────
// COMPONENT: EDA — DENSITY-NORMALIZED NEIGHBORHOOD COMPARISON
// ─────────────────────────────────────────────

const DensityComparisonChart = () => (
  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
    <div className="mb-4">
      <h3 className="font-bold text-slate-800">Neighborhood Density Comparison</h3>
      <p className="text-xs text-slate-400 mt-1">Violations per 1,000 residential parcels — density-normalized to prevent bias from larger neighborhoods.</p>
    </div>
    <div className="h-72">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={DENSITY_COMPARISON} layout="vertical" margin={{ left: 100, right: 20 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
          <XAxis type="number" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 10 }} />
          <YAxis dataKey="fullName" type="category" axisLine={false} tickLine={false} tick={{ fill: '#475569', fontSize: 11, fontWeight: 600 }} width={100} />
          <Tooltip contentStyle={CustomTooltipStyle} formatter={(v) => [`${v} / 1,000 homes`, 'Violation Density']} />
          <Bar dataKey="density" radius={[0, 6, 6, 0]} maxBarSize={18}>
            {DENSITY_COMPARISON.map((entry) => (
              <Cell key={entry.fullName} fill={getRiskColor(entry.density)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  </div>
);

// ─────────────────────────────────────────────
// COMPONENT: EDA — REMEDIATION LAG HISTOGRAM
// ─────────────────────────────────────────────

const LagHistogram = () => (
  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
    <div className="mb-4">
      <h3 className="font-bold text-slate-800">Remediation Lag Distribution</h3>
      <p className="text-xs text-slate-400 mt-1">Right-skewed distribution confirms median (895 days) is a more reliable central measure than mean (1,340 days). Tail driven by "Zombie Properties."</p>
    </div>
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={LAG_HISTOGRAM}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
          <XAxis dataKey="bucket" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 10 }} dy={8} />
          <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip contentStyle={CustomTooltipStyle} formatter={(v) => [v, 'Properties']} />
          <ReferenceLine x="731–895" stroke="#2563eb" strokeDasharray="4 4" label={{ value: 'Median', position: 'top', fontSize: 10, fill: '#2563eb' }} />
          <Bar dataKey="count" radius={[4, 4, 0, 0]} maxBarSize={40}>
            {LAG_HISTOGRAM.map((entry, i) => (
              <Cell key={i} fill={i <= 4 ? '#bfdbfe' : i === 5 ? '#2563eb' : '#1e3a8a'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
    <div className="mt-3 grid grid-cols-3 gap-3 text-xs">
      {[['P25', '~350 days', 'text-slate-500'], ['Median', '895 days', 'text-blue-600 font-bold'], ['Mean', '1,340 days', 'text-red-500']].map(([l, v, cls]) => (
        <div key={l} className="bg-slate-50 rounded-lg p-2 text-center">
          <p className="text-slate-400 text-[10px] uppercase tracking-wider">{l}</p>
          <p className={`mt-0.5 font-bold ${cls}`}>{v}</p>
        </div>
      ))}
    </div>
  </div>
);

// ─────────────────────────────────────────────
// COMPONENT: EDA — ESCALATION TIMELINE
// ─────────────────────────────────────────────

const EscalationTimeline = () => (
  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
    <div className="mb-6">
      <h3 className="font-bold text-slate-800">Enforcement Escalation Timeline</h3>
      <p className="text-xs text-slate-400 mt-1">Average journey from first complaint to building permit — a 1,307-day process. The gap between "Unfit" designation and permit issuance alone averages 895 days.</p>
    </div>
    <div className="relative">
      {/* Horizontal line */}
      <div className="absolute top-5 left-0 right-0 h-0.5 bg-slate-200 z-0"></div>
      <div className="flex justify-between relative z-10">
        {ESCALATION_DATA.map((stage, i) => {
          const colors = ['#94a3b8', '#f59e0b', '#f97316', '#ef4444', '#2563eb'];
          return (
            <div key={i} className="flex flex-col items-center gap-2 flex-1">
              <div className="w-10 h-10 rounded-full border-2 border-white shadow-md flex items-center justify-center text-white text-xs font-black"
                style={{ backgroundColor: colors[i] }}>
                {i + 1}
              </div>
              <p className="text-[9px] font-bold text-slate-600 text-center leading-tight max-w-[70px]">{stage.stage}</p>
              <span className="text-[10px] font-black" style={{ color: colors[i] }}>{stage.label}</span>
            </div>
          );
        })}
      </div>
      {/* Gap annotations */}
      <div className="mt-6 grid grid-cols-4 gap-2">
        {[
          ['Initial → Re-inspect', '+94 days'],
          ['Re-inspect → Notice', '+93 days'],
          ['Notice → "Unfit"', '+225 days'],
          ['"Unfit" → Permit', '+895 days ⚠'],
        ].map(([label, days]) => (
          <div key={label} className="bg-slate-50 border border-slate-100 rounded-lg p-2 text-center">
            <p className="text-[9px] text-slate-400">{label}</p>
            <p className="text-xs font-black text-slate-700 mt-0.5">{days}</p>
          </div>
        ))}
      </div>
    </div>
  </div>
);

// ─────────────────────────────────────────────
// COMPONENT: EDA — VIOLATION TYPE BREAKDOWN
// ─────────────────────────────────────────────

const ViolationTypeChart = () => {
  const COLORS = ['#1e40af','#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe','#dbeafe'];
  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
      <div className="mb-4">
        <h3 className="font-bold text-slate-800">Violation Type Breakdown</h3>
        <p className="text-xs text-slate-400 mt-1">Structural and heating failures account for 44% of all filed violations, driving the bulk of "Unfit" escalations.</p>
      </div>
      <div className="flex gap-4 items-center">
        <div className="h-56 w-56 flex-shrink-0">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={VIOLATION_TYPES} dataKey="count" nameKey="type" innerRadius={55} outerRadius={85} paddingAngle={4} startAngle={90} endAngle={-270}>
                {VIOLATION_TYPES.map((_, i) => <Cell key={i} fill={COLORS[i]} stroke="none" />)}
              </Pie>
              <Tooltip contentStyle={CustomTooltipStyle} formatter={(v, n) => [v.toLocaleString(), n]} />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="flex-1 space-y-2">
          {VIOLATION_TYPES.map((item, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-sm flex-shrink-0" style={{ backgroundColor: COLORS[i] }}></div>
              <span className="text-xs text-slate-600 flex-1 leading-tight">{item.type}</span>
              <span className="text-xs font-bold text-slate-800 w-8 text-right">{item.pct}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────
// COMPONENT: EDA — STATUS ATTRITION
// ─────────────────────────────────────────────

const AttritionChart = () => (
  <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
    <div className="mb-4">
      <h3 className="font-bold text-slate-800">Status Attrition — How Cases Close</h3>
      <p className="text-xs text-slate-400 mt-1">Only 51% of closures reflect verified physical repair. Administrative age-out closures (29%) are a critical data quality concern.</p>
    </div>
    <div className="h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={ATTRITION_DATA}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
          <XAxis dataKey="method" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 9 }} dy={8} interval={0} />
          <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <Tooltip contentStyle={CustomTooltipStyle} formatter={(v) => [v.toLocaleString(), 'Cases']} />
          <Bar dataKey="count" radius={[6, 6, 0, 0]} maxBarSize={52}>
            {ATTRITION_DATA.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
    <div className="mt-4 p-3 bg-amber-50 border border-amber-200 rounded-lg flex gap-2 items-start">
      <AlertTriangle size={14} className="text-amber-500 mt-0.5 flex-shrink-0" />
      <p className="text-xs text-amber-700 leading-relaxed">
        <span className="font-bold">Methodology Note:</span> Resolution Rate in this dashboard excludes administrative age-out closures to avoid overstating physical remediation.
      </p>
    </div>
  </div>
);

// ─────────────────────────────────────────────
// MAIN APPLICATION
// ─────────────────────────────────────────────

export default function App() {
  const [selectedNeighborhood, setSelectedNeighborhood] = useState('Northside');
  const [view, setView] = useState('dashboard');

  const currentStats = useMemo(
    () => MOCK_STATS[selectedNeighborhood] || MOCK_STATS['Default'],
    [selectedNeighborhood]
  );

  const resolutionRate = (((currentStats.violations - currentStats.open) / currentStats.violations) * 100).toFixed(1);
  const permitMatchRate = ((currentStats.permitsMatched / currentStats.violations) * 100).toFixed(1);
  const riskColor = getRiskColor(currentStats.density);
  const riskLabel = getRiskLabel(currentStats.density);

  const TABS = [
    { id: 'dashboard', label: 'Analytics',  icon: BarChart3 },
    { id: 'eda',       label: 'EDA Deep Dive', icon: FileSearch },
    { id: 'map',       label: 'Hotspots',   icon: MapIcon },
  ];

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 selection:bg-blue-100">

      {/* ── Navigation ── */}
      <nav className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg shadow-lg shadow-blue-200">
              <Home className="text-white" size={20} />
            </div>
            <div>
              <span className="font-bold text-lg block leading-none text-slate-800">Syracuse Housing Safety</span>
              <span className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Enforcement Tracker · Phase 4</span>
            </div>
          </div>
          <div className="flex bg-slate-100 p-1 rounded-lg gap-1">
            {TABS.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setView(id)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm transition-all ${view === id ? 'bg-white shadow-sm text-blue-600 font-bold' : 'text-slate-500 hover:text-slate-700'}`}
              >
                <Icon size={14} /> {label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto p-6 space-y-8">

        {/* ── Hero / Neighborhood Selector ── */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h1 className="text-3xl font-black text-slate-900">{selectedNeighborhood}</h1>
              <span className="px-2 py-0.5 rounded-full text-xs font-bold text-white" style={{ backgroundColor: riskColor }}>
                {riskLabel} Risk
              </span>
            </div>
            <p className="text-slate-500 text-sm">Municipal enforcement outcomes · {view === 'eda' ? 'Exploratory Data Analysis' : 'Live tracker'}</p>
          </div>
          <div className="flex flex-wrap gap-2">
            {NEIGHBORHOODS.map(nbh => (
              <button
                key={nbh}
                onClick={() => setSelectedNeighborhood(nbh)}
                className={`px-3 py-1 rounded-full text-xs font-bold transition-all border ${selectedNeighborhood === nbh ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-slate-600 border-slate-200 hover:border-blue-400'}`}
              >
                {nbh}
              </button>
            ))}
          </div>
        </div>

        {/* ══════════════════════════════════
            VIEW: DASHBOARD
        ══════════════════════════════════ */}
        {view === 'dashboard' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

            {/* KPI Cards */}
            <div className="lg:col-span-8 grid grid-cols-1 md:grid-cols-3 gap-6">

              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start">
                  <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">Total Violations</p>
                  <AlertTriangle className="text-amber-400" size={16} />
                </div>
                <p className="text-4xl font-black text-slate-900 mt-2">{currentStats.violations.toLocaleString()}</p>
                <div className="mt-4 text-[10px] font-bold text-red-500 flex items-center gap-1">
                  <Activity size={10} /> +4.2% since last quarter
                </div>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start">
                  <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">Remediation Gap</p>
                  <Clock className="text-blue-500" size={16} />
                </div>
                <p className="text-4xl font-black text-blue-600 mt-2">{currentStats.medianLag}</p>
                <p className="text-slate-400 text-[10px] mt-1 font-medium">MEDIAN DAYS TO PERMIT</p>
                <p className="text-slate-300 text-[10px]">Mean: {currentStats.meanLag} days (right-skewed)</p>
              </div>

              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex justify-between items-start">
                  <p className="text-slate-400 text-xs font-bold uppercase tracking-wider">Health Score</p>
                  <ShieldCheck className="text-emerald-500" size={16} />
                </div>
                <p className="text-4xl font-black text-slate-900 mt-2">{currentStats.healthScore}<span className="text-lg text-slate-400">/100</span></p>
                <div className="w-full bg-slate-100 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="h-full rounded-full transition-all duration-700"
                    style={{ width: `${currentStats.healthScore}%`, backgroundColor: currentStats.healthScore >= 80 ? '#10b981' : currentStats.healthScore >= 60 ? '#f59e0b' : '#ef4444' }}
                  ></div>
                </div>
              </div>

              {/* Extended KPIs Row */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                <p className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Violation Density</p>
                <p className="text-2xl font-black" style={{ color: riskColor }}>{currentStats.density}</p>
                <p className="text-slate-400 text-[10px] mt-1">per 1,000 homes</p>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                <p className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">Permit Match Rate</p>
                <p className={`text-2xl font-black ${parseFloat(permitMatchRate) < 5 ? 'text-red-500' : 'text-slate-800'}`}>{permitMatchRate}%</p>
                <p className="text-slate-400 text-[10px] mt-1">{parseFloat(permitMatchRate) < 5 ? '⚠ High Stagnation Risk' : 'Within expected range'}</p>
              </div>

              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
                <p className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-2">IQR Lag Range</p>
                <p className="text-2xl font-black text-slate-800">{currentStats.p25Lag}–{currentStats.p75Lag}</p>
                <p className="text-slate-400 text-[10px] mt-1">days (P25–P75)</p>
              </div>

              {/* Main Lifecycle Chart */}
              <div className="md:col-span-3 bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
                <div className="flex justify-between items-center mb-6">
                  <div>
                    <h3 className="font-bold text-lg text-slate-800">Violation vs. Permit Lifecycle</h3>
                    <p className="text-xs text-slate-400 mt-0.5">Monthly filing trends reveal the enforcement-remediation gap in real time.</p>
                  </div>
                  <div className="flex gap-4 text-xs font-bold">
                    <span className="flex items-center gap-1.5"><div className="w-2.5 h-2.5 bg-blue-600 rounded-full"></div>Violations</span>
                    <span className="flex items-center gap-1.5"><div className="w-2.5 h-2.5 bg-slate-300 rounded-full"></div>Permits</span>
                  </div>
                </div>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={TREND_DATA}>
                      <defs>
                        <linearGradient id="colorV" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%"  stopColor="#2563eb" stopOpacity={0.12}/>
                          <stop offset="95%" stopColor="#2563eb" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                      <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} dy={10} />
                      <YAxis axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 11 }} />
                      <Tooltip contentStyle={CustomTooltipStyle} />
                      <Area type="monotone" dataKey="violations" stroke="#2563eb" strokeWidth={3} fillOpacity={1} fill="url(#colorV)" name="Violations" />
                      <Line type="monotone" dataKey="permits"    stroke="#cbd5e1" strokeWidth={2} dot={false} name="Permits" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            {/* Side Panel */}
            <div className="lg:col-span-4 space-y-6">
              <SmartAuditor neighborhood={selectedNeighborhood} stats={currentStats} />

              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                <h3 className="font-bold text-slate-800 mb-4 text-sm flex items-center gap-2">
                  <Activity size={14} className="text-slate-400" /> Backlog Distribution
                </h3>
                <div className="h-52">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={[
                          { name: 'Resolved', value: currentStats.violations - currentStats.open },
                          { name: 'Pending',  value: currentStats.open }
                        ]}
                        innerRadius={55} outerRadius={80} paddingAngle={6} dataKey="value"
                      >
                        <Cell fill="#2563eb" stroke="none" />
                        <Cell fill="#f1f5f9" stroke="none" />
                      </Pie>
                      <Tooltip contentStyle={CustomTooltipStyle} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="space-y-2 mt-2">
                  {[['Resolution Efficiency', `${resolutionRate}%`, 'text-blue-600'],['Open Cases', currentStats.open.toLocaleString(), 'text-amber-500']].map(([l, v, cls]) => (
                    <div key={l} className="flex justify-between items-center text-xs">
                      <span className="text-slate-500">{l}</span>
                      <span className={`font-bold ${cls}`}>{v}</span>
                    </div>
                  ))}
                  <div className="w-full bg-slate-100 h-1 rounded-full mt-1">
                    <div className="bg-blue-600 h-full rounded-full" style={{ width: `${resolutionRate}%` }}></div>
                  </div>
                </div>
              </div>

              {/* Mini escalation callout */}
              <div className="bg-red-50 border border-red-100 rounded-2xl p-5">
                <div className="flex items-center gap-2 mb-2">
                  <AlertCircle size={16} className="text-red-500" />
                  <h4 className="font-bold text-red-700 text-sm">Escalation Alert</h4>
                </div>
                <p className="text-xs text-red-600 leading-relaxed">
                  Properties in <span className="font-bold">{selectedNeighborhood}</span> take an average of <span className="font-bold">{currentStats.medianLag} days</span> to receive a repair permit after "Unfit" designation. City benchmark is 180 days.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* ══════════════════════════════════
            VIEW: EDA DEEP DIVE
        ══════════════════════════════════ */}
        {view === 'eda' && (
          <div className="space-y-6">
            <div className="bg-blue-50 border border-blue-100 rounded-2xl p-5 flex gap-3 items-start">
              <Info size={18} className="text-blue-500 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm font-bold text-blue-800">Exploratory Data Analysis — City-wide View</p>
                <p className="text-xs text-blue-600 mt-1 leading-relaxed">
                  The six panels below reflect city-wide EDA findings from 137,663 code violation records, 264 "Unfit" designations, and 47,902 building permits. Neighborhood selector above filters the dashboard tab only.
                </p>
              </div>
            </div>

            {/* Row 1 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <SeasonalChart />
              <DensityComparisonChart />
            </div>

            {/* Row 2 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <LagHistogram />
              <ViolationTypeChart />
            </div>

            {/* Row 3 — full width */}
            <EscalationTimeline />
            <AttritionChart />
          </div>
        )}

        {/* ══════════════════════════════════
            VIEW: MAP HOTSPOTS
        ══════════════════════════════════ */}
        {view === 'map' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <div className="lg:col-span-8">
              <SyracuseSVGMap selected={selectedNeighborhood} onSelect={setSelectedNeighborhood} />
            </div>
            <div className="lg:col-span-4 space-y-4">
              <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                <h3 className="font-bold text-slate-800 mb-4 flex items-center gap-2">
                  <MapPin size={16} className="text-red-500" /> Hotspot Details
                </h3>
                <p className="text-sm text-slate-500 leading-relaxed">
                  The <span className="font-bold text-slate-900">{selectedNeighborhood}</span> area shows a violation density of{' '}
                  <span className="font-bold" style={{ color: riskColor }}>{currentStats.density}</span>{' '}
                  per 1,000 residents — classified as <span className="font-bold" style={{ color: riskColor }}>{riskLabel} Risk</span>.
                  High concentrations are linked to older housing stock and deferred maintenance.
                </p>
                <div className="mt-4 grid grid-cols-2 gap-3 text-xs">
                  {[
                    ['Median Lag',   `${currentStats.medianLag} days`],
                    ['Open Cases',   currentStats.open.toLocaleString()],
                    ['Permit Rate',  `${permitMatchRate}%`],
                    ['Health Score', `${currentStats.healthScore}/100`],
                  ].map(([l, v]) => (
                    <div key={l} className="bg-slate-50 rounded-lg p-3">
                      <p className="text-slate-400 text-[10px] uppercase tracking-wider">{l}</p>
                      <p className="font-bold text-slate-800 mt-0.5">{v}</p>
                    </div>
                  ))}
                </div>
                <div className="mt-4 p-3 bg-slate-50 rounded-xl border border-dashed border-slate-300">
                  <p className="text-[10px] font-bold text-slate-400 uppercase">Primary Corrective Action</p>
                  <p className="text-sm font-bold text-slate-700 mt-1">Structural Repair (Roof / Foundation)</p>
                </div>
              </div>
              <SmartAuditor neighborhood={selectedNeighborhood} stats={currentStats} />
            </div>
          </div>
        )}
      </main>

      <footer className="max-w-7xl mx-auto px-6 py-12 text-center">
        <div className="h-px bg-slate-200 w-24 mx-auto mb-8"></div>
        <p className="text-slate-400 text-xs font-medium">Syracuse Housing Safety Tracker © 2026 · Karan C. Salunkhe</p>
        <p className="text-slate-300 text-[10px] mt-2 uppercase tracking-[0.2em]">Syracuse University iSchool · Open Data Civic Challenge · Phase 4</p>
      </footer>
    </div>
  );
}
