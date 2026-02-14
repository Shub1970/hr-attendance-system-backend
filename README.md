# HR Attendance Backend

FastAPI backend connected to Supabase for managing employee records and attendance logs.

## Tech Stack

- Language: Python 3
- API framework: FastAPI
- Validation and schemas: Pydantic v2
- ASGI server: Uvicorn
- Database platform: Supabase (PostgreSQL)
- Database access: `supabase-py` / PostgREST client
- Environment management: `python-dotenv`

## Project Structure

- `main.py` - FastAPI app entrypoint and router registration
- `backend/config.py` - environment loading and validation
- `backend/supabase_client.py` - shared Supabase client
- `models/` - Pydantic request and response schemas
- `controls/` - business logic and Supabase table operations
- `routers/` - API route definitions
- `seeds/` - scripts to seed employees and attendance data

## Environment

Create a `.env` file in the backend root with:

- `SUPABASE_URL`
- `SUPABASE_KEY`

## Installation and Run

Install dependencies:

```bash
pip install -r requirement.txt
```

Run the API locally:

```bash
uvicorn main:app --reload
```

Open API docs:

- `http://127.0.0.1:8000/docs`

## Seed Data

Seed employees:

```bash
python -m seeds.employees_seed
```

This script uses upsert on `employee_id`, so reruns do not create duplicate employee rows.

Seed attendance:

```bash
python -m seeds.attendance_seed
```

This script seeds the last 7 days for all employees and uses upsert on `(employee_id, attendance_date)`, so reruns do not create duplicate attendance rows.

## API Endpoints

Health:

- `GET /health`

Employees:

- `POST /employees`
- `GET /employees`
- `GET /employees/{employee_id}`
- `PUT /employees/{employee_id}`
- `DELETE /employees/{employee_id}`

Attendance:

- `POST /attendance`
- `GET /attendance`
- `GET /attendance/{attendance_id}`
- `PUT /attendance/{attendance_id}`
- `DELETE /attendance/{attendance_id}`

Optional filters for `GET /attendance`:

- `employee_id` (UUID)
- `attendance_date` (YYYY-MM-DD)
- `status` (`present` or `absent`)
