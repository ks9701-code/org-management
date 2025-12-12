Organization Management Service

A multi-tenant backend service built with FastAPI and MongoDB, designed to support dynamic organization management where each organization gets its own MongoDB collection.

This project demonstrates a scalable, secure, and production-ready multi-tenant architecture using modern backend best practices.

🌐 Live Demo

Swagger UI: https://org-management.onrender.com/docs

ReDoc: https://org-management.onrender.com/redoc

⚠️ Render Free Tier Notice
This service is hosted on Render’s free plan, which spins down after inactivity.
The first request may take 30–60 seconds due to cold start. Subsequent requests are fast.

🚀 Features

🧱 Multi-Tenant Architecture (one MongoDB collection per organization)

🔐 JWT Authentication for admin users

🔑 Bcrypt Password Hashing

⚙️ Dynamic Collection Creation

🔄 Automatic Data Migration on Organization Rename

📄 Swagger & ReDoc API Documentation

🧪 Pytest-based Test Coverage

☁️ Cloud-deployed on Render

🏗️ Architecture Overview
Client (Postman / Frontend)
        │
        ▼
FastAPI Application
│
├── API Routes
│   ├── /org/create
│   ├── /org/get
│   ├── /org/update
│   ├── /org/delete
│   └── /admin/login
│
├── Services Layer
│   ├── OrganizationService
│   └── AuthService
│
└── Core Utilities
    ├── JWT & Bcrypt Security
    └── MongoDB Connection
        │
        ▼
MongoDB Atlas (Master Database)
│
├── organizations
├── admin_users
├── org_acme_corp
├── org_test_inc
└── org_* (one per organization)

📌 API Workflow
1️⃣ Create Organization

Endpoint: POST /org/create
Authentication: ❌ Not required

{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "securepassword123"
}

2️⃣ Admin Login (Get JWT Token)

Endpoint: POST /admin/login
Authentication: ❌ Not required

{
  "email": "admin@acme.com",
  "password": "securepassword123"
}


📌 Save the returned access_token for protected endpoints.

3️⃣ Update Organization

Endpoint: PUT /org/update
Authentication: ✅ Required

Authorization: Bearer <access_token>

{
  "organization_name": "Acme Corp",
  "email": "newadmin@acme.com",
  "password": "newpassword123",
  "new_organization_name": "Updated Corp Name"
}

4️⃣ Delete Organization

Endpoint: DELETE /org/delete
Authentication: ✅ Required

DELETE /org/delete?organization_name=Acme Corp
Authorization: Bearer <access_token>

5️⃣ Get Organization (Optional)

Endpoint: GET /org/get
Authentication: ❌ Not required

GET /org/get?organization_name=Acme Corp

🧠 Design Decisions & Trade-offs
Dynamic Collections (Chosen Approach)

Pros

Strong data isolation

Simple deletion (drop collection)

Faster queries (no org_id filtering)

Schema flexibility

Compliance-friendly

Cons

MongoDB collection limits

Index management per collection

Harder cross-org queries

Backup complexity

Alternatives Considered

Shared collections with organization_id

Database-per-organization

Sharding by organization

📌 Chosen for this assignment:
Dynamic collections provide clarity, simplicity, and strong isolation.

🔒 Security Considerations

Passwords hashed with bcrypt

JWT tokens with expiration

Admin-only protected routes

Pydantic input validation

Production Recommendations

HTTPS only

Rate limiting

Refresh tokens

Request logging

Environment-specific secrets

MongoDB role-based access

🛠️ Local Setup
Prerequisites

Python 3.10+

MongoDB Atlas (M0 free tier)

Git

Installation
git clone https://github.com/ks9701-code/org-management.git
cd org-management-service
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

Environment Variables

Create .env from template:

cp .env.example .env

APP_NAME=Org Management Service
JWT_SECRET=your-secure-random-key
JWT_ALGO=HS256
JWT_EXPIRE_MINUTES=1440
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MASTER_DB=master_db

Run Locally
uvicorn app.main:app --reload --port 8000


Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

🧪 Testing
pytest tests/

📦 Project Structure
org-management-service/
├── app/
│   ├── core/        # Config, DB, Security
│   ├── models/      # MongoDB models
│   ├── schemas/     # Pydantic schemas
│   ├── services/    # Business logic
│   ├── api/         # Routes & dependencies
│   └── utils/       # Helpers
├── tests/
├── .env.example
├── requirements.txt
├── Procfile
└── README.md

☁️ Deployment (Render)

Free tier deployment

Auto-deploy from GitHub

Cold start expected after inactivity

Live API:
https://org-management.onrender.com/docs

📝 License

This project is created for educational and assignment purposes.

🤝 Contributing

This is an assignment project, but feel free to fork and extend.

📧 Support

For issues or questions, please open a GitHub issue.

⭐ Built with FastAPI & MongoDB
