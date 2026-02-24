from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Complaint
from functools import wraps

staff = Blueprint('staff', __name__)

def staff_required(f):
    """Decorator to ensure only staff users can access the route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'staff':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@staff.route("/")
@staff.route("/dashboard")
@staff_required
def dashboard():
    """Staff dashboard - view assigned complaints."""
    complaints = Complaint.query.filter(
        Complaint.assigned_to == current_user.id,
        Complaint.is_deleted == False
    ).order_by(Complaint.date_posted.desc()).all()

    return render_template('staff/dashboard.html', title='Staff Tasks', complaints=complaints)

@staff.route("/update/<int:complaint_id>", methods=['GET', 'POST'])
@staff_required
def update_complaint(complaint_id):
    """Update complaint status - only assigned complaints."""
    complaint = Complaint.query.get_or_404(complaint_id)

    if complaint.is_deleted:
        abort(404)

    if complaint.assigned_to != current_user.id:
        flash('You can only update complaints assigned to you.', 'danger')
        return redirect(url_for('staff.dashboard'))

    if request.method == 'POST':
        new_status = request.form.get('status')
        notes = request.form.get('notes')

        if new_status and new_status in ['In Progress', 'Resolved']:
            complaint.status = new_status
            db.session.commit()

            flash('Complaint updated successfully!', 'success')
            return redirect(url_for('staff.dashboard'))

    return render_template('staff/update_complaint.html', title='Update Task', complaint=complaint)
