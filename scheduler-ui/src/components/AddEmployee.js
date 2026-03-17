import { useState } from "react";
import { addEmployee } from "../api";

function AddEmployee({ refresh }) {

  const [form, setForm] = useState({
    id: "",
    name: "",
    skills: "",
    available_from: 9,
    available_to: 17,
    max_hours: 6
  });

  const handleSubmit = async () => {

    const emp = {
      ...form,
      id: parseInt(form.id),
      skills: form.skills.split(",")
    };

    await addEmployee(emp);
    refresh();
  };

  return (
    <div>
      <h3>Add Employee</h3>

      <input placeholder="ID" onChange={e => setForm({...form, id: e.target.value})} />
      <input placeholder="Name" onChange={e => setForm({...form, name: e.target.value})} />
      <input placeholder="Skills (comma)" onChange={e => setForm({...form, skills: e.target.value})} />

      <button onClick={handleSubmit}>Add</button>
    </div>
  );
}

export default AddEmployee;