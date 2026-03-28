import React, { useEffect, useState } from "react";
import {
  getSchedule, reschedule, resetData,
  getWellness, getFairness, getRecommendations,
  reassignTask
} from "../api";
import ScheduleView from "./ScheduleView";
import TimelineView from "./TimelineView";
import AddEmployee from "./AddEmployee";
import AddTask from "./AddTask";
import WellnessDashboard from "./WellnessDashboard";
import FairnessView from "./FairnessView";
import RecommendationsPanel from "./RecommendationsPanel";
import "../App.css";

const TABS = [
  { id: "list",            label: "📋 List View" },
  { id: "timeline",        label: "📅 Timeline" },
  { id: "wellness",        label: "🫀 Wellness" },
  { id: "fairness",        label: "⚖️ Fairness" },
  { id: "recommendations", label: "💡 Recommendations" },
];

function TabButton({ id, label, active, onClick }) {
  return (
    <button
      onClick={() => onClick(id)}
      style={{
        padding: "8px 16px",
        background: active
          ? "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
          : "#e0e0e0",
        color: active ? "white" : "#333",
        border: "none",
        borderRadius: "8px",
        cursor: "pointer",
        fontWeight: "600",
        fontSize: "13px",
        transition: "all 0.2s",
      }}
    >
      {label}
    </button>
  );
}

function Dashboard() {
  const [data, setData] = useState(null);
  const [activeTab, setActiveTab] = useState("list");
  const [wellness, setWellness] = useState([]);
  const [fairness, setFairness] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  const loadSchedule = async () => {
    const res = await getSchedule();
    setData(res);
  };

  const loadWellness = async () => {
    const [w, f, r] = await Promise.all([
      getWellness(),
      getFairness(),
      getRecommendations(),
    ]);
    setWellness(w);
    setFairness(f);
    setRecommendations(r);
  };

  const loadAll = async () => {
    await loadSchedule();
    await loadWellness();
  };

  const handleReschedule = async () => {
    const res = await reschedule();
    setData(res);
    await loadWellness();
  };

  const handleReassign = async (taskId, empId) => {
    const res = await reassignTask(taskId, empId);
    setData(res);
    await loadWellness();
  };

  const handleReset = async () => {
    const res = await resetData();
    setData(res);
    await loadWellness();
  };

  useEffect(() => {
    loadAll();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="container">
      <div className="dashboard">
        <h1>🤖 AI Scheduler Dashboard</h1>

        {/* Action buttons */}
        <div style={{ display: "flex", gap: "10px", marginBottom: "16px", flexWrap: "wrap" }}>
          <button onClick={handleReschedule}>▶ Run Scheduler</button>
          <button
            onClick={handleReset}
            style={{ background: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)" }}
          >
            🔄 Reset to Default
          </button>
        </div>

        {/* Tab Navigation */}
        <div style={{ display: "flex", gap: "8px", marginBottom: "24px", flexWrap: "wrap" }}>
          {TABS.map(tab => (
            <TabButton
              key={tab.id}
              id={tab.id}
              label={tab.label}
              active={activeTab === tab.id}
              onClick={setActiveTab}
            />
          ))}
        </div>

        {/* Add forms (only on schedule tabs) */}
        {(activeTab === "list" || activeTab === "timeline") && (
          <>
            <AddEmployee refresh={loadAll} />
            <AddTask refresh={loadAll} />
          </>
        )}

        {/* Tab Content */}
        {activeTab === "list" && data && <ScheduleView data={data} onReassign={handleReassign} />}
        {activeTab === "timeline" && data && <TimelineView data={data} />}
        {activeTab === "wellness" && (
          <WellnessDashboard data={wellness} onUpdate={loadWellness} />
        )}
        {activeTab === "fairness" && (
          <FairnessView data={fairness} />
        )}
        {activeTab === "recommendations" && (
          <RecommendationsPanel data={recommendations} />
        )}
      </div>
    </div>
  );
}

export default Dashboard;