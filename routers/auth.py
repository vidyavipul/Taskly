from fastapi import APIRouter, Depends, Path, Query, HTTPException
from pydantic import BaseModel, Field
from models import Users
from passlib.context import CryptContext
from typing import Optional, Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError 
from datetime import timedelta, datetime, timezone

# Initialize router for authentication endpoints
router = APIRouter()

SECRET_KEY = 'e2902310d7c3b3df2248e4e58349df4123e49d1d52ad6f0c8a8030482aa3f3e0'
AlGORITHM = 'HS256'

# Configure password hashing with bcrypt algorithm
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') 
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

# Pydantic model to validate parameters passed to api endpoints
class CreateUserRequest(BaseModel):
    email: str = Field(min_length=1)
    username: str = Field(min_length=1)
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    password: str = Field(min_length=8)
    role: str = Field(min_length=1)

# Pydantic model to validate token for authorization
class Token(BaseModel):
    access_token: str
    token_type: str

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Type alias for database dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

# Helper Functions
def authenticate_user(username: str, password: str, db: db_dependency):
    ''''''
    user = db.query(Users).filter(Users.username == username).first()
    if not user: 
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc)
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=AlGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[AlGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user')
        return {'username': username, 'user_id': user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user') 

# Endpoint to register a new user
@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    '''Create a new user'''
    create_user_model = Users(
        username = create_user_request.username,
        email = create_user_request.email,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True
    )
    db.add(create_user_model)
    db.commit()

# Endpoint to retrieve users with optional filters
@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(
    db: db_dependency,
    username: Optional[str] = Query(default=None, min_length=1),
    role: Optional[str] = Query(default=None, min_length=1),
    is_active: Optional[bool]= Query(default=None),
):
    '''Get all users, optionally filter by username, role, is_active'''
    query = db.query(Users)

    # Apply filters if provided
    if username:
        query = db.query(Users).filter(Users.username == username)
    if role:
        query = db.query(Users).filter(Users.role == role)
    if is_active is not None:
        query = db.query(Users).filter(Users.is_active == is_active)
    
    return query.all()
    
# Endpoint for user login and authentication
@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_for_access_token(
    db: db_dependency, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    '''Get access tokens by verifying username and password'''
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail = 'Wrong username or Password')
    token = create_access_token(form_data.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}
    
    