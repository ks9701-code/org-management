# Organization Management Service

A multi-tenant backend service built with FastAPI and MongoDB that supports dynamic organization management with separate MongoDB collections per organization.

## 🏗️ Architecture Overview

```
┌─────────────┐
│   Client    │
│  (Postman/  │
│   Frontend) │
└──────┬──────┘
       │ HTTP/REST
       │
┌──────▼─────────────────────────────────────┐
│         FastAPI Application                │
│  ┌──────────────────────────────────────┐ │
│  │  API Routes                          │ │
│  │  - /org/create                       │ │
│  │  - /org/get                          │ │
│  │  - /org/update                       │ │
│  │  - /org/delete                       │ │
│  │  - /admin/login                      │ │
│  └──────────┬───────────────────────────┘ │
│             │                             │
│  ┌──────────▼───────────────────────────┐ │
│  │  Services Layer                      │ │
│  │  - OrganizationService               │ │
│  │  - AuthService                       │ │
│  └──────────┬───────────────────────────┘ │
│             │                             │
│  ┌──────────▼───────────────────────────┐ │
│  │  Core Utilities                      │ │
│  │  - Security (JWT, bcrypt)           │ │
│  │  - Database Connection               │ │
│  └──────────┬───────────────────────────┘ │
└─────────────┼─────────────────────────────┘
              │
              │ MongoDB Connection
              │
┌─────────────▼─────────────────────────────┐
│      MongoDB Atlas (Master Database)       │
│  ┌──────────────────────────────────────┐ │
│  │  Collections:                        │ │
│  │  - organizations (metadata)          │ │
│  │  - admin_users (credentials)          │ │
│  │  - org_acme_corp (dynamic)           │ │
│  │  - org_test_inc (dynamic)            │ │
│  │  - org_* (one per organization)      │ │
│  └──────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

## 🚀 Features

- **Multi-tenant Architecture**: Each organization gets its own MongoDB collection
- **JWT Authentication**: Secure token-based authentication for admin users
- **Password Security**: Bcrypt hashing for password storage
- **Dynamic Collection Creation**: Collections created automatically on organization creation
- **RESTful API**: Clean REST endpoints for all operations
- **Data Migration**: Automatic data migration when organization names change

## 📋 Prerequisites

- Python 3.10 or higher
- MongoDB Atlas account (free tier M0 cluster)
- Git

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd org-management-service
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
APP_NAME=Org Management Service
JWT_SECRET=your-secret-key-change-this-in-production-min-32-chars
JWT_ALGO=HS256
JWT_EXPIRE_MINUTES=1440

MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MASTER_DB=master_db
```

**Getting MongoDB Atlas URI:**
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free M0 cluster
3. Create a database user
4. Add your IP to network access (or use `0.0.0.0/0` for development)
5. Click "Connect" → "Connect your application"
6. Copy the connection string and replace `<password>` with your password

### 5. Run the Application

**Development mode (with auto-reload):**
```bash
uvicorn app.main:app --reload --port 8000
```

**Production mode:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### 6. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### 1. Create Organization
```http
POST /org/create
Content-Type: application/json

{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "organization_name": "Acme Corp",
  "collection_name": "org_acme_corp",
  "admin_email": "admin@acme.com",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 2. Get Organization
```http
GET /org/get?organization_name=Acme Corp
```

### 3. Update Organization
```http
PUT /org/update
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "organization_name": "Acme Corp",
  "email": "newadmin@acme.com",
  "password": "newpassword123"
}
```

### 4. Delete Organization
```http
DELETE /org/delete
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "organization_name": "Acme Corp"
}
```

### 5. Admin Login
```http
POST /admin/login
Content-Type: application/json

{
  "email": "admin@acme.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "admin_id": "507f1f77bcf86cd799439011",
  "organization_id": "507f191e810c19729de860ea",
  "organization_name": "Acme Corp"
}
```

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/
```

## 📦 Project Structure

```
org-management-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration settings
│   │   ├── database.py          # MongoDB connection
│   │   └── security.py          # JWT & password hashing
│   ├── models/
│   │   ├── __init__.py
│   │   └── master.py            # MongoDB document models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── org.py               # Organization Pydantic schemas
│   │   └── auth.py              # Authentication schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── org_service.py       # Organization business logic
│   │   └── auth_service.py      # Authentication logic
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py              # Dependencies (auth)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── org.py           # Organization endpoints
│   │       └── admin.py         # Admin endpoints
│   └── utils/
│       ├── __init__.py
│       └── naming.py            # Collection naming utility
├── tests/
│   ├── __init__.py
│   └── test_org.py             # Test cases
├── .env.example                # Environment variables template
├── .gitignore
├── Procfile                    # For deployment
├── requirements.txt            # Python dependencies
└── README.md
```

## 🚀 Deployment to Render (Free Hosting)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [Render](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `org-management-service` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `MONGO_URI`: Your MongoDB Atlas connection string
   - `JWT_SECRET`: A secure random string (min 32 characters)
   - `JWT_ALGO`: `HS256`
   - `JWT_EXPIRE_MINUTES`: `1440`
   - `MASTER_DB`: `master_db`
   - `APP_NAME`: `Org Management Service`
6. Click "Create Web Service"
7. Wait for deployment (usually 2-5 minutes)

Your API will be available at: `https://your-service-name.onrender.com`

### Step 3: Update MongoDB Atlas Network Access

Add Render's IP ranges or use `0.0.0.0/0` (with strong password) in MongoDB Atlas Network Access settings.

## 🎯 Design Decisions & Trade-offs

### Architecture Scalability Analysis

#### ✅ Pros of Current Design (Dynamic Collections)

1. **Data Isolation**: Each organization's data is completely isolated
2. **Easy Deletion**: Dropping a collection is straightforward
3. **Performance**: No need to filter by `organization_id` in queries
4. **Schema Flexibility**: Each organization can have different schemas
5. **Compliance**: Easier to meet data residency requirements

#### ❌ Cons of Current Design

1. **Collection Limit**: MongoDB has a limit on number of collections (varies by version)
2. **Management Overhead**: More collections to manage and monitor
3. **Cross-org Queries**: Difficult to query across organizations
4. **Index Management**: Need to create indexes per collection
5. **Backup Complexity**: More collections to backup

#### 🔄 Alternative Architectures

**1. Shared Collections with `organization_id`**
```
✅ Pros: Fewer collections, easier cross-org queries
❌ Cons: Need indexes on org_id, less isolation
```

**2. Database-per-Organization**
```
✅ Pros: Maximum isolation, separate connections
❌ Cons: More complex connection management, higher overhead
```

**3. Sharding by Organization**
```
✅ Pros: Scales horizontally, good for large orgs
❌ Cons: Complex setup, overkill for small apps
```

### Recommended Approach

For this assignment, **dynamic collections** are appropriate because:
- Simple to implement
- Clear data isolation
- Easy to demonstrate multi-tenancy
- Suitable for small to medium scale

For production at scale, consider:
- **Hybrid approach**: Shared collections with `organization_id` for small orgs, dedicated collections for large orgs
- **Sharding**: When you have thousands of organizations
- **Database-per-org**: For enterprise customers with strict compliance needs

## 🔒 Security Considerations

- ✅ Passwords hashed with bcrypt
- ✅ JWT tokens with expiration
- ✅ Admin authentication required for update/delete
- ✅ Input validation with Pydantic
- ⚠️ **Production Recommendations**:
  - Use HTTPS only
  - Implement rate limiting
  - Add request logging
  - Use environment-specific secrets
  - Enable MongoDB authentication
  - Implement refresh tokens

## 📝 License

This project is created for educational/assignment purposes.

## 🤝 Contributing

This is an assignment project. Feel free to fork and extend!

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI and MongoDB**

