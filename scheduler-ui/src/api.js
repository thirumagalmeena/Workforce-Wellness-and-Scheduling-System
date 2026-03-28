const BASE = "http://127.0.0.1:8000";

export const getSchedule = async () => {
  try {
    const res = await fetch(`${BASE}/schedule`);
    return await res.json();
  } catch (error) {
    console.error("Error fetching schedule:", error);
    return { schedule: [], pending: [], idle: [] };
  }
};

export const addEmployee = async (data) => {
  try {
    await fetch(`${BASE}/add-employee`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  } catch (error) {
    console.error("Error adding employee:", error);
  }
};

export const addTask = async (data) => {
  try {
    await fetch(`${BASE}/add-task`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  } catch (error) {
    console.error("Error adding task:", error);
  }
};

export const reschedule = async () => {
  try {
    const res = await fetch(`${BASE}/reschedule`, { method: "POST" });
    return await res.json();
  } catch (error) {
    console.error("Error rescheduling:", error);
    return { schedule: [], pending: [], idle: [] };
  }
};

export const reassignTask = async (taskId, employeeId) => {
  try {
    const res = await fetch(`${BASE}/reassign-task`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task_id: taskId, employee_id: employeeId }),
    });
    return await res.json();
  } catch (error) {
    console.error("Error reassiging task:", error);
    return { schedule: [], pending: [], idle: [] };
  }
};

export const resetData = async () => {
  try {
    const res = await fetch(`${BASE}/reset`, { method: "POST" });
    return await res.json();
  } catch (error) {
    console.error("Error resetting data:", error);
    return { schedule: [], pending: [], idle: [] };
  }
};

// ── Wellness API ──────────────────────────────────────────────────────────────

export const getWellness = async () => {
  try {
    const res = await fetch(`${BASE}/wellness`);
    const data = await res.json();
    return data.wellness || [];
  } catch (error) {
    console.error("Error fetching wellness:", error);
    return [];
  }
};

export const getFairness = async () => {
  try {
    const res = await fetch(`${BASE}/fairness`);
    return await res.json();
  } catch (error) {
    console.error("Error fetching fairness:", error);
    return null;
  }
};

export const getRecommendations = async () => {
  try {
    const res = await fetch(`${BASE}/recommendations`);
    const data = await res.json();
    return data.recommendations || [];
  } catch (error) {
    console.error("Error fetching recommendations:", error);
    return [];
  }
};

export const updateWellness = async (payload) => {
  try {
    const res = await fetch(`${BASE}/update-wellness`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return await res.json();
  } catch (error) {
    console.error("Error updating wellness:", error);
    return { error: "Failed to update" };
  }
};