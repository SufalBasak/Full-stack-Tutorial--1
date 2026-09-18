# models.py
# This file describes the MySQL table using a Python class.

from sqlalchemy import Column, Integer, String
from database import Base


class Student(Base):

    # The real table name inside MySQL
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        nullable=False,
        unique=True
    )

    college = Column(
        String(150),
        nullable=False
    )

    course = Column(
        String(100),
        nullable=False
    )

    year = Column(
        Integer,
        nullable=False
    )

    phone = Column(
        String(15),
        nullable=False
    )