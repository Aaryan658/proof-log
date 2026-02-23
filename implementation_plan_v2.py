import os
from datetime import datetime
from flask import Flask, request, session, redirect, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'media/proofs')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default='intern') # 'intern' or 'mentor'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    proof_path = db.Column(db.String(500)) # Optional file path
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    project = db.relationship('Project', backref=db.backref('logs', lazy=True))

# --- Helpers ---
def current_user():
    if "user_id" in session:
        return db.session.get(User, session["user_id"])
    return None

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    # Login logic with Role check if needed, or just redirect to dashboard
    pass 

@app.route("/register", methods=["GET", "POST"])
def register():
    # Add role selection
    pass

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    # Show projects. If mentor, maybe show something else? 
    # For now, simplistic: Mentors can also create projects or just view? 
    # Requirement: "Mentor can view intern’s logs". 
    # Let's keep it simple: Everyone sees their own "Projects". 
    # Maybe add a "View Intern Project" feature later or simple URL sharing.
    pass

@app.route("/project/<int:project_id>", methods=["GET", "POST"])
def project_detail(project_id):
    # Add Log logic (Date, Hours, Description, Proof)
    pass

@app.route("/media/<path:filename>")
def media(filename):
    return send_from_directory('media', filename)
