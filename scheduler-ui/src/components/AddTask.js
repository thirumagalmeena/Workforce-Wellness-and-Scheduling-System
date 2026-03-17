import { useState } from "react";
import { addTask } from "../api";

function AddTask({ refresh }) {

  const [form, setForm] = useState({
    id: "",
    name: "",
    skill: "",
    duration: 2,
    deadline: 17,
    priority: 3
  });

  const handleSubmit = async () => {

    const task = {
      ...form,
      id: parseInt(form.id)
    };

    await addTask(task);
    refresh();
  };

  return (
    <div>
      <h3>Add Task</h3>

      <input placeholder="ID" onChange={e => setForm({...form, id: e.target.value})} />
      <input placeholder="Name" onChange={e => setForm({...form, name: e.target.value})} />
      <input placeholder="Skill" onChange={e => setForm({...form, skill: e.target.value})} />

      <button onClick={handleSubmit}>Add</button>
    </div>
  );
}

export default AddTask;