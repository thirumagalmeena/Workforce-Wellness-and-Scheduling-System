import React, { useState } from "react";
import { updateWellness } from "../api";

const TAG_COLORS = {
  Excellent: { bg: "#d1fae5", text: "#065f46", border: "#6ee7b7" },
  Good:      { bg: "#dbeafe", text: "#1e3a8a", border: "#93c5fd" },
  Fair:      { bg: "#fef3c7", text: "#92400e", border: "#fcd34d" },
  "At Risk": { bg: "#fee2e2", text: "#991b1b", border: "#fca5a5" },
};

function Bar({ label, value, max = 10, color }) {
  const pct = Math.round((value / max) * 100);
  return (
    <div style={{ marginBottom: "8px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", marginBottom: "3px", color: "#6b7280" }}>
        <span>{label}</span>
        <span>{value.toFixed(1)} / {max}</span>
      </div>
      <div style={{ height: "8px", background: "#e5e7eb", borderRadius: "4px", overflow: "hidden" }}>
        <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: "4px", transition: "width 0.4s ease" }} />
      </div>
    </div>
  );
}

function EmployeeCard({ emp, onUpdate }) {
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({
    fatigue: emp.fatigue,
    stress: emp.stress,
    satisfaction: emp.satisfaction,
  });
  const [saving, setSaving] = useState(false);

  const colors = TAG_COLORS[emp.tag] || TAG_COLORS["Fair"];

  const handleSave = async () => {
    setSaving(true);
    await updateWellness({
      employee_id: emp.employee_id,
      fatigue: parseFloat(form.fatigue),
      stress: parseFloat(form.stress),
      satisfaction: parseFloat(form.satisfaction),
    });
    setSaving(false);
    setEditing(false);
    onUpdate();
  };

  return (
    <div style={{
      background: "white",
      borderRadius: "16px",
      padding: "20px",
      boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
      border: `2px solid ${colors.border}`,
      transition: "transform 0.2s",
    }}
      onMouseEnter={e => e.currentTarget.style.transform = "translateY(-3px)"}
      onMouseLeave={e => e.currentTarget.style.transform = "translateY(0)"}
    >
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
        <div>
          <div style={{ fontWeight: "700", fontSize: "16px", color: "#1f2937" }}>{emp.name}</div>
          <div style={{ fontSize: "11px", color: "#6b7280" }}>ID: {emp.employee_id}</div>
        </div>
        <div style={{
          padding: "4px 12px", borderRadius: "20px",
          background: colors.bg, color: colors.text,
          fontWeight: "700", fontSize: "12px", border: `1px solid ${colors.border}`
        }}>
          {emp.tag}
        </div>
      </div>

      {/* Score Ring */}
      <div style={{ textAlign: "center", marginBottom: "16px" }}>
        <div style={{
          width: "80px", height: "80px", borderRadius: "50%", margin: "0 auto",
          background: `conic-gradient(${colors.border} ${emp.score * 3.6}deg, #e5e7eb 0deg)`,
          display: "flex", alignItems: "center", justifyContent: "center",
          boxShadow: "0 0 0 6px white inset",
          position: "relative",
        }}>
          <div style={{ fontWeight: "800", fontSize: "20px", color: colors.text }}>{Math.round(emp.score)}</div>
        </div>
        <div style={{ fontSize: "11px", color: "#9ca3af", marginTop: "6px" }}>Wellness Score</div>
      </div>

      {/* Bars */}
      {!editing ? (
        <>
          <Bar label="😴 Fatigue"     value={emp.fatigue}      color="#f87171" />
          <Bar label="😤 Stress"      value={emp.stress}       color="#fb923c" />
          <Bar label="😊 Satisfaction" value={emp.satisfaction} color="#34d399" />
          <div style={{ display: "flex", gap: "8px", marginTop: "12px", flexWrap: "wrap" }}>
            <span style={{ fontSize: "11px", background: "#f3f4f6", padding: "3px 8px", borderRadius: "10px" }}>
              🔁 Shifts: {emp.consecutive_shifts}
            </span>
            <span style={{ fontSize: "11px", background: "#f3f4f6", padding: "3px 8px", borderRadius: "10px" }}>
              ⏱️ Hours: {emp.weekly_hours}h
            </span>
            <span style={{ fontSize: "11px", background: "#f3f4f6", padding: "3px 8px", borderRadius: "10px" }}>
              🎯 High-Pri: {emp.high_priority_task_count}
            </span>
          </div>
          <button
            onClick={() => setEditing(true)}
            style={{ marginTop: "14px", width: "100%", padding: "8px", background: "#667eea", color: "white", border: "none", borderRadius: "8px", cursor: "pointer", fontSize: "12px", fontWeight: "600" }}
          >
            ✏️ Update Signals
          </button>
        </>
      ) : (
        <div>
          {["fatigue", "stress", "satisfaction"].map(field => (
            <div key={field} style={{ marginBottom: "10px" }}>
              <label style={{ fontSize: "12px", fontWeight: "600", color: "#374151", textTransform: "capitalize" }}>{field} (0–10)</label>
              <input
                type="number" min="0" max="10" step="0.5"
                value={form[field]}
                onChange={e => setForm(f => ({ ...f, [field]: e.target.value }))}
                style={{ display: "block", width: "100%", padding: "6px 10px", borderRadius: "8px", border: "1px solid #d1d5db", marginTop: "4px", fontSize: "13px", boxSizing: "border-box" }}
              />
            </div>
          ))}
          <div style={{ display: "flex", gap: "8px", marginTop: "8px" }}>
            <button onClick={handleSave} disabled={saving}
              style={{ flex: 1, padding: "8px", background: "#10b981", color: "white", border: "none", borderRadius: "8px", cursor: "pointer", fontWeight: "600", fontSize: "12px" }}>
              {saving ? "Saving..." : "✅ Save"}
            </button>
            <button onClick={() => setEditing(false)}
              style={{ flex: 1, padding: "8px", background: "#e5e7eb", color: "#374151", border: "none", borderRadius: "8px", cursor: "pointer", fontWeight: "600", fontSize: "12px" }}>
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function WellnessDashboard({ data, onUpdate }) {
  if (!data || data.length === 0) {
    return <div style={{ textAlign: "center", color: "#6b7280", padding: "40px" }}>No wellness data available. Run the scheduler first.</div>;
  }

  const avgScore = Math.round(data.reduce((s, e) => s + e.score, 0) / data.length);

  return (
    <div style={{ marginTop: "20px" }}>
      <h2 style={{ marginBottom: "6px" }}>🫀 Employee Wellness Dashboard</h2>
      <p style={{ color: "#6b7280", fontSize: "13px", marginBottom: "20px" }}>
        Team Average Wellness Score: <strong style={{ color: avgScore >= 60 ? "#10b981" : "#ef4444" }}>{avgScore}</strong>
      </p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))", gap: "20px" }}>
        {data.map(emp => (
          <EmployeeCard key={emp.employee_id} emp={emp} onUpdate={onUpdate} />
        ))}
      </div>
    </div>
  );
}

export default WellnessDashboard;
