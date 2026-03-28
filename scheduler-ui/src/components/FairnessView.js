import React from "react";

const SUGGESTION_COLORS = {
  lighter:  { bg: "#fee2e2", text: "#991b1b", icon: "🔄" },
  heavier:  { bg: "#d1fae5", text: "#065f46", icon: "⬆️" },
  balanced: { bg: "#dbeafe", text: "#1e3a8a", icon: "✅" },
};

function MiniBar({ value, max, color }) {
  const pct = Math.round((value / Math.max(max, 1)) * 100);
  return (
    <div style={{ flex: 1, height: "10px", background: "#e5e7eb", borderRadius: "5px", overflow: "hidden" }}>
      <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: "5px", transition: "width 0.5s ease" }} />
    </div>
  );
}

function FairnessView({ data }) {
  if (!data) {
    return <div style={{ textAlign: "center", color: "#6b7280", padding: "40px" }}>No fairness data available.</div>;
  }

  const { scores, rotation_suggestions: suggestions } = data;
  if (!scores) return null;

  const maxPriority = Math.max(...scores.per_employee.map(e => e.priority_load), 1);
  const maxHours    = Math.max(...scores.per_employee.map(e => e.total_hours), 1);

  const giniColor = (g) => g < 0.15 ? "#10b981" : g < 0.3 ? "#f59e0b" : "#ef4444";

  return (
    <div style={{ marginTop: "20px" }}>
      <h2 style={{ marginBottom: "6px" }}>⚖️ Shift Rotation & Fairness</h2>
      <p style={{ color: "#6b7280", fontSize: "13px", marginBottom: "20px" }}>
        Long-term task distribution analysis using Gini coefficient
      </p>

      {/* Summary Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: "16px", marginBottom: "30px" }}>
        <div style={{ background: "white", borderRadius: "12px", padding: "20px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)", textAlign: "center" }}>
          <div style={{ fontSize: "32px", fontWeight: "800", color: giniColor(scores.gini_priority) }}>{scores.gini_priority.toFixed(3)}</div>
          <div style={{ fontSize: "12px", color: "#6b7280", marginTop: "4px" }}>Gini (Priority)</div>
          <div style={{ fontSize: "10px", color: "#9ca3af" }}>0 = perfect equality</div>
        </div>
        <div style={{ background: "white", borderRadius: "12px", padding: "20px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)", textAlign: "center" }}>
          <div style={{ fontSize: "32px", fontWeight: "800", color: giniColor(scores.gini_hours) }}>{scores.gini_hours.toFixed(3)}</div>
          <div style={{ fontSize: "12px", color: "#6b7280", marginTop: "4px" }}>Gini (Hours)</div>
          <div style={{ fontSize: "10px", color: "#9ca3af" }}>0 = perfect equality</div>
        </div>
        <div style={{ background: "white", borderRadius: "12px", padding: "20px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)", textAlign: "center" }}>
          <div style={{
            fontSize: "32px", fontWeight: "800",
            color: scores.fairness_pct >= 70 ? "#10b981" : scores.fairness_pct >= 50 ? "#f59e0b" : "#ef4444"
          }}>{scores.fairness_pct}%</div>
          <div style={{ fontSize: "12px", color: "#6b7280", marginTop: "4px" }}>Fairness Score</div>
          <div style={{ fontSize: "10px", color: "#9ca3af" }}>higher = more balanced</div>
        </div>
      </div>

      {/* Per-Employee Bars */}
      <div style={{ background: "white", borderRadius: "12px", padding: "20px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)", marginBottom: "24px" }}>
        <h3 style={{ marginBottom: "16px", fontSize: "14px", color: "#374151" }}>Priority-Weighted Load Distribution</h3>
        {scores.per_employee.map(emp => (
          <div key={emp.employee_id} style={{ marginBottom: "14px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "4px" }}>
              <div style={{ width: "80px", fontWeight: "600", fontSize: "13px", color: "#1f2937", flexShrink: 0 }}>{emp.name}</div>
              <MiniBar value={emp.priority_load} max={maxPriority} color="linear-gradient(90deg, #667eea, #764ba2)" />
              <div style={{ width: "60px", textAlign: "right", fontSize: "12px", color: "#6b7280", flexShrink: 0 }}>
                {emp.priority_load.toFixed(1)} pts
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
              <div style={{ width: "80px", fontSize: "11px", color: "#9ca3af", flexShrink: 0 }}>hours</div>
              <MiniBar value={emp.total_hours} max={maxHours} color="linear-gradient(90deg, #f093fb, #f5576c)" />
              <div style={{ width: "60px", textAlign: "right", fontSize: "12px", color: "#6b7280", flexShrink: 0 }}>
                {emp.total_hours.toFixed(1)} h
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Rotation Suggestions */}
      <div style={{ background: "white", borderRadius: "12px", padding: "20px", boxShadow: "0 2px 12px rgba(0,0,0,0.07)" }}>
        <h3 style={{ marginBottom: "16px", fontSize: "14px", color: "#374151" }}>🔄 Rotation Suggestions (Next Cycle)</h3>
        {(suggestions || []).map((s, i) => {
          const c = SUGGESTION_COLORS[s.suggestion] || SUGGESTION_COLORS.balanced;
          return (
            <div key={i} style={{
              padding: "12px 16px", borderRadius: "10px",
              background: c.bg, color: c.text,
              marginBottom: "8px", fontSize: "13px", fontWeight: "500",
            }}>
              {s.message}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default FairnessView;
