function ScheduleView({ data, onReassign }) {
  const schedule = data?.schedule || [];
  const pending = data?.pending || [];
  const idle = data?.idle || [];

  // Assuming data structure has everything flat, or we need all employees for dropdowns.
  // We'll pass the full employees list down from the parent or derive it manually.
  // The API response for `getSchedule()` returns `idle` but not all employees. 
  // Wait, schedule has `{ employee: "Name", ... }` but we need employee IDs for the API.
  // The backend's `getSchedule` returns names, we need IDs. I will update `getSchedule` in backend
  // to return task_id and emp_id as well.
  
  return (
    <div>
      <h2>📋 Scheduled Tasks</h2>
      {schedule.length === 0 ? (
        <p style={{ color: "#6b7280" }}>No tasks scheduled.</p>
      ) : (
        schedule.map((item, index) => (
          <div key={index} style={{
            display: "flex", justifyContent: "space-between", alignItems: "center",
            padding: "12px 16px", margin: "8px 0", background: "white",
            borderRadius: "10px", borderLeft: "4px solid #667eea",
            boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
          }}>
            <div>
              <div style={{ fontWeight: "700", color: "#1f2937", marginBottom: "4px" }}>{item.task}</div>
              <div style={{ fontSize: "12px", color: "#6b7280" }}>
                Assigned to: <strong style={{color:"#4f46e5"}}>{item.employee}</strong> ({item.start}:00 - {item.end}:00)
              </div>
            </div>
            {onReassign && item.task_id && data.all_employees ? (
              <select 
                onChange={(e) => onReassign(item.task_id, parseInt(e.target.value))}
                value=""
                style={{ padding: "6px 10px", borderRadius: "6px", border: "1px solid #d1d5db", fontSize: "12px", cursor: "pointer" }}
              >
                <option value="" disabled>Reassign to...</option>
                {data.all_employees.map(emp => {
                  // Wait, "Scheduled Tasks" don't include the required skill directly in the API. 
                  // But for UI clarity, we can just optionally disable reassigning back to the same person.
                  // If we don't know the exact skill required for this task in the `item` payload, we just let them try.
                  return (
                    <option key={emp.id} value={emp.id} disabled={emp.name === item.employee}>
                      {emp.name}
                    </option>
                  );
                })}
              </select>
            ) : null}
          </div>
        ))
      )}

      <h2 style={{ marginTop: "30px", color: "#991b1b" }}>⏳ Pending Tasks</h2>
      <p style={{ fontSize: "12px", color: "#6b7280", marginBottom: "12px" }}>Tasks the AI couldn't schedule (overlap or missing skills). Assign manually:</p>
      {pending.length === 0 ? (
        <p style={{ color: "#6b7280" }}>No pending tasks.</p>
      ) : (
        pending.map(t => (
          <div key={t.id} style={{
            display: "flex", justifyContent: "space-between", alignItems: "center",
            padding: "12px 16px", margin: "8px 0", background: "#fef2f2",
            borderRadius: "10px", borderLeft: "4px solid #ef4444",
            boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
          }}>
            <div>
              <div style={{ fontWeight: "700", color: "#991b1b", marginBottom: "4px" }}>{t.name}</div>
              <div style={{ fontSize: "12px", color: "#b91c1c" }}>Required Skill: <strong>{t.skill}</strong> • Duration: {t.duration}h</div>
            </div>
            {onReassign && data.all_employees ? (
              <select 
                onChange={(e) => onReassign(t.id, parseInt(e.target.value))}
                value=""
                style={{ padding: "6px 10px", borderRadius: "6px", border: "1px solid #fca5a5", background: "white", fontSize: "12px", cursor: "pointer" }}
              >
                <option value="" disabled>Force Assign to...</option>
                {data.all_employees.map(emp => {
                  const hasSkill = emp.skills && emp.skills.includes(t.skill);
                  return (
                    <option key={emp.id} value={emp.id} disabled={!hasSkill}>
                      {emp.name} {!hasSkill && "(Missing Skill)"}
                    </option>
                  );
                })}
              </select>
            ) : null}
          </div>
        ))
      )}

      <h2 style={{ marginTop: "30px", color: "#065f46" }}>😴 Idle Employees</h2>
      <p style={{ fontSize: "12px", color: "#6b7280", marginBottom: "12px" }}>Employees completely unassigned in this cycle:</p>
      {idle.length === 0 ? (
        <p style={{ color: "#6b7280" }}>No idle employees.</p>
      ) : (
        <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
          {idle.map(e => (
            <div key={e.id} style={{
              padding: "10px 16px", background: "#ecfdf5", border: "1px solid #a7f3d0",
              borderRadius: "20px", color: "#065f46", fontSize: "13px", fontWeight: "600",
              boxShadow: "0 2px 5px rgba(0,0,0,0.02)"
            }}>
              {e.name} <span style={{ fontWeight: "400", fontSize: "11px", color: "#047857" }}>(Skills: {e.skills?.join(", ")})</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default ScheduleView;