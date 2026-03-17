const BASE = "http://127.0.0.1:8000";

export const getSchedule = async () => {
  try {
    console.log("Fetching from:", `${BASE}/schedule`);
    const res = await fetch(`${BASE}/schedule`);
    const data = await res.json();
    console.log("Received data:", data);
    return data;
  } catch (error) {
    console.error("Error fetching schedule:", error);
    return { schedule: [], pending: [], idle: [] };
  }
};

export const addEmployee = async (data) => {
  try {
    await fetch(`${BASE}/add-employee`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
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
      headers: {"Content-Type": "application/json"},
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

export const resetData = async () => {
  try {
    const res = await fetch(`${BASE}/reset`, { method: "POST" });
    return await res.json();
  } catch (error) {
    console.error("Error resetting data:", error);
    return { schedule: [], pending: [], idle: [] };
  }
};