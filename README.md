# Workforce Wellness & AI Scheduling System

An intelligent, reactive workforce scheduling system that uses advanced Search Algorithms, Fuzzy Logic, and Rule-Based Inference to distribute tasks equitably while actively tracking and managing employee wellness and fatigue.

## Core AI & Engineering Concepts Implemented

This system was built combining multiple artificial intelligence topologies and modern full-stack software architectures:

### 1. Intelligent Scheduling Kernel (Heuristic A* Search)
The core scheduler utilizes an **A* (A-Star) Search Algorithm** to navigate the highly-constrained state space of employee assignments. It optimizes task placement by minimizing a meticulously designed heuristic cost function ($h(x)$), balancing constraint compliance against fairness penalties and task completion rates. It natively supports skipping unassignable tasks, sending them to a Pending Queue.

### 2. Constraint Satisfaction Problem (CSP) Modeling
The environment strictly enforces hard constraints during state-node expansions:
- **Skill Matching:** Verifies employee capabilities against task requirements.
- **Availability Windows:** Respects start/end time availabilities.
- **Temporal Overlap:** Prevents scheduling multiple tasks concurrently for a single employee.
- **Regulatory Limits:** Prevents violation of maximum daily/weekly working hours.

### 3. Wellness & Physiological State Modeling
The system goes beyond task-matching by actively modeling simulated human factors. A **Wellness Scorer** analyzes stateful variables—_Fatigue (0-10), Stress (0-10), Satisfaction (0-10), and Consecutive Shifts_—to generate quantifiable Health Scores and tag employees into Risk Categories (Excellent, Good, Fair, At Risk).

### 4. Fuzzy Logic Inference System
To handle "soft" qualitative factors, the system features a bespoke, pure-Python **Fuzzy Logic Engine** built from the ground up:
- Uses **Triangular & Trapezoidal Membership Functions** to fuzzify crisp inputs (Fatigue & Stress) into linguistic variables (Low, Medium, High).
- Applies **Mamdani-style Inference Rules** (e.g., *IF Fatigue is High AND Stress is High THEN Workload Reduction is High*).
- Defuzzifies outputs into concrete numerical reduction multipliers and flexibility indexes.

### 5. Rule-Based Expert System (Inference Engine)
A forward-chaining **Inference Engine** runs post-schedule to evaluate both crisp operational constraints and Fuzzy outputs. It triggers discrete, actionable system alerts:
- **Mandatory Break Enforcement:** Triggered when continuous shift limits are breached.
- **Workload Reduction:** Recommends specific percentage reductions based on fuzzy outputs.
- **Rotation Suggestions:** Flags employees who have handled excessively high-priority tasks for too long.

### 6. Fairness & Equity Tracking (Gini Coefficient)
The system employs the statistical **Gini Coefficient**—traditionally used in economics to measure wealth inequality—to track scheduling fairness. It calculates the disparity in "Priority Load" and "Total Hours" across the workforce, directly injecting a `fairness_penalty` back into the A* heuristic to force the AI to self-correct and distribute heavy tasks evenly over time.

### 7. Real-Time Reactive Event Simulation
Simulates real-world operational chaos. The system supports a dynamic **Adjustment Search** routine that triggers when an employee unexpectedly becomes unavailable. It isolates affected assignments and rapidly searches for localized re-assignments to patch the schedule without requiring a full global recalculation.

### 8. Human-in-the-Loop (HITL) Manual Overrides
Acknowledging that AI cannot foresee every business reality, the system implements a strict Manual Reassignment Override mapping. Human managers can instantly bypass heuristic checks via a React dashboard to force-assign pending tasks or swap overloaded employees, instantly generating downward recalculations of Wellness, Fairness, and Constraints.

### 9. Decoupled Microservices Architecture
- **Backend:** A RESTful API driven by **FastAPI** (Python), exposing modular endpoints for `/schedule`, `/wellness`, `/fairness`, and `/reassign-task`.
- **Frontend:** A responsive **React JS** Dashboard featuring dynamic SVG Timeline plotting, asynchronous data fetching, and an interactive 5-tab interface (Timeline, List, Wellness, Fairness, Recommendations).

---

## Running the System

### 1. Terminal / CLI Simulation
To run the full end-to-end Python engine simulation (which prints exhaustive logs of the A* solver, Real-Time Events, Fuzzy Logic calculations, and Gini Scores):
```bash
python main.py
```

### 2. Full-Stack Web App
To run the interactive UI dashboard:
1. **Start the Backend:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
2. **Start the Frontend:**
   ```bash
   cd scheduler-ui
   npm start
   ```