from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

# SQLite database URL - creates todos.db file in current directory
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# Create database engine - check_same_thread=False allows SQLite to work with FastAPI's threading
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# Session factory for creating database sessions - autocommit=False requires explicit commit
SessionLocal = sessionmaker(autoflush=False, autocommit= False, bind=engine)

# Base class for all ORM models to inherit from
class Base(DeclarativeBase):
    pass