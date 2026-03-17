function ScheduleView({ data }) {
  // Safely access properties with defaults
  const schedule = data?.schedule || [];
  const pending = data?.pending || [];
  const idle = data?.idle || [];

  return (
    <div>
      <h2>📋 Schedule</h2>
      {schedule.length === 0 ? (
        <p>No schedule yet</p>
      ) : (
        schedule.map((item, index) => (
          <div key={index} style={{
            padding: "10px",
            margin: "5px 0",
            background: "#f0f4f8",
            borderRadius: "8px",
            borderLeft: "4px solid #667eea"
          }}>
            <strong>{item.task}</strong> → {item.employee} 
            <span style={{ color: "#666", marginLeft: "10px" }}>
              ({item.start} - {item.end})
            </span>
          </div>
        ))
      )}

      <h2>⏳ Pending Tasks</h2>
      {pending.length === 0 ? (
        <p>None</p>
      ) : (
        pending.map(t => (
          <div key={t.id} style={{
            padding: "8px",
            margin: "4px 0",
            background: "#fff3cd",
            borderRadius: "4px"
          }}>
            {t.name} (Skill: {t.skill})
          </div>
        ))
      )}

      <h2>😴 Idle Employees</h2>
      {idle.length === 0 ? (
        <p>None</p>
      ) : (
        idle.map(e => (
          <div key={e.id} style={{
            padding: "8px",
            margin: "4px 0",
            background: "#d4edda",
            borderRadius: "4px"
          }}>
            {e.name} (Skills: {e.skills?.join(", ")})
          </div>
        ))
      )}
    </div>
  );
}

export default ScheduleView;