# schemas.py
# Pydantic models decide what data is ALLOWED in and what goes out.

from pydantic import BaseModel, Field


# Data coming IN from React
class StudentCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: str = Field(
        ...,
        min_length=5,
        max_length=100
    )

    college: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    course: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    year: int = Field(
        ...,
        ge=1,
        le=5
    )

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15
    )


# Data going OUT to React
class StudentOut(StudentCreate):

    id: int

    # Lets Pydantic read data straight
    # from a SQLAlchemy object
    model_config = {
        "from_attributes": True
    }