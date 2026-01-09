# Taskly - FastAPI Todo Application

A robust RESTful API built with FastAPI for managing todos with user authentication and authorization.

## 🚀 Features

- **User Authentication**
  - User registration with password hashing (bcrypt)
  - JWT token-based authentication
  - OAuth2 password flow
  - Secure password storage

- **Todo Management**
  - Create, read, update, and delete todos
  - User-specific todo isolation
  - Priority levels and completion status
  - Todo filtering and querying

- **Database**
  - SQLite database with SQLAlchemy ORM
  - Automatic table creation
  - Relationship management between users and todos

## 🛠️ Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **Passlib** - Password hashing library
- **Python-Jose** - JWT token implementation
- **Uvicorn** - ASGI server

## 📋 Prerequisites

- Python 3.8+
- pip package manager

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/vidyavipul/Taskly.git
cd Taskly
```

2. Create and activate virtual environment:
```bash
python -m venv fastapienv
source fastapienv/bin/activate  # On Windows: fastapienv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🔑 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/` | Register a new user |
| POST | `/token` | Login and get access token |
| GET | `/user` | Get users (with optional filters) |

### Todos

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/todos/` | Get all todos for authenticated user |
| GET | `/todos/{todo_id}` | Get specific todo by ID |
| POST | `/todos/` | Create a new todo |
| PUT | `/todos/{todo_id}` | Update an existing todo |
| DELETE | `/todos/{todo_id}` | Delete a todo |

## 📝 Example Usage

### Register a User
```bash
curl -X POST "http://127.0.0.1:8000/auth/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepass123",
    "role": "user"
  }'
```

### Login
```bash
curl -X POST "http://127.0.0.1:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepass123"
```

### Create a Todo
```bash
curl -X POST "http://127.0.0.1:8000/todos/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project",
    "description": "Finish the FastAPI todo app",
    "priority": 5,
    "complete": false
  }'
```

## 📁 Project Structure

```
TodoApp/
├── main.py              # FastAPI application entry point
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── requirements.txt     # Project dependencies
├── routers/
│   ├── auth.py         # Authentication endpoints
│   └── todos.py        # Todo CRUD endpoints
└── todosapp.db         # SQLite database (auto-generated)
```

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- User-specific data isolation
- SQL injection prevention via ORM
- Input validation with Pydantic

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Vidya Vipul**
- GitHub: [@vidyavipul](https://github.com/vidyavipul)

## 🙏 Acknowledgments

- FastAPI documentation and community
- SQLAlchemy for the excellent ORM
- All contributors who help improve this project
