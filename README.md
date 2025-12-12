Organization Management Service

A multi-tenant backend service built with FastAPI and MongoDB, designed to support dynamic organization management where each organization gets its own MongoDB collection.
This project demonstrates a scalable and secure approach to multi-tenancy with clean architecture and RESTful APIs.

🌐 Live API

🔗 Swagger UI (Live API Docs):
https://org-management.onrender.com/docs

✅ The API is fully deployed and ready to use.
You can test all endpoints directly from Swagger UI.

⚠️ Note on Hosting (Render Free Tier):
This service is hosted on Render’s free plan, which spins down after inactivity.
The first request may take ~30–60 seconds to start the server (cold start).
Subsequent requests will be fast once the service is active.

🏗️ Architecture Overview
┌─────────────┐
│   Client    │
│ (Postman /  │
│ Frontend)   │
└──────┬──────┘
       │ HTTP / REST
       ▼
┌──────────────────────────────────────────┐
│          FastAPI Application              │
│ ┌──────────────────────────────────────┐ │
│ │ API Routes                           │ │
│ │  - /org/create                       │ │
│ │  - /org/get                          │ │
│ │  - /org/update                       │ │
│ │  - /org/delete                       │ │
│ │  - /admin/login                      │ │
│ └──────────┬───────────────────────────┘ │
│            │                               │
│ ┌──────────▼───────────────────────────┐ │
│ │ Services Layer                       │ │
│ │  - OrganizationService              │ │
│ │  - AuthService                      │ │
│ └──────────┬───────────────────────────┘ │
│            │                               │
│ ┌──────────▼───────────────────────────┐ │
│ │ Core Utilities                       │ │
│ │  - JWT & Bcrypt Security             │ │
│ │  - Database Connection               │ │
│ └──────────┬───────────────────────────┘ │
└────────────┼─────────────────────────────┘
             │ MongoDB Connection
             ▼
┌──────────────────────────────────────────┐
│        MongoDB Atlas (Master DB)          │
│ ┌──────────────────────────────────────┐ │
│ │ Collections                           │ │
│ │  - organizations (metadata)           │ │
│ │  - admin_users (credentials)          │ │
│ │  - org_acme_corp (dynamic)            │ │
│ │  - org_test_inc (dynamic)             │ │
│ │  - org_* (one per organization)       │ │
│ └──────────────────────────────────────┘ │
└──────────────────────────────────────────┘

🚀 Quick Start – How to Execute
Step-by-Step Workflow
1️⃣ Create Organization

Endpoint: POST /org/create
Authentication: ❌ Not required

📎 Live Docs:
https://org-management.onrender.com/docs#/organizations/create_organization_org_create_post

Request

POST /org/create
Content-Type: application/json

{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "securepassword123"
}


Response

{
  "organization_name": "Acme Corp",
  "collection_name": "org_acme_corp",
  "admin_email": "admin@acme.com",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}


📌 Important:
Save the organization name and credentials — they are required for login.

2️⃣ Admin Login (Get JWT Token)

Endpoint: POST /admin/login
Authentication: ❌ Not required

📎 Live Docs:
https://org-management.onrender.com/docs#/admin/admin_login_admin_login_post

Request

{
  "email": "admin@acme.com",
  "password": "securepassword123"
}


Response

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "admin_id": "507f1f77bcf86cd799439011",
  "organization_id": "507f191e810c19729de860ea",
  "organization_name": "Acme Corp"
}


⚠️ Save the access_token — required for update & delete operations.

3️⃣ Update Organization

Endpoint: PUT /org/update
Authentication: ✅ Required (Bearer Token)

📎 Live Docs:
https://org-management.onrender.com/docs#/organizations/update_organization_org_update_put

Headers

Authorization: Bearer <your-access-token>


Request

{
  "organization_name": "Acme Corp",
  "email": "newadmin@acme.com",
  "password": "newpassword123",
  "new_organization_name": "Updated Corp Name"
}


📌 Important Notes

organization_name must match your current org

email must be new

password updates admin password

new_organization_name is optional

Response

{
  "organization_name": "Updated Corp Name",
  "collection_name": "org_updated_corp_name",
  "admin_email": "newadmin@acme.com",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:01"
}

4️⃣ Delete Organization

Endpoint: DELETE /org/delete
Authentication: ✅ Required

📎 Live Docs:
https://org-management.onrender.com/docs#/organizations/delete_organization_org_delete_delete

Request

DELETE /org/delete?organization_name=Acme Corp
Authorization: Bearer <your-access-token>


Response

{
  "message": "Organization 'Acme Corp' deleted successfully"
}


📌 You can only delete your own organization.

5️⃣ Get Organization (Optional)

Endpoint: GET /org/get
Authentication: ❌ Not required

Request

GET /org/get?organization_name=Acme Corp

🚀 Key Features

✅ Multi-tenant Architecture (one MongoDB collection per org)

🔐 JWT-based Authentication

🔑 Bcrypt Password Hashing

⚙️ Dynamic Collection Creation

🔄 Automatic Data Migration on Rename

🧱 Clean Service-based Architecture

📄 Swagger & ReDoc API Docs

🎯 Design Decisions & Trade-offs
Dynamic Collections (Current Approach)

Pros

Strong data isolation

Easy organization deletion

Better query performance

Flexible schemas

Compliance-friendly

Cons

MongoDB collection limits

Index management overhead

Hard cross-organization queries

Backup complexity

Alternative Approaches

Shared collections with organization_id

Database-per-organization

Sharding by organization

📌 Chosen for this assignment:
Dynamic collections → simple, clear, and effective for small-to-medium scale.

🔒 Security Considerations

✅ Bcrypt password hashing

✅ JWT authentication with expiry

✅ Protected update & delete routes

✅ Pydantic input validation

Production Enhancements Recommended

HTTPS only

Rate limiting

Refresh tokens

Request logging

IP whitelisting

MongoDB role-based access

🚀 Deployment (Render – Free Tier)

Hosted on Render

Auto-deploy from GitHub

Free tier used for demo/assignment

⚠️ Cold Start Notice

Render free services sleep after 15 minutes of inactivity
First request may take 30–60 seconds to respond

🔗 Live Docs:
https://org-management.onrender.com/docs

📦 Project Structure

(unchanged – same as your original)

📝 License

This project is created for educational and assignment purposes.

🤝 Contributing

Feel free to fork, explore, and extend this project.

📧 Support

For issues or questions, please open an issue on GitHub.

Built with ❤️ using FastAPI & MongoDB
