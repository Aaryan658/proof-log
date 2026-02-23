# ProofLog

ProofLog is a simple web application that allows users to create projects and log their daily work sessions with optional proof files.

## Privacy & Access Control
- **Private by Default**: All projects and logs are private to the user who created them.
- **Authentication Required**: Users must register and login to access the system.
- **Mentorship Verification**: Mentors can view all intern logs and explicitly approve or revoke them. Only approved logs count towards an intern's total project hours.

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
   - To register as an **Intern**, your email must end with `@intern.com` (e.g., `student@intern.com`).
   - To register as a **Mentor**, your email must end with `@mentor.com` (e.g., `faculty@mentor.com`).
2. **Login** to access your dashboard.
3. **Interns**: Create Projects, log daily work, and optionally upload proof screenshots.
4. **Mentors**: View all assigned intern projects, and click "Approve Log" to verify intern hours. Total hours are only calculated based on explicitly approved logs!
