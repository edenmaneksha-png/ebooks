# eBooks — Django Backend

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py create_default_admin   # creates eden / eden123
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/auth/register/ | Create account |
| POST | /api/auth/login/    | Get token |
| POST | /api/auth/logout/   | Revoke token |
| GET  | /api/auth/me/       | Current user |
| GET  | /api/books/         | List books (search, category, sort) |
| POST | /api/books/         | Add book (admin, multipart with pdf_file) |
| GET  | /api/books/{id}/    | Book detail + pdf_url |
| DELETE | /api/books/{id}/  | Delete book (admin) |
| POST | /api/books/seed/    | Seed 12 demo books (admin) |
| DELETE | /api/books/wipe/  | Delete all books (admin) |
| GET/POST | /api/progress/  | Reading progress (auth required) |

## Database

SQLite file at `db.sqlite3` (auto-created on first migrate).  
PDF files stored in `media/pdfs/`.

## Django Admin

http://127.0.0.1:8000/admin/  →  eden / eden123

## Production notes

- Set `SECRET_KEY` and `DEBUG=False` in settings  
- Add CORS headers if frontend is on a different origin  
- Consider Postgres for multi-user production use
