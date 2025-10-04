# ExesMan - Expense Management System

Complete setup guide for running the ExesMan application locally.

## Project Structure

\`\`\`
exesman/
├── api/                    # FastAPI Backend
│   ├── models/            # SQLAlchemy database models
│   ├── schemas/           # Pydantic validation schemas
│   ├── routers/           # API route handlers
│   ├── utils/             # Authentication utilities
│   ├── alembic/           # Database migrations
│   ├── main.py            # FastAPI application entry
│   ├── config.py          # Configuration settings
│   └── database.py        # Database connection
├── app/                   # Next.js Frontend
│   ├── dashboard/         # Dashboard page
│   ├── expenses/          # Expenses management
│   ├── approvals/         # Manager approvals
│   ├── admin/             # Admin settings
│   ├── login/             # Login page
│   └── signup/            # Signup page
├── components/            # React components
│   ├── layout/            # Layout components
│   └── ui/                # Shadcn UI components
├── lib/                   # Utilities
│   ├── api.ts             # Axios API client
│   └── types.ts           # TypeScript types
└── store/                 # Zustand state management
    └── auth-store.ts      # Authentication store
\`\`\`

## Backend Setup

### 1. Prerequisites

- Python 3.9+
- PostgreSQL 12+

### 2. Install Dependencies

\`\`\`bash
cd api
pip install -r requirements.txt
\`\`\`

### 3. Configure Environment

Create a `.env` file in the `api/` directory:

\`\`\`env
DATABASE_URL=postgresql://username:password@localhost:5432/exesman
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
\`\`\`

Replace `username`, `password`, and `your-secret-key-here-change-in-production` with your actual values.

### 4. Initialize Database

Run the initialization script to create tables and seed test data:

\`\`\`bash
cd ..
python scripts/init_db.py
\`\`\`

This will create:
- 2 companies (Acme Corp, TechStart Inc)
- 6 users with different roles
- 15 sample expenses

**Test Accounts:**
- Admin: `admin@acme.com` / `admin123`
- Manager: `manager@acme.com` / `manager123`
- Employee: `employee@acme.com` / `employee123`

### 5. Start Backend Server

\`\`\`bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Frontend Setup

### 1. Prerequisites

- Node.js 18+
- npm or yarn

### 2. Install Dependencies

\`\`\`bash
npm install
\`\`\`

### 3. Configure Environment

The frontend uses the `NEXT_PUBLIC_API_URL` environment variable which should already be configured in your v0 project settings.

If running locally outside of v0, create a `.env.local` file:

\`\`\`env
NEXT_PUBLIC_API_URL=http://localhost:8000
\`\`\`

### 4. Start Frontend Server

\`\`\`bash
npm run dev
\`\`\`

The application will be available at `http://localhost:3000`

## Features

### Authentication
- JWT-based authentication
- Role-based access control (Admin, Manager, Employee)
- Secure password hashing with bcrypt
- Persistent login with Zustand + localStorage

### Dashboard
- Real-time statistics
- Expense category breakdown chart
- Recent activity feed
- Role-specific views

### Expense Management
- Create, view, edit, and delete expenses
- Advanced data table with sorting, filtering, and pagination
- Status tracking (Pending, Approved, Rejected)
- Receipt upload support

### Approval Workflow
- Manager approval interface
- Approve/reject actions with loading states
- Hierarchical approval system
- Email notifications (coming soon)

### Admin Settings
- User management (create, view, delete)
- Company settings configuration
- Role assignment
- Currency settings

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/register` - Admin register user

### Companies
- `GET /companies` - List companies
- `POST /companies` - Create company (Admin)
- `PUT /companies/{id}` - Update company (Admin)
- `DELETE /companies/{id}` - Delete company (Admin)

### Users
- `GET /users` - List users (filtered by role)
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user (Admin)

### Expenses
- `GET /expenses` - List expenses (filtered by role)
- `POST /expenses` - Create expense
- `GET /expenses/{id}` - Get expense details
- `PUT /expenses/{id}` - Update expense
- `DELETE /expenses/{id}` - Delete expense
- `PATCH /expenses/{id}/approve` - Approve expense (Manager/Admin)
- `PATCH /expenses/{id}/reject` - Reject expense (Manager/Admin)
- `GET /expenses/stats` - Get dashboard statistics

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **Alembic** - Database migrations

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Shadcn/ui** - Beautiful UI components
- **TanStack Table** - Advanced data tables
- **Recharts** - Data visualization
- **Zustand** - State management
- **Axios** - HTTP client
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **Framer Motion** - Animations

## Troubleshooting

### Backend Issues

**Database connection error:**
- Verify PostgreSQL is running
- Check DATABASE_URL in .env file
- Ensure database exists: `createdb exesman`

**Import errors:**
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.9+)

### Frontend Issues

**API connection error:**
- Verify backend is running on port 8000
- Check NEXT_PUBLIC_API_URL environment variable
- Check browser console for CORS errors

**Build errors:**
- Clear Next.js cache: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules && npm install`

## Next Steps

1. **Email Notifications** - Add email alerts for expense approvals
2. **File Upload** - Implement receipt image upload to cloud storage
3. **Reports** - Generate expense reports and analytics
4. **Mobile App** - Build React Native mobile application
5. **Multi-currency** - Support multiple currencies with conversion
6. **Audit Log** - Track all user actions for compliance

## Support

For issues or questions, please check:
- API Documentation: `http://localhost:8000/docs`
- Backend logs in terminal
- Frontend console in browser DevTools
