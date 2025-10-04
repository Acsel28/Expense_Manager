ExesMan API - FastAPI Backend
Setup Instructions
1. Install Dependencies
```bash cd api pip install -r requirements.txt ```

2. Configure Environment Variables
Copy the example environment file and update with your PostgreSQL credentials:

```bash cp .env.example .env ```

Edit .env and set your database connection string: ``` DATABASE_URL=postgresql://your_username:your_password@localhost:5432/exesman SECRET_KEY=generate-a-secure-random-key-here ```

3. Create Database
Create a PostgreSQL database named exesman:

```bash createdb exesman ```

Or using psql: ```sql CREATE DATABASE exesman; ```

4. Run Database Migrations
After we set up Alembic migrations, you'll run:

```bash alembic upgrade head ```

5. Start the Development Server
```bash python main.py ```

Or using uvicorn directly: ```bash uvicorn main:app --reload --host 0.0.0.0 --port 8000 ```

The API will be available at:

API: http://localhost:8000
Interactive API docs: http://localhost:8000/docs
Alternative API docs: http://localhost:8000/redoc
Project Structure
``` api/ ├── main.py # FastAPI application entry point ├── config.py # Configuration and settings ├── database.py # Database connection and session ├── requirements.txt # Python dependencies ├── .env # Environment variables (create from .env.example) ├── models/ # SQLAlchemy models (coming next) ├── schemas/ # Pydantic schemas (coming next) ├── routers/ # API route handlers (coming next) ├── services/ # Business logic (coming next) └── alembic/ # Database migrations (coming next) ```

Next Steps
Create database models (Company, User, Expense)
Set up authentication with JWT
Build API endpoints
Configure Alembic for migrations
