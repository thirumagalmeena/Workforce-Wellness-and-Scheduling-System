import React, { useEffect, useState } from "react";
import { getSchedule, reschedule, resetData } from "../api";
import ScheduleView from "./ScheduleView";
import TimelineView from "./TimelineView";
import AddEmployee from "./AddEmployee";
import AddTask from "./AddTask";
import "../App.css";

function Dashboard() {
  const [data, setData] = useState(null);
  const [viewMode, setViewMode] = useState("list"); // "list" or "timeline"

  const loadData = async () => {
    const res = await getSchedule();
    setData(res);
  };

  const handleReschedule = async () => {
    const res = await reschedule();
    setData(res);
  };

  const handleReset = async () => {
    const res = await resetData();
    setData(res);
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="container">
      <div className="dashboard">
        <h1>🤖 AI Scheduler Dashboard</h1>

        <div style={{ display: "flex", gap: "10px", marginBottom: "20px", flexWrap: "wrap" }}>
          <button onClick={handleReschedule}>
            Run Scheduler
          </button>
          <button 
            onClick={handleReset}
            style={{ 
              background: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
            }}
          >
            🔄 Reset to Default Data
          </button>
          
          {/* View toggle buttons */}
          <div style={{ marginLeft: "auto", display: "flex", gap: "5px" }}>
            <button 
              onClick={() => setViewMode("list")}
              style={{
                background: viewMode === "list" ? "#667eea" : "#e0e0e0",
                color: viewMode === "list" ? "white" : "#333"
              }}
            >
              📋 List View
            </button>
            <button 
              onClick={() => setViewMode("timeline")}
              style={{
                background: viewMode === "timeline" ? "#667eea" : "#e0e0e0",
                color: viewMode === "timeline" ? "white" : "#333"
              }}
            >
              📅 Timeline View
            </button>
          </div>
        </div>

        <AddEmployee refresh={loadData} />
        <AddTask refresh={loadData} />

        {data && (
          <>
            {viewMode === "list" ? (
              <ScheduleView data={data} />
            ) : (
              <TimelineView data={data} />
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default Dashboard;