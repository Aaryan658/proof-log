# ProofLog

ProofLog is a simple web application that allows users to create projects and log their daily work sessions with optional proof files.

## Privacy & Access Control
- **Private by Default**: All projects and logs are private to the user who created them.
- **Authentication Required**: Users must register and login to access the system.
- **Validation**: This is an MVP academic project. Logs are **self-reported** and not currently validated by external reviewers (mentors/teachers). Validated reviewer roles are a planned future extension.

## Tech Stack
- **Backend**: Flask (SQLAlchemy, WTForms)
- **Frontend**: Plain HTML/CSS (Jinja2 Templates)
- **Database**: SQLite

## Setup & Run
   ```bash
   pip install -r requirements.txt
   ```
2. Run:
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000/`.

## How to use
1. **Register** a new account.
2. **Login** to access your private dashboard.
3. **Create Projects** (Visible only to you).
4. **Log Work** inside a project.
