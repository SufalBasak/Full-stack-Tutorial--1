# Student Management App

This project is a full-stack student management application built with:

- Frontend: React + Vite
- Backend: FastAPI
- Database: MySQL (Aiven MySQL in production)
- ORM: SQLAlchemy
- Validation: Pydantic
- Environment management: Python dotenv

The app allows users to:

- view all students
- add a new student
- update student information
- delete a student

---

## Project Structure

```text
Curd_demo/
├── backend/
│   ├── .env
│   ├── ca.pem
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── schemas.py
│   └── venv/
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       ├── index.css
│       ├── main.jsx
│       └── components/
│           ├── StudentCard.jsx
│           └── StudentForm.jsx
└── README.md
```

---

## 1. How the frontend works

The frontend is created in React using Vite.

### Main responsibilities

- display students in cards
- show a form for adding and editing students
- send HTTP requests to the backend API
- update the UI after add, update, or delete actions

### Main frontend file

- `frontend/src/App.jsx`

This file:

- stores the student list in React state
- loads students from the backend using `fetch()`
- handles delete action
- passes data to the form component
- updates the UI when data changes

### API call example

```js
const API_URL =
  import.meta.env.VITE_API_URL || "https://full-stack-tutorial-1.onrender.com";

const response = await fetch(`${API_URL}/students`);
const data = await response.json();
```

This means the frontend connects to the backend using the configured backend URL.

---

## 2. How the backend works

The backend is created with FastAPI.

### Main backend file

- `backend/main.py`

This file contains:

- the FastAPI app instance
- all API routes
- CORS setup
- database table creation

### Main route responsibilities

#### Home route

```python
@app.get("/")
def home():
    return {"message": "Student Card API is running"}
```

#### Get all students

```python
@app.get("/students")
def get_students():
    ...
```

#### Get one student

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
    ...
```

#### Create student

```python
@app.post("/students")
def create_student(student: schemas.StudentCreate):
    ...
```

#### Update student

```python
@app.put("/students/{student_id}")
def update_student(student_id: int, student: schemas.StudentCreate):
    ...
```

#### Delete student

```python
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    ...
```

The backend uses SQLAlchemy to interact with the database and Pydantic to validate incoming data.

---

## 3. How the database works

The project uses MySQL.

### Database model

The database table is created in `backend/models.py`.

```python
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    college = Column(String(255), nullable=False)
    course = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=False)
```

This table stores all student records.

### Database connection

The database configuration is handled in `backend/database.py`.

It:

- loads values from the `.env` file
- builds a MySQL connection string
- creates the SQLAlchemy engine
- creates a database session

Example:

```python
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
```

Then it creates:

```python
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)
```

This is the connection between FastAPI and MySQL.

---

## 4. How the backend connects with frontend

The communication between frontend and backend is done through HTTP requests.

### Flow

1. The React app loads in the browser.
2. The frontend calls an API like:
   - `GET /students`
   - `POST /students`
   - `PUT /students/{id}`
   - `DELETE /students/{id}`
3. FastAPI receives the request.
4. FastAPI connects to the MySQL database using SQLAlchemy.
5. Data is read or changed in the database.
6. FastAPI returns JSON data to the frontend.
7. The React app updates the UI.

### Example

Frontend:

```js
const res = await fetch(`${API_URL}/students`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(studentData),
});
```

Backend:

```python
@app.post("/students")
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    return new_student
```

---

## 5. How the backend connects with database

The backend uses SQLAlchemy sessions.

### Session setup

In `backend/database.py`:

```python
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

Then:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

This function gives each API route a database session. The route then queries or modifies the database using ORM objects.

---

## 6. Environment variables

The project uses a `.env` file inside the backend folder.

Example:

```env
DB_HOST=mysql-...aivencloud.com
DB_PORT=23515
DB_USER=avnadmin
DB_PASSWORD=your_password_here
DB_NAME=defaultdb
DB_SSL=true
DB_SSL_CA=ca.pem
```

### Why this matters

- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` are required for the database connection.
- `DB_SSL=true` and `DB_SSL_CA=ca.pem` are required when using Aiven MySQL.

The certificate file `ca.pem` is used to securely connect to the remote database.

---

## 7. Frontend and backend in production

### Backend deployment

The backend is deployed on Render.

Example backend URL:

```text
https://full-stack-tutorial-1.onrender.com
```

### Frontend deployment

The frontend is usually deployed on Vercel.

To connect to the backend in production, the frontend uses:

```js
const API_URL =
  import.meta.env.VITE_API_URL || "https://full-stack-tutorial-1.onrender.com";
```

So the frontend can run locally or in production using the correct backend URL.

---

## 8. CORS

CORS is enabled in the backend so the frontend can call the API.

This is configured in `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This allows requests from local development and deployed frontend URLs.

---

## 9. How the app works end-to-end

The full app flow is:

1. User opens the frontend.
2. React loads and calls the backend route `/students`.
3. FastAPI receives the request.
4. FastAPI uses SQLAlchemy to query the MySQL database.
5. MySQL returns student records.
6. FastAPI sends JSON to the frontend.
7. React renders the student cards.
8. When the user submits a form, the frontend sends POST/PUT/DELETE to the backend.
9. The backend updates the MySQL table.
10. The frontend refreshes the card list.

---

## 10. Local setup

### Backend

```bash
cd Curd_demo/backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

### Frontend

```bash
cd Curd_demo/frontend
npm install
npm run dev
```

---

## 11. Production deployment summary

The app is designed so that:

- backend is hosted on Render
- database is hosted on Aiven MySQL
- frontend is hosted on Vercel or another static hosting service

The connection is made through environment variables and API URLs.

---

## Final note

This project is a small but complete full-stack application that demonstrates how a modern frontend, backend API, and database are connected together in real-world development.

The key idea is:

- frontend handles user interaction
- backend handles business logic and API endpoints
- database stores the actual data
- environment variables keep sensitive information secure

---

If you want, I can also create a second version of this README in a more professional GitHub style with badges, screenshots, and deployment steps.
