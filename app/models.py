from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'student', 'admin', 'staff'

    # Relationships
    complaints = db.relationship('Complaint', backref='author', lazy=True, foreign_keys='Complaint.user_id')
    assigned_complaints = db.relationship('Complaint', backref='assignee', lazy=True, foreign_keys='Complaint.assigned_to')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Wi-Fi / Internet, Classrooms, etc.
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False, default='Low')  # Low, Medium, High
    location = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(100), nullable=True)  # UUID filename
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_resolved = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Pending, In Progress, Resolved

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Staff ID

    # Soft delete for admin
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    upvotes = db.relationship('Upvote', backref='complaint', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='complaint_ref', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Complaint('{self.title}', '{self.date_posted}', '{self.status}')"

class Upvote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'complaint_id', name='_user_complaint_uc'),)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    author = db.relationship('User', backref=db.backref('comments', lazy=True))
