from datetime import datetime, timedelta
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
from app import db
from app.models import Complaint, ComplaintHistory
from functools import wraps

staff = Blueprint('staff', __name__)

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'staff':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def check_escalations():
    """Utility function to auto-escalate complaints older than 3 days that are not resolved."""
    three_days_ago = datetime.utcnow() - timedelta(days=3)
    
    # Exclude Resolved and already Escalated
    pending_complaints = Complaint.query.filter(
        Complaint.status.not_in(['Resolved', 'Escalated']),
        Complaint.date_posted <= three_days_ago
    ).all()
    
    for c in pending_complaints:
        old_status = c.status
        c.status = 'Escalated'
        history = ComplaintHistory(complaint_id=c.id, old_status=old_status, 
                                   new_status='Escalated', notes='System auto-escalation (> 3 days).', 
                                   changed_by=None) # System change
        db.session.add(history)
    db.session.commit()

@staff.route("/")
@staff.route("/dashboard")
@staff_required
def dashboard():
    check_escalations()
    # View assigned complaints
    complaints = Complaint.query.filter_by(assignee=current_user).order_by(Complaint.date_posted.desc()).all()
    return render_template('staff/dashboard.html', title='Staff Tasks', complaints=complaints)

@staff.route("/update/<int:complaint_id>", methods=['GET', 'POST'])
@staff_required
def update_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    if complaint.assignee != current_user:
        flash('You can only update complaints assigned to you.', 'danger')
        return redirect(url_for('staff.dashboard'))

    if request.method == 'POST':
        new_status = request.form.get('status')
        notes = request.form.get('notes')
        
        if new_status and new_status != complaint.status:
            old_status = complaint.status
            complaint.status = new_status
            
            history = ComplaintHistory(complaint_id=complaint.id, old_status=old_status, 
                                       new_status=new_status, notes=notes, 
                                       changed_by=current_user.id)
            db.session.add(history)
            db.session.commit()
            
            flash('Complaint updated successfully!', 'success')
            return redirect(url_for('staff.dashboard'))

    return render_template('staff/update_complaint.html', title='Update Task', complaint=complaint)
