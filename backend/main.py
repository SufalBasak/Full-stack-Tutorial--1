# main.py
# This is the heart of the backend:
# the FastAPI app and all routes.

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas

from database import engine, get_db


# Create the "students" table in MySQL
# if it does not exist yet.
models.Base.metadata.create_all(bind=engine)


# Create the FastAPI application
app = FastAPI(title="Student Card API")


# ---------------------------------------------------------------
# CORS: allow the React app (port 5173)
# to call this API (port 8000)
# ---------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://full-stack-tutorial-1.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------
# HOME
# ---------------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Student Card API is running"
    }


# ---------------------------------------------------------------
# GET ALL STUDENTS
# ---------------------------------------------------------------

@app.get(
    "/students",
    response_model=list[schemas.StudentOut]
)
def get_students(
    db: Session = Depends(get_db)
):
    return db.query(models.Student).all()


# ---------------------------------------------------------------
# GET ONE STUDENT
# ---------------------------------------------------------------

@app.get(
    "/students/{student_id}",
    response_model=schemas.StudentOut
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# ---------------------------------------------------------------
# CREATE STUDENT
# ---------------------------------------------------------------

@app.post(
    "/students",
    response_model=schemas.StudentOut
)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):

    # Is this email already used?
    exists = db.query(models.Student).filter(
        models.Student.email == student.email
    ).first()

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Pydantic -> SQLAlchemy
    new_student = models.Student(
        **student.model_dump()
    )

    # Prepare INSERT
    db.add(new_student)

    # Actually save it in MySQL
    db.commit()

    # Get the new ID from MySQL
    db.refresh(new_student)

    return new_student


# ---------------------------------------------------------------
# UPDATE STUDENT
# ---------------------------------------------------------------

@app.put(
    "/students/{student_id}",
    response_model=schemas.StudentOut
)
def update_student(
    student_id: int,
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):

    existing_student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if existing_student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    email_taken = db.query(models.Student).filter(
        models.Student.email == student.email,
        models.Student.id != student_id
    ).first()

    if email_taken:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    for key, value in student.model_dump().items():
        setattr(existing_student, key, value)

    db.commit()
    db.refresh(existing_student)

    return existing_student


# ---------------------------------------------------------------
# DELETE STUDENT
# ---------------------------------------------------------------

@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)

    db.commit()

    return {
        "message": "Student deleted successfully"
    }