import React, { useState, useEffect } from "react";
import "./Tasks.css";

const Tasks = () => {
  const [tasks, setTasks] = useState(JSON.parse(localStorage.getItem('tasks')) || []); 
  const [completedTasks, setCompletedTasks] = useState(JSON.parse(localStorage.getItem('completedTasks')) || []);
  const [journal, setJournal] = useState(JSON.parse(localStorage.getItem('journal')) || []);
  const [taskInput, setTaskInput] = useState("");
  const [journalInput, setJournalInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
  }, [tasks]);

  useEffect(() => {
    localStorage.setItem('completedTasks', JSON.stringify(completedTasks));
  }, [completedTasks]);

  useEffect(() => {
    localStorage.setItem('journal', JSON.stringify(journal));
  }, [journal]);

  const addTask = () => {
    if (taskInput.trim()) {
      const newTask = { content: taskInput, is_completed: false, id: Date.now() };
      setTasks([...tasks, newTask]);
      setTaskInput("");
    }
  };

  const completeTask = (task) => {
    const updatedTasks = tasks.filter((t) => t.id !== task.id);
    const updatedCompletedTasks = [...completedTasks, { ...task, is_completed: true }];

    setTasks(updatedTasks);
    setCompletedTasks(updatedCompletedTasks);
  };

  const journalAboutTask = (task) => {
    if (journalInput.trim()) {
      const newJournalEntry = {
        content: journalInput,
        taskId: task.id,
        id: Date.now(),
      };

      setJournal([...journal, newJournalEntry]);
      setJournalInput("");
    }
  };  

  return (
    <div className="tasks-container">
        <input
          className="task-input"
          value={taskInput}
          onChange={(e) => setTaskInput(e.target.value)}
          disabled={isLoading}
        />
        <>
          <button className="add-task-button" onClick={addTask} disabled={isLoading}>
            {isLoading ? "Adding..." : "Add Task"}
          </button>
          <ul className="task-list">
            {tasks.map((task) => (
              <li className="task-list-item" key={task.id}>
                <div>{task.content}</div>
                <button
                  className="complete-task-button"
                  onClick={() => completeTask(task)}
                >
                  Complete
                </button>
              </li>
            ))}
          </ul>
          <h4>Accomplished</h4>
          {completedTasks.map((task) => (
            <div className="completed-task" key={task.id}>
              {task.content}
              <input
                className="journal-input"
                value={journalInput}
                onChange={(e) => setJournalInput(e.target.value)}
                placeholder="Journal about the task"
              />
              <button
                className="add-journal-button"
                onClick={() => journalAboutTask(task)}
              >
                Add Journal Entry
              </button>
            </div>
          ))}
          <h4>Journal</h4>
          {journal.map((entry, index) => (
            <div className="journal-entry" key={index}>
              <p className="journal-text">{entry.content}</p>
            </div>
          ))}
        </>
    </div>
  );
};

export default Tasks;