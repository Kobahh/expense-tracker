# Expense Tracker

A full-stack personal expense tracker built with Flask and SQLite. Users can register, log in, and manage their own expenses through a secured, session-based interface with a live summary dashboard.

**Live app:** https://expense-tracker-4pla.onrender.com
> Hosted on Render's free tier — the app may take 30–60 seconds to wake up on first load after a period of inactivity.

## Features

- **User authentication** — registration and login with hashed passwords (`werkzeug.security`), session-based auth, and logout
- **Full CRUD on expenses** — create, read, update, and delete, each scoped to the logged-in user
- **Ownership-enforced access** — every read/write query checks both the target row's ID and the session's `user_id`, so one user can never view or modify another user's data
- **Summary dashboard** — total spend and a per-category breakdown, computed with SQL aggregation (`SUM`, `GROUP BY`)
- **Server-side input validation** — rejects invalid amounts (non-numeric, zero, or negative) and empty required fields, independent of any client-side restrictions
- **Styled UI** — a shared external stylesheet applied consistently across all pages

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite (via the standard library `sqlite3` module)
- **Auth:** Flask sessions, `werkzeug.security` for password hashing
- **Frontend:** Jinja2 templates, vanilla CSS
- **Deployment:** Render (Gunicorn as the WSGI server)

## Project Structure

```
expense_tracker/
├── app.py              # Routes and application logic
├── database.py         # Database initialization (init_db)
├── schema.sql           # Table definitions (users, expenses)
├── requirements.txt
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── edit_expense.html
└── static/
    └── style.css
```

## Database Schema

**users**
| Column   | Type    | Notes                |
|----------|---------|-----------------------|
| id       | INTEGER | Primary key           |
| username | TEXT    | Unique, not null       |
| password | TEXT    | Hashed, not null       |

**expenses**
| Column      | Type    | Notes                          |
|-------------|---------|----------------------------------|
| id          | INTEGER | Primary key                     |
| user_id     | INTEGER | Foreign key → users(id)         |
| amount      | REAL    | Not null                        |
| category    | TEXT    | Not null                        |
| description | TEXT    | Not null                        |
| date        | TEXT    | Not null                        |

## Running Locally

```bash
# Clone the repo
git clone https://github.com/Kobahh/expense-tracker.git
cd expense-tracker

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python3 app.py
```

Visit `http://127.0.0.1:5000` in your browser. The database is created automatically on first run.

## Notes on the Deployment

This app is deployed with SQLite on Render's free tier, which uses an ephemeral filesystem — the database resets on every service restart or redeploy. This is a deliberate trade-off for a free-tier demo; a production deployment of this app would use a persistent database such as PostgreSQL instead.

## What I Learned

This project was built end-to-end as a way to learn full-stack web development fundamentals, including:
- Flask routing, request handling, and Jinja templating
- Relational schema design with foreign keys
- Password hashing and why it differs from encryption
- Session-based authentication
- Writing and reasoning about parameterized SQL queries (and why they matter for security)
- SQL aggregation (`SUM`, `GROUP BY`)
- Server-side vs. client-side validation
- Git/GitHub workflow and deploying a Flask app to production with Gunicorn
