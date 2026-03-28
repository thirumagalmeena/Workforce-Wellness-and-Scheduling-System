import React from "react";

const ACTION_STYLES = {
  enforce_break:    { bg: "#fee2e2", text: "#991b1b",  icon: "🔴", label: "Mandatory Break" },
  reduce_workload:  { bg: "#fef3c7", text: "#92400e",  icon: "🟠", label: "Reduce Workload" },
  rotation_needed:  { bg: "#ede9fe", text: "#5b21b6",  icon: "🔄", label: "Rotation Needed" },
  flag_rest:        { bg: "#fee2e2", text: "#7f1d1d",  icon: "⚠️", label: "Rest Flagged" },
  no_action:        { bg: "#d1fae5", text: "#065f46",  icon: "✅", label: "All Good" },
};

function SymptomChecker({ symptom }) {
  const { signals, triggered, rest_recommended, message } = symptom;
  return (
    <div style={{
      borderRadius: "10px", padding: "12px 14px",
      background: rest_recommended ? "#fff7ed" : "#f0fdf4",
      border: `1px solid ${rest_recommended ? "#fed7aa" : "#bbf7d0"}`,
      marginTop: "12px",
    }}>
      <div style={{ fontWeight: "600", fontSize: "12px", marginBottom: "8px", color: rest_recommended ? "#92400e" : "#065f46" }}>
        🩺 Symptom Checker
      </div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "6px", marginBottom: "8px" }}>
        {Object.entries(signals).map(([key, val]) => (
          <span key={key} style={{
            padding: "2px 8px", borderRadius: "10px", fontSize: "11px",
            background: val ? "#fee2e2" : "#f3f4f6",
            color: val ? "#991b1b" : "#6b7280",
            fontWeight: val ? "600" : "400",
          }}>
            {val ? "⚡ " : "• "}{key.replace(/_/g, " ")}
          </span>
        ))}
      </div>
      <div style={{ fontSize: "12px", color: rest_recommended ? "#92400e" : "#065f46" }}>{message}</div>
    </div>
  );
}

function EmployeeRecommendationCard({ emp }) {
  return (
    <div style={{
      background: "white", borderRadius: "14px", padding: "20px",
      boxShadow: "0 4px 16px rgba(0,0,0,0.07)",
      border: emp.actions.includes("enforce_break") || emp.actions.includes("flag_rest")
        ? "2px solid #fca5a5" : "2px solid #e5e7eb",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
        <div style={{ fontWeight: "700", fontSize: "15px", color: "#1f2937" }}>{emp.name}</div>
        <div style={{ display: "flex", gap: "6px", flexWrap: "wrap" }}>
          {emp.actions.map(action => {
            const s = ACTION_STYLES[action] || ACTION_STYLES.no_action;
            return (
              <span key={action} style={{
                padding: "3px 10px", borderRadius: "12px",
                background: s.bg, color: s.text,
                fontSize: "11px", fontWeight: "700",
              }}>
                {s.icon} {s.label}
              </span>
            );
          })}
        </div>
      </div>

      {/* Recommendation Texts */}
      <div style={{ marginBottom: "8px" }}>
        {emp.recommendations.map((rec, i) => (
          <div key={i} style={{
            padding: "10px 14px", borderRadius: "8px",
            background: "#f9fafb", fontSize: "13px",
            color: "#374151", marginBottom: "6px",
            lineHeight: "1.5",
            borderLeft: "3px solid #667eea",
          }}>
            {rec}
          </div>
        ))}
      </div>

      <SymptomChecker symptom={emp.symptom_check} />
    </div>
  );
}

function RecommendationsPanel({ data }) {
  if (!data || data.length === 0) {
    return <div style={{ textAlign: "center", color: "#6b7280", padding: "40px" }}>No recommendations available.</div>;
  }

  // Sort: most urgent first (those with enforce_break or flag_rest)
  const sorted = [...data].sort((a, b) => {
    const urgency = (x) => (x.actions.includes("enforce_break") ? 3 : 0)
      + (x.actions.includes("flag_rest") ? 2 : 0)
      + (x.actions.includes("reduce_workload") ? 1 : 0);
    return urgency(b) - urgency(a);
  });

  const atRiskCount = data.filter(e =>
    e.actions.some(a => ["enforce_break", "flag_rest", "reduce_workload"].includes(a))
  ).length;

  return (
    <div style={{ marginTop: "20px" }}>
      <h2 style={{ marginBottom: "6px" }}>💡 Wellness Recommendations</h2>
      <p style={{ color: "#6b7280", fontSize: "13px", marginBottom: "20px" }}>
        Inference engine analysis · {atRiskCount} of {data.length} employees need attention
      </p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "20px" }}>
        {sorted.map(emp => (
          <EmployeeRecommendationCard key={emp.employee_id} emp={emp} />
        ))}
      </div>
    </div>
  );
}

export default RecommendationsPanel;
