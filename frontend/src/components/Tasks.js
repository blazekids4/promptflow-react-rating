import React, { useState, useEffect } from "react";
import "./Tasks.css";

const Tasks = () => {
  const [tasks, setTasks] = useState(
    JSON.parse(localStorage.getItem("tasks")) || []
  );
  const [completedTasks, setCompletedTasks] = useState(
    JSON.parse(localStorage.getItem("completedTasks")) || []
  );
  const [journalInput, setJournalInput] = useState("");
  const [completedJournalEntries, setCompletedJournalEntries] = useState(
    JSON.parse(localStorage.getItem("completedJournalEntries")) || []
  );
  const [taskInput, setTaskInput] = useState("");
  const [checkedInTask, setCheckedInTask] = useState(null);

  const resetTasks = () => {
    localStorage.clear();
    setTasks([]);
    setCompletedTasks([]);
    setCompletedJournalEntries([]);
    setCheckedInTask(null);
    setJournalInput("");
    setTaskInput("");
  };

  useEffect(() => {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }, [tasks]);

  useEffect(() => {
    localStorage.setItem("completedTasks", JSON.stringify(completedTasks));
  }, [completedTasks]);

  useEffect(() => {
    localStorage.setItem(
      "completedJournalEntries",
      JSON.stringify(completedJournalEntries)
    );
  }, [completedJournalEntries]);

  const addTask = () => {
    if (taskInput.trim()) {
      const newTask = {
        content: taskInput,
        id: Date.now(),
      };
      setTasks([...tasks, newTask]);
      setTaskInput("");
    }
  };

  const checkInTask = (task) => {
    setCheckedInTask(task);
  };

  const completeJournalEntry = () => {
    if (journalInput.trim()) {
      const newJournalEntry = {
        content: journalInput,
        taskId: checkedInTask.id,
        id: Date.now(),
      };
      setCompletedJournalEntries([...completedJournalEntries, newJournalEntry]);
      setCompletedTasks([...completedTasks, checkedInTask]);
      setTasks(tasks.filter((task) => task.id !== checkedInTask.id));
      setCheckedInTask(null);
      setJournalInput("");
    }
  };

  return (
    <div className="tasks-container">
      <input
        className="task-input"
        value={taskInput}
        onChange={(e) => setTaskInput(e.target.value)}
      />
      <button className="add-task-button" onClick={addTask}>
        Add Task
      </button>
      <button className="reset-button" onClick={resetTasks}>
        Reset Tasks
      </button>
      <ul className="task-list">
        {tasks.map((task) => (
          <li className="task-list-item" key={task.id}>
            <div>{task.content}</div>
            <button
              className="check-in-task-button"
              onClick={() => checkInTask(task)}
            >
              Check In
            </button>
            {checkedInTask === task && (
              <>
                <input
                  className="journal-input"
                  value={journalInput}
                  onChange={(e) => setJournalInput(e.target.value)}
                />
                <button
                  className="complete-task-button"
                  onClick={completeJournalEntry}
                >
                  Complete
                </button>
              </>
            )}
          </li>
        ))}
      </ul>
      <h4>Completed Tasks and Journals</h4>
      <table className="completed-tasks-table">
        <thead>
          <tr>
            <th>Task</th>
            <th>Journal Entry</th>
          </tr>
        </thead>
        <tbody>
          {completedTasks.map((task) => {
            const associatedJournalEntry = completedJournalEntries.find(
              (entry) => entry.taskId === task.id
            );
            return (
              <tr key={task.id}>
                <td>{task.content}</td>
                <td>{associatedJournalEntry?.content}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default Tasks;
