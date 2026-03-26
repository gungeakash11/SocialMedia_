# API Documentation - Social Media API

## Overview
This document provides a comprehensive guide to all API endpoints, request bodies, response bodies, and data flows.

---

## Table of Contents
1. [Authentication Endpoints](#authentication-endpoints)
2. [User Endpoints](#user-endpoints)
3. [Post Endpoints](#post-endpoints)
4. [Vote Endpoints](#vote-endpoints)
5. [Data Models & Schemas](#data-models--schemas)
6. [Response Status Codes](#response-status-codes)

---

## Authentication Endpoints

### 1. Login (Create Access Token)
**Endpoint:** `POST /login`

**Purpose:** Authenticate user and receive JWT access token

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "securePassword123"
}
```
- `username`: User's email address
- `password`: User's password (plain text)

**Response Body (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
- `access_token`: JWT token for authenticated requests
- `token_type`: Always "bearer"

**Error Responses:**
- `404 NOT FOUND`: Invalid credentials (wrong email or password)

**Data Flow:**
1. Client sends email & password
2. API checks if user exists
3. API verifies password hash
4. If valid → Generate JWT token → Return token
5. If invalid → Return error

---

## User Endpoints

### 1. Create User (Register)
**Endpoint:** `POST /users`

**Purpose:** Register a new user account

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "securePassword123"
}
```
- `email`: Valid email address (must be unique)
- `password`: Password string (will be hashed before storage)

**Response Body (201 CREATED):**
```json
{
  "id": 1,
  "email": "newuser@example.com",
  "created_at": "2026-02-11T10:30:45.123456Z"
}
```
- `id`: Auto-generated user ID
- `email`: User's email
- `created_at`: Account creation timestamp

**Data Flow:**
1. Receive email & password
2. Hash the password using bcrypt
3. Create new User record in database
4. Return user info (password NOT included in response)

---

### 2. Get User by ID
**Endpoint:** `GET /users/{id}`

**Purpose:** Retrieve specific user information

**Path Parameters:**
- `id`: User ID (integer)

**Response Body (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2026-02-11T10:30:45.123456Z"
}
```

**Error Responses:**
- `404 NOT FOUND`: User with given ID doesn't exist

---

### 3. Get All Users
**Endpoint:** `GET /users`

**Purpose:** Retrieve all users in the system

**Response Body (200 OK):**
```json
[
  {
    "id": 1,
    "email": "user1@example.com",
    "created_at": "2026-02-11T10:30:45.123456Z"
  },
  {
    "id": 2,
    "email": "user2@example.com",
    "created_at": "2026-02-11T10:35:20.654321Z"
  }
]
```

---

## Post Endpoints

### 1. Create Post
**Endpoint:** `POST /posts`

**Authentication:** Required (Bearer token)

**Purpose:** Create a new post

**Request Body:**
```json
{
  "title": "My First Post",
  "content": "This is the content of my first post. It can be quite long!",
  "published": true
}
```
- `title`: Post title (required)
- `content`: Post content/body (required)
- `published`: Boolean flag to publish post (default: true)

**Response Body (201 CREATED):**
```json
{
  "id": 1,
  "title": "My First Post",
  "content": "This is the content of my first post...",
  "published": true,
  "created_at": "2026-02-11T11:00:00.000000Z",
  "owner_id": 5,
  "owner": {
    "id": 5,
    "email": "user@example.com",
    "created_at": "2026-02-11T10:30:45.123456Z"
  }
}
```
- `id`: Auto-generated post ID
- `owner_id`: ID of user who created the post
- `owner`: Complete user object who owns the post
- `created_at`: Post creation timestamp

**Data Flow:**
1. Client sends post data + JWT token
2. Extract current user from token
3. Create Post with owner_id = current user
4. Return post with owner details

---

### 2. Get All Posts
**Endpoint:** `GET /posts`

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `limit`: Number of posts to return (default: 5)
- `skip`: Number of posts to skip/skip (default: 0, for pagination)
- `search`: Search term to filter posts by title (default: "", no filter)

**Example Request:**
```
GET /posts?limit=10&skip=0&search=python
```

**Response Body (200 OK):**
```json
[
  {
    "Post": {
      "id": 1,
      "title": "Python Tips",
      "content": "Here are some python tips...",
      "published": true,
      "created_at": "2026-02-11T11:00:00.000000Z",
      "owner_id": 5,
      "owner": {
        "id": 5,
        "email": "user@example.com",
        "created_at": "2026-02-11T10:30:45.123456Z"
      }
    },
    "votes": 4
  },
  {
    "Post": {
      "id": 2,
      "title": "Python Tutorial",
      "content": "Learn python from scratch...",
      "published": true,
      "created_at": "2026-02-11T11:15:30.000000Z",
      "owner_id": 3,
      "owner": {
        "id": 3,
        "email": "author@example.com",
        "created_at": "2026-02-11T09:00:00.000000Z"
      }
    },
    "votes": 7
  }
]
```
- `Post`: Complete post object
- `votes`: Count of votes on this post

**Data Flow:**
1. Client requests posts with filters
2. Query posts from database
3. Join with Vote table to count votes per post
4. Filter by search term & apply limit/skip
5. Group by post ID and count votes
6. Return posts with vote counts

---

### 3. Get Single Post
**Endpoint:** `GET /posts/{id}`

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `id`: Post ID (integer)

**Response Body (200 OK):**
```json
{
  "Post": {
    "id": 1,
    "title": "My First Post",
    "content": "This is my first post content...",
    "published": true,
    "created_at": "2026-02-11T11:00:00.000000Z",
    "owner_id": 5,
    "owner": {
      "id": 5,
      "email": "user@example.com",
      "created_at": "2026-02-11T10:30:45.123456Z"
    }
  },
  "votes": 3
}
```

**Error Responses:**
- `404 NOT FOUND`: Post with given ID doesn't exist

---

### 4. Update Post
**Endpoint:** `PUT /posts/{id}`

**Authentication:** Required (Bearer token)

**Authorization:** Only post owner can update

**Path Parameters:**
- `id`: Post ID to update

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content goes here",
  "published": true
}
```

**Response Body (202 ACCEPTED):**
```json
{
  "id": 1,
  "title": "Updated Title",
  "content": "Updated content goes here",
  "published": true,
  "created_at": "2026-02-11T11:00:00.000000Z",
  "owner_id": 5,
  "owner": {
    "id": 5,
    "email": "user@example.com",
    "created_at": "2026-02-11T10:30:45.123456Z"
  }
}
```

**Error Responses:**
- `404 NOT FOUND`: Post doesn't exist
- `403 FORBIDDEN`: Current user is not post owner

**Data Flow:**
1. Client sends update data + JWT token + post ID
2. Extract current user from token
3. Find post by ID
4. Check if current user owns the post
5. If owner → Update post fields → Return updated post
6. If not owner → Return 403 Forbidden

---

### 5. Delete Post
**Endpoint:** `DELETE /posts/{id}`

**Authentication:** Required (Bearer token)

**Authorization:** Only post owner can delete

**Path Parameters:**
- `id`: Post ID to delete

**Response:** `204 NO CONTENT` (empty body)

**Error Responses:**
- `404 NOT FOUND`: Post doesn't exist
- `403 FORBIDDEN`: Current user is not post owner

**Data Flow:**
1. Client sends delete request + JWT token + post ID
2. Extract current user from token
3. Find post by ID
4. Check if current user owns the post
5. If owner → Delete post from database → Return 204
6. If not owner → Return 403 Forbidden

---

## Vote Endpoints

### 1. Vote on Post
**Endpoint:** `POST /vote`

**Authentication:** Required (Bearer token)

**Purpose:** Add or remove vote on a post

**Request Body:**
```json
{
  "post_id": 1,
  "dir": 1
}
```
- `post_id`: ID of post to vote on
- `dir`: Vote direction
  - `1`: Add vote (upvote)
  - `0`: Remove vote

**Response Body (201 CREATED):**
```json
{
  "message": "Vote added successfully"
}
```

OR (when removing vote):
```json
{
  "message": "Vote removed successfully"
}
```

**Error Responses:**
- `404 NOT FOUND`: Post doesn't exist
- `404 NOT FOUND`: Trying to remove vote that doesn't exist
- `409 CONFLICT`: User already voted on this post

**Data Flow:**

**For Adding Vote (dir=1):**
1. Client sends post_id & dir=1 + JWT token
2. Extract current user from token
3. Check if post exists
4. Check if user already voted on this post
5. If already voted → Return 409 Conflict
6. If not voted → Create new Vote record → Return success message

**For Removing Vote (dir=0):**
1. Client sends post_id & dir=0 + JWT token
2. Extract current user from token
3. Check if post exists
4. Check if user's vote exists on this post
5. If vote exists → Delete vote → Return success message
6. If no vote found → Return 404 Not Found

---

## Data Models & Schemas

### User Schema
**Request (UserCreate):**
```
email: EmailStr (required)
password: str (required)
```

**Response (UserOut):**
```
id: int
email: str
created_at: datetime
```

---

### Post Schemas

**Request (PostCreate):**
```
title: str (required)
content: str (required)
published: bool (optional, default: true)
```

**Response (Post):**
```
id: int
title: str
content: str
published: bool
created_at: datetime
owner_id: int
owner: UserOut (nested user object)
```

**Response with Votes (PostOut):**
```
Post: Post (complete post object)
votes: int (count of votes)
```

---

### Vote Schema
**Request (Vote):**
```
post_id: int (required)
dir: int (required, must be ≤ 1)
```

---

### Token Schema
**Response (Token):**
```
access_token: str (JWT token)
token_type: str (always "bearer")
```

---

### TokenData Schema
**Internal Use:**
```
id: Optional[int] = None
```

---

## Response Status Codes

| Status Code | Meaning | Usage |
|-------------|---------|-------|
| 200 | OK | Successful GET request |
| 201 | CREATED | Successful resource creation (POST) |
| 202 | ACCEPTED | Successful update (PUT) |
| 204 | NO CONTENT | Successful deletion (DELETE) |
| 400 | BAD REQUEST | Invalid request data |
| 403 | FORBIDDEN | Unauthorized action (not owner) |
| 404 | NOT FOUND | Resource doesn't exist |
| 409 | CONFLICT | Duplicate vote attempt |

---

## Complete Request/Response Examples

### Example 1: Create User and Login

**Step 1: Register New User**
```
POST /users
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "created_at": "2026-02-11T12:00:00Z"
}
```

**Step 2: Login**
```
POST /login
Content-Type: application/x-www-form-urlencoded

username=john@example.com&password=securepass123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Example 2: Create and Vote on Post

**Step 1: Create Post**
```
POST /posts
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "FastAPI Tutorial",
  "content": "Learn how to build APIs with FastAPI",
  "published": true
}
```

**Response:**
```json
{
  "id": 10,
  "title": "FastAPI Tutorial",
  "content": "Learn how to build APIs with FastAPI",
  "published": true,
  "created_at": "2026-02-11T12:15:00Z",
  "owner_id": 1,
  "owner": {
    "id": 1,
    "email": "john@example.com",
    "created_at": "2026-02-11T12:00:00Z"
  }
}
```

**Step 2: Get Posts with Vote Count**
```
GET /posts?limit=10&skip=0&search=FastAPI
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "Post": {
      "id": 10,
      "title": "FastAPI Tutorial",
      "content": "Learn how to build APIs with FastAPI",
      "published": true,
      "created_at": "2026-02-11T12:15:00Z",
      "owner_id": 1,
      "owner": {
        "id": 1,
        "email": "john@example.com",
        "created_at": "2026-02-11T12:00:00Z"
      }
    },
    "votes": 0
  }
]
```

**Step 3: Vote on Post**
```
POST /vote
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "post_id": 10,
  "dir": 1
}
```

**Response:**
```json
{
  "message": "Vote added successfully"
}
```

**Step 4: Get Post Again (Vote Count Updated)**
```
GET /posts/10
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "Post": {
    "id": 10,
    "title": "FastAPI Tutorial",
    "content": "Learn how to build APIs with FastAPI",
    "published": true,
    "created_at": "2026-02-11T12:15:00Z",
    "owner_id": 1,
    "owner": {
      "id": 1,
      "email": "john@example.com",
      "created_at": "2026-02-11T12:00:00Z"
    }
  },
  "votes": 1
}
```

---

## Authentication Flow Diagram

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ 1. POST /login (email, password)
       ↓
┌─────────────────────────────────┐
│   Verify User Credentials       │
│ - Check if user exists          │
│ - Verify password hash          │
└──────────────────┬──────────────┘
                   │
                   ├─ Valid → Generate JWT Token
                   │
                   └─ Invalid → Return 404 Error
       │
       ↓
┌──────────────────────────────────┐
│   Return Token to Client         │
│ {                                │
│   "access_token": "...",         │
│   "token_type": "bearer"         │
│ }                                │
└──────────────────┬───────────────┘
       │
       │ 2. Use Token in Subsequent Requests
       │    Authorization: Bearer <token>
       ↓
┌────────────────────────────────┐
│   Extract User from Token      │
│   (Validate & Decode JWT)      │
└────────────────┬───────────────┘
                 │
                 ├─ Valid Token → Proceed with request
                 │
                 └─ Invalid Token → Return 401 Unauthorized
                 │
                 ↓
         ┌─────────────┐
         │   Execute   │
         │   Endpoint  │
         └─────────────┘
```

---

## Key Features

✅ **User Authentication**: Secure login with JWT tokens  
✅ **Post Management**: Create, read, update, delete posts  
✅ **Vote System**: Users can upvote/downvote posts  
✅ **Authorization**: Posts can only be deleted/updated by owner  
✅ **Search & Pagination**: Filter posts by title and paginate results  
✅ **Vote Counting**: Track total votes per post  
✅ **Password Hashing**: Passwords are securely hashed with bcrypt  

---

**Last Updated:** February 11, 2026
