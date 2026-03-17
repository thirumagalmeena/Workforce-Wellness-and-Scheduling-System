import React from "react";
import moment from "moment";

function TimelineView({ data }) {
  console.log("TimelineView received data:", data);

  if (!data) {
    return <div>Loading timeline data...</div>;
  }

  if (!data.schedule || data.schedule.length === 0) {
    return (
      <div style={{ padding: "20px", textAlign: "center", color: "#666" }}>
        <p>No schedule to display. Run the scheduler first!</p>
      </div>
    );
  }

  // Get unique employees
  const employees = [...new Set(data.schedule.map(item => item.employee))];
  
  // Preferred order
  const preferredOrder = ["Carol", "David", "Bob", "Alice"];
  employees.sort((a, b) => {
    const indexA = preferredOrder.indexOf(a);
    const indexB = preferredOrder.indexOf(b);
    if (indexA === -1) return 1;
    if (indexB === -1) return -1;
    return indexA - indexB;
  });

  // Hours from 8 to 20
  const hours = Array.from({ length: 13 }, (_, i) => i + 8);

  const getTaskForEmployeeAtHour = (employee, hour) => {
    return data.schedule.find(item => 
      item.employee === employee && 
      hour >= item.start && 
      hour < item.end
    );
  };

  const getTaskColor = (taskName) => {
    if (taskName.toLowerCase().includes("database")) return "#48bb78";
    if (taskName.toLowerCase().includes("repository")) return "#ed8936";
    if (taskName.toLowerCase().includes("cleaning")) return "#9f7aea";
    return "#4299e1";
  };

  return (
    <div style={{ marginTop: "30px" }}>
      <h2>📅 Schedule Timeline</h2>
      
      <div style={{ 
        background: "white", 
        borderRadius: "10px",
        boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
        overflowX: "auto"
      }}>
        {/* Header */}
        <div style={{ display: "flex", borderBottom: "2px solid #e2e8f0" }}>
          <div style={{ 
            width: "150px", 
            padding: "15px 10px",
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            color: "white",
            fontWeight: "600",
            fontSize: "12px"
          }}>
            Employee
          </div>
          {hours.map(hour => (
            <div key={hour} style={{ 
              width: "80px", 
              padding: "10px",
              background: "#f7fafc",
              borderLeft: "1px solid #e2e8f0",
              textAlign: "center",
              fontWeight: "500",
              color: "#4a5568",
              fontSize: "11px"
            }}>
              {hour.toString().padStart(2, '0')}:00
            </div>
          ))}
        </div>

        {/* Employee Rows */}
        {employees.map(employee => (
          <div key={employee} style={{ display: "flex", borderBottom: "1px solid #e2e8f0" }}>
            <div style={{ 
              width: "150px", 
              padding: "15px 10px",
              background: "#f7fafc",
              fontWeight: "600",
              color: "#2d3748",
              borderRight: "2px solid #e2e8f0"
            }}>
              {employee}
            </div>

            {hours.map(hour => {
              const task = getTaskForEmployeeAtHour(employee, hour);
              const bgColor = task ? getTaskColor(task.task) : "#f7fafc";
              const isStartOfTask = task && task.start === hour;
              
              return (
                <div key={`${employee}-${hour}`} style={{ 
                  width: "80px",
                  height: "60px",
                  borderLeft: "1px solid #e2e8f0",
                  backgroundColor: bgColor,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: task ? "white" : "transparent",
                  fontSize: "11px",
                  fontWeight: "500",
                  textAlign: "center",
                  padding: "5px",
                  cursor: task ? "pointer" : "default",
                  boxShadow: task ? "0 2px 4px rgba(0,0,0,0.1)" : "none"
                }}
                title={task ? task.task : ""}
                >
                  {isStartOfTask ? task.task : ""}
                </div>
              );
            })}
          </div>
        ))}
      </div>

      {/* Legend */}
      <div style={{ 
        display: "flex", 
        gap: "20px", 
        marginTop: "20px",
        padding: "15px",
        background: "#f7fafc",
        borderRadius: "8px",
        flexWrap: "wrap"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <div style={{ width: "20px", height: "20px", background: "#4299e1", borderRadius: "4px" }}></div>
          <span>Other Tasks</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <div style={{ width: "20px", height: "20px", background: "#48bb78", borderRadius: "4px" }}></div>
          <span>Database Tasks</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <div style={{ width: "20px", height: "20px", background: "#ed8936", borderRadius: "4px" }}></div>
          <span>Repository Tasks</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <div style={{ width: "20px", height: "20px", background: "#9f7aea", borderRadius: "4px" }}></div>
          <span>Data Cleaning</span>
        </div>
      </div>
    </div>
  );
}

export default TimelineView;