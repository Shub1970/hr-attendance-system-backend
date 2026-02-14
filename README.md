# HR Attendance Backend

FastAPI backend connected to Supabase for managing `employees` and `attendance`.

## Project Structure

- `main.py` - FastAPI app entrypoint, imports all routers
- `backend/config.py` - environment loading and validation
- `backend/supabase_client.py` - shared Supabase client
- `models/` - Pydantic request/response schemas
- `routers/` - API routes

## Environment

Required values in `.env`:

- `SUPABASE_URL`
- `SUPABASE_KEY`

## Run

```bash
uvicorn main:app --reload
```

Swagger docs:

- `http://127.0.0.1:8000/docs`

## Seed Employees

Run the employee seed script:

```bash
python -m seeds.employees_seed
```

This uses upsert on `employee_id`, so running it multiple times will not create duplicate employee rows.

## Seed Attendance

Run the attendance seed script:

```bash
python -m seeds.attendance_seed
```

This seeds the last 7 days for all employees and uses upsert on `(employee_id, attendance_date)`, so reruns do not create duplicate attendance rows.

## API Endpoints

### Health

- `GET /health`

### Employees

- `POST /employees`
- `GET /employees`
- `GET /employees/{employee_id}`
- `PUT /employees/{employee_id}`
- `DELETE /employees/{employee_id}`

Example request:

```json
{
  "employee_id": "EMP-1001",
  "full_name": "John Doe",
  "email": "john@example.com",
  "department": "Engineering"
}
```

### Attendance

- `POST /attendance`
- `GET /attendance`
- `GET /attendance/{attendance_id}`
- `PUT /attendance/{attendance_id}`
- `DELETE /attendance/{attendance_id}`

Optional filters on list attendance:

- `employee_id` (UUID)
- `attendance_date` (YYYY-MM-DD)
- `status` (`present` or `absent`)

Example request:

```json
{
  "employee_id": "00000000-0000-0000-0000-000000000000",
  "attendance_date": "2026-02-14",
  "status": "present"
}
```
