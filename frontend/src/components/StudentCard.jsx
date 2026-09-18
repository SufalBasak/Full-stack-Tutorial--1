// src/components/StudentCard.jsx
// A small component that shows the data it is given.

function StudentCard({ student, onDelete, onEdit }) {
  return (
    <div className="card">
      <h3 className="card-title">Student Card</h3>
      <p><span>ID:</span> {student.id}</p>
      <p><span>Name:</span> {student.name}</p>
      <p><span>Email:</span> {student.email}</p>
      <p><span>College:</span> {student.college}</p>
      <p><span>Course:</span> {student.course}</p>
      <p><span>Year:</span> {student.year}</p>
      <p><span>Phone:</span> {student.phone}</p>

      <div className="card-actions">
        <button className="btn-edit" onClick={() => onEdit(student)}>
          Edit
        </button>

        <button className="btn-delete" onClick={() => onDelete(student.id)}>
          Delete
        </button>
      </div>
    </div>
  );
}

export default StudentCard;