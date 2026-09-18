import { useState, useEffect } from "react";

import StudentForm from "./components/StudentForm.jsx";
import StudentCard from "./components/StudentCard.jsx";

const API_URL = "http://localhost:8000";

function App() {
  const [students, setStudents] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [editingStudent, setEditingStudent] = useState(null);

  const loadStudents = async () => {
    try {
      setLoading(true);

      const response = await fetch(`${API_URL}/students`);

      if (!response.ok) {
        throw new Error("Bad response");
      }

      const data = await response.json();
      setStudents(data);
      setMessage("");
    } catch (error) {
      setMessage("Failed to load students. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStudents();
  }, []);

  const deleteStudent = async (id) => {
    try {
      const response = await fetch(`${API_URL}/students/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Delete failed");
      }

      setMessage("Student deleted successfully");
      if (editingStudent && editingStudent.id === id) {
        setEditingStudent(null);
      }
      loadStudents();
    } catch (error) {
      setMessage("Could not delete this student");
    }
  };

  return (
    <div className="page">
      <header className="header">
        <h1>Student Card App</h1>
        <p>React + FastAPI + MySQL</p>
      </header>

      <main className="container">
        <StudentForm
          apiUrl={API_URL}
          onStudentAdded={loadStudents}
          setMessage={setMessage}
          editingStudent={editingStudent}
          onEditComplete={() => setEditingStudent(null)}
        />

        {message && <p className="message">{message}</p>}

        <h2 className="section-title">Student Cards</h2>

        {loading && <p className="info">Loading students...</p>}

        {!loading && students.length === 0 && (
          <p className="info">No students yet. Add the first one above.</p>
        )}

        <div className="card-grid">
          {students.map((student) => (
            <StudentCard
              key={student.id}
              student={student}
              onDelete={deleteStudent}
              onEdit={() => setEditingStudent(student)}
            />
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;