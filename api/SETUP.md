# ExesMan Backend Setup Guide

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Step-by-Step Setup

### 1. Install Dependencies

\`\`\`bash
cd api
pip install -r requirements.txt
\`\`\`

### 2. Create PostgreSQL Database

Using `createdb` command:
\`\`\`bash
createdb exesman
\`\`\`

Or using `psql`:
\`\`\`bash
psql -U postgres
CREATE DATABASE exesman;
\q
\`\`\`

### 3. Configure Environment Variables

Copy the example environment file:
\`\`\`bash
cp .env.example .env
\`\`\`

Edit `.env` and update with your settings:
\`\`\`env
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/exesman
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
\`\`\`

**Important:** Generate a secure SECRET_KEY using:
\`\`\`bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
\`\`\`

### 4. Initialize Database

Run the initialization script to create tables and seed data:
\`\`\`bash
python scripts/init_db.py
\`\`\`

This will create:
- All database tables (companies, users, expenses)
- Sample company: "Acme Corporation"
- Test users with different roles
- Sample expenses for testing

### 5. Start the API Server

Using the main script:
\`\`\`bash
python main.py
\`\`\`

Or using uvicorn directly:
\`\`\`bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

The API will be available at:
- **API Base URL:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

## Test Accounts

After running the initialization script, you can login with:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@acme.com | admin123 |
| Manager | manager@acme.com | manager123 |
| Employee | alice@acme.com | alice123 |
| Employee | bob@acme.com | bob123 |

## Using Alembic Migrations (Alternative to init_db.py)

If you prefer to use Alembic for migrations:

### Initialize Alembic (already done)
\`\`\`bash
alembic init alembic
\`\`\`

### Create Initial Migration
\`\`\`bash
alembic revision --autogenerate -m "Initial migration"
\`\`\`

### Apply Migrations
\`\`\`bash
alembic upgrade head
\`\`\`

### Create New Migration (after model changes)
\`\`\`bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
\`\`\`

## API Endpoints Overview

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Companies
- `GET /api/v1/companies` - List companies
- `POST /api/v1/companies` - Create company (Admin only)
- `GET /api/v1/companies/{id}` - Get company details
- `PUT /api/v1/companies/{id}` - Update company (Admin only)
- `DELETE /api/v1/companies/{id}` - Delete company (Admin only)

### Users
- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/users` - List users (role-based access)
- `GET /api/v1/users/{id}` - Get user details
- `GET /api/v1/users/subordinates/list` - Get subordinates (Managers)
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user (Admin only)

### Expenses
- `GET /api/v1/expenses` - List expenses (with filters)
- `POST /api/v1/expenses` - Create expense
- `GET /api/v1/expenses/pending` - List pending approvals (Managers)
- `GET /api/v1/expenses/stats` - Get expense statistics
- `GET /api/v1/expenses/{id}` - Get expense details
- `PUT /api/v1/expenses/{id}` - Update expense
- `PATCH /api/v1/expenses/{id}/status` - Approve/reject expense (Managers)
- `DELETE /api/v1/expenses/{id}` - Delete expense

## Testing the API

### 1. Login to get access token
\`\`\`bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@acme.com&password=admin123"
\`\`\`

### 2. Use the token in subsequent requests
\`\`\`bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
\`\`\`

### 3. Or use the interactive docs
Visit http://localhost:8000/docs and use the "Authorize" button to login.

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running: `pg_isready`
- Check DATABASE_URL in `.env` file
- Ensure database exists: `psql -l | grep exesman`

### Import Errors
- Ensure you're in the `api` directory
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Migration Issues
- Drop and recreate database if needed
- Run `python scripts/init_db.py` again

## Next Steps

1. Test all API endpoints using the interactive docs
2. Integrate with the React frontend
3. Add file upload for receipts (using Vercel Blob or similar)
4. Implement email notifications for expense approvals
5. Add more comprehensive error handling and logging
