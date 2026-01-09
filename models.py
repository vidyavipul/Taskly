from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

# SQLAlchemy ORM model for Users table
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

# SQLAlchemy ORM model for todos table
class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing primary key
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)  # Priority level 1-5
    complete = Column(Boolean, default=False)  # Completion status, defaults to incomplete
    owner = Column(Integer, ForeignKey("users.id"))

    
