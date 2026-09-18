import { useState, useEffect } from "react";

function StudentForm({
  apiUrl,
  onStudentAdded,
  setMessage,
  editingStudent = null,
  onEditComplete = null
}) {
  const emptyForm = {
    name: "",
    email: "",
    college: "",
    course: "",
    year: "",
    phone: "",
  };

  const [form, setForm] = useState(emptyForm);

  useEffect(() => {
    if (editingStudent) {
      setForm({
        ...editingStudent,
        year: String(editingStudent.year)
      });
    } else {
      setForm(emptyForm);
    }
  }, [editingStudent]);

  const resetForm = () => {
    setForm(emptyForm);
    if (onEditComplete) {
      onEditComplete();
    }
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm({
      ...form,
      [name]: value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (
      !form.name ||
      !form.email ||
      !form.college ||
      !form.course ||
      !form.year ||
      !form.phone
    ) {
      setMessage("Please fill in every field");
      return;
    }

    try {
      const studentData = {
        ...form,
        year: Number(form.year)
      };

      const url = editingStudent
        ? `${apiUrl}/students/${editingStudent.id}`
        : `${apiUrl}/students`;

      const method = editingStudent ? "PUT" : "POST";

      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(studentData)
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      setMessage(
        editingStudent
          ? "Student updated successfully"
          : "Student added successfully"
      );

      resetForm();
      onStudentAdded();
    } catch (error) {
      setMessage(
        editingStudent
          ? "Could not update student. Check the backend and the email."
          : "Could not add student. Check the backend and the email."
      );
    }
  };

  return (
    <form className="form" onSubmit={handleSubmit}>
      <h2 className="section-title">
        {editingStudent ? "Edit Student" : "Add Student"}
      </h2>

      <div className="form-grid">
        <input
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
        />

        <input
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
        />

        <input
          name="college"
          placeholder="College"
          value={form.college}
          onChange={handleChange}
        />

        <input
          name="course"
          placeholder="Course"
          value={form.course}
          onChange={handleChange}
        />

        <input
          name="year"
          placeholder="Year (1-5)"
          type="number"
          value={form.year}
          onChange={handleChange}
        />

        <input
          name="phone"
          placeholder="Phone"
          value={form.phone}
          onChange={handleChange}
        />
      </div>

      <div className="form-actions">
        <button type="submit" className="btn-add">
          {editingStudent ? "Save Changes" : "Add Student"}
        </button>

        {editingStudent && (
          <button type="button" className="btn-cancel" onClick={resetForm}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

export default StudentForm;

