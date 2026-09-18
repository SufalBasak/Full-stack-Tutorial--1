from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import ssl
from urllib.parse import quote_plus

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost").strip()
DB_PORT = os.getenv("DB_PORT", "3306").strip()
DB_USER = os.getenv("DB_USER", "root").strip()
DB_PASSWORD = os.getenv("DB_PASSWORD", "").strip()
DB_NAME = os.getenv("DB_NAME", "student_db").strip()
DB_SSL = os.getenv("DB_SSL", "false").strip().lower() in {"1", "true", "yes", "required"}
DB_SSL_MODE = os.getenv("DB_SSL_MODE", "REQUIRED").strip().upper()
DB_SSL_CA = os.getenv("DB_SSL_CA", "ca.pem").strip()

if "@" in DB_HOST:
    raise ValueError(
        "DB_HOST must be just the server name, for example 'localhost'. "
        "Do not set it like 'root@localhost' or '1234@localhost'. "
        "Use DB_USER for the username and DB_PASSWORD for the password."
    )

missing = [
    key for key, value in {
        "DB_HOST": DB_HOST,
        "DB_PORT": DB_PORT,
        "DB_USER": DB_USER,
        "DB_NAME": DB_NAME,
    }.items() if not value
]

if missing:
    raise ValueError(
        "Missing required MySQL environment values: "
        + ", ".join(missing)
        + ". Create a .env file in the backend folder with DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, and DB_NAME."
    )

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?charset=utf8mb4"
)

connect_args = {}
if DB_SSL:
    if not DB_SSL_CA:
        raise ValueError(
            "DB_SSL is enabled, but DB_SSL_CA is missing. Download the Aiven CA certificate and set DB_SSL_CA to its file path (for example: backend/ca.pem)."
        )

    if not os.path.exists(DB_SSL_CA):
        raise FileNotFoundError(
            f"Aiven CA certificate file not found: {DB_SSL_CA}. Download the certificate from Aiven and save it in the backend folder, then restart the app."
        )

    connect_args["ssl"] = ssl.create_default_context(cafile=DB_SSL_CA)

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()