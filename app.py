import os
from datetime import datetime
from flask import Flask, request, session, redirect, render_template, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'media/proofs')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default='intern') # 'intern' or 'mentor'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Added ForeignKey
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('projects', lazy=True)) # Relationship

    @property
    def approved_hours(self):
        return sum(log.hours for log in self.logs if log.is_approved)
        
    @property
    def pending_hours(self):
        return sum(log.hours for log in self.logs if not log.is_approved)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    proof_path = db.Column(db.String(500)) # Optional file path
    is_approved = db.Column(db.Boolean, default=False, nullable=False) # Added for Mentor Approval
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', backref=db.backref('logs', lazy=True))

# --- Helpers ---
def current_user():
    if "user_id" in session:
        return db.session.get(User, session["user_id"])
    return None

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    if current_user():
        return redirect("/dashboard")
    error = None
    if request.method == "POST":
        u = User.query.filter_by(email=request.form["email"]).first()
        if not u:
            error = "User not found. Please register."
        elif not check_password_hash(u.password, request.form["password"]):
            error = "Incorrect password."
        else:
            session["user_id"] = u.id
            return redirect("/dashboard")
    return render_template("index.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user():
        return redirect("/dashboard")
        
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not (email.endswith('@intern.com') or email.endswith('@mentor.com')):
            return render_template("register.html", error="Email must end with @intern.com or @mentor.com")

        role = "mentor" if email.endswith('@mentor.com') else "intern"

        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters")

        u = User(
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        try:
            db.session.add(u)
            db.session.commit()
            return redirect("/")
        except:
            db.session.rollback()
            return render_template("register.html", error="Email already exists")
    return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    user = current_user()
    if not user:
        return redirect("/")
    
    if user.role == "mentor":
        # Mentor View: Show all projects from all interns
        projects = Project.query.join(User).filter(User.role == 'intern').order_by(Project.created_at.desc()).all()
        return render_template("mentor_dashboard.html", projects=projects, user=user)
    
    # Intern View
    if request.method == "POST":
        p = Project(name=request.form["name"], description=request.form["description"], user_id=user.id)
        db.session.add(p)
        db.session.commit()
        
    projects = Project.query.filter_by(user_id=user.id).all()
    return render_template("dashboard.html", projects=projects, user=user)

@app.route("/project/<int:project_id>", methods=["GET", "POST"])
def project_detail(project_id):
    user = current_user()
    if not user:
        return redirect("/")
        
    project = db.get_or_404(Project, project_id)
    
    # Permission Check
    is_owner = (project.user_id == user.id)
    if not is_owner and user.role != 'mentor':
         return redirect("/dashboard")

    if request.method == 'POST':
        if not is_owner: # Mentors cannot add logs
            return redirect(url_for('project_detail', project_id=project.id))
            
        file = request.files.get('proof_file')
        proof_path = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.now().timestamp()}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            proof_path = f"proofs/{unique_filename}"

        log = Log(
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            hours=float(request.form['hours']),
            description=request.form['description'],
            proof_path=proof_path,
            project_id=project.id
        )
        db.session.add(log)
        db.session.commit()
        return redirect(url_for('project_detail', project_id=project.id))

    return render_template("project_detail.html", project=project, user=user)

@app.route("/log/<int:log_id>/toggle_status", methods=["POST"])
def toggle_log_status(log_id):
    user = current_user()
    if not user or user.role != "mentor":
        return redirect("/")
        
    log = db.get_or_404(Log, log_id)
    log.is_approved = not log.is_approved
    db.session.commit()
    return redirect(url_for('project_detail', project_id=log.project_id))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/media/<path:filename>')
def media(filename):
    if filename.startswith('proofs/'):
        filename = filename[7:]
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
