# 🚀 Social Media API

A modern, fast, and scalable **REST API** for a social media platform built with **FastAPI**, **PostgreSQL**, and **JWT Authentication**.

![FastAPI](https://img.shields.io/badge/FastAPI-0.124-009688?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.13-3776ab?style=flat&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=flat&logo=postgresql)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Database Migrations](#-database-migrations)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- ✅ **User Authentication** - JWT-based secure authentication
- ✅ **User Management** - Create, read, update user profiles
- ✅ **Post Management** - Create, read, update, delete posts
- ✅ **Voting System** - Like/unlike posts
- ✅ **CORS Support** - Cross-origin resource sharing enabled
- ✅ **Database Migrations** - Alembic for version control
- ✅ **Password Hashing** - Bcrypt for secure password storage
- ✅ **Role-based Access** - Secure endpoints with JWT tokens
- ✅ **API Documentation** - Interactive Swagger UI & ReDoc

---

## 🛠 Tech Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.124.4 | Web framework |
| **Python** | 3.13+ | Language |
| **PostgreSQL** | Latest | Database |
| **SQLAlchemy** | Latest | ORM |
| **Alembic** | 1.18.1 | Database migrations |
| **Pydantic** | 2.12.5 | Data validation |
| **Python-Jose** | 3.5.0 | JWT tokens |
| **Bcrypt** | 3.2.0 | Password hashing |
| **Passlib** | 1.7.4 | Password utilities |
| **Gunicorn** | 25.1.0 | Production server |
| **Uvicorn** | Latest | ASGI server |

---

## 📁 Project Structure

```
FAST_API/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── oauth2.py            # JWT authentication
│   ├── utils.py             # Utility functions
│   └── routers/
│       ├── auth.py          # Authentication endpoints
│       ├── user.py          # User endpoints
│       ├── post.py          # Post endpoints
│       └── vote.py          # Voting endpoints
├── alembic/                 # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── nginx/                   # Nginx configuration
├── alembic.ini             # Alembic config
├── requirements.txt        # Python dependencies
├── Procfile                # Deployment config
├── gunicorn.service        # Systemd service file
├── .env                    # Environment variables (git ignored)
├── .gitignore             # Git ignore file
├── .env.example           # Example environment file
└── README.md              # This file

```

---

## 🚀 Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- pip & virtualenv
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/gungeakash11/SocialMedia_.git
cd FAST_API
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv myenv
myenv\Scripts\activate

# macOS/Linux
python3 -m venv myenv
source myenv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/social_media_db
SECRET_KEY=your-secret-key-here-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 5: Initialize Database

```bash
# Run Alembic migrations
alembic upgrade head
```

---

## ⚙️ Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/social_media_db

# JWT Configuration
SECRET_KEY=your_super_secret_key_minimum_32_characters_required
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=False
ENVIRONMENT=development
```

---

## 🏃 Running the Application

### Development Mode

```bash
# Using Uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Using Gunicorn with Uvicorn workers
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Access the Application

**Development (Local):**
- **API**: http://localhost:8000
- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

**Production:** Coming soon (domain pending)

---

## 📚 API Documentation

### Authentication Endpoints

#### Login
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### User Endpoints

#### Create User
```http
POST /users/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

#### Get User by ID
```http
GET /users/{user_id}
Authorization: Bearer {access_token}
```

### Post Endpoints

#### Create Post
```http
POST /posts/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "My First Post",
  "content": "This is the content of my post"
}
```

#### Get All Posts
```http
GET /posts/
```

#### Get Post by ID
```http
GET /posts/{post_id}
```

#### Update Post
```http
PUT /posts/{post_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content"
}
```

#### Delete Post
```http
DELETE /posts/{post_id}
Authorization: Bearer {access_token}
```

### Vote Endpoints

#### Vote on Post
```http
POST /vote/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "post_id": 1,
  "dir": 1
}
```

For more detailed API documentation, visit: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

---

## 🗄️ Database Migrations

### Create New Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic history
```

---

## 🌐 Deployment

### Deploy to Heroku

1. Create a `Procfile` (already included):
```
web: gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku config:set DATABASE_URL=your_postgres_url
heroku config:set SECRET_KEY=your_secret_key
heroku releases
```

### Deploy with Nginx & Gunicorn

1. Copy `gunicorn.service` to systemd:
```bash
sudo cp gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start gunicorn
```

2. Configure Nginx (use the `nginx` config file):
```bash
sudo cp nginx /etc/nginx/sites-available/social-media-api
sudo ln -s /etc/nginx/sites-available/social-media-api /etc/nginx/sites-enabled/
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Akash Gunge**
- GitHub: [@gungeakash11](https://github.com/gungeakash11)
- Email: gungeakash11@gmail.com

---

## 📞 Support

If you have any questions or issues, please:
- Open an [Issue](https://github.com/gungeakash11/SocialMedia_/issues)
- Contact the maintainer
- Check the [API Documentation](./API_DOCUMENTATION.md)

---

## 🎯 Roadmap

- [ ] WebSocket support for real-time notifications
- [ ] Image upload functionality
- [ ] Comment system
- [ ] Follow/Unfollow users
- [ ] User profiles with avatars
- [ ] Search functionality
- [ ] Admin dashboard
- [ ] Email verification
- [ ] Password reset functionality
- [ ] Rate limiting

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ by Akash Gunge**
