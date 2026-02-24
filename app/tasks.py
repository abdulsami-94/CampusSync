from datetime import datetime, timedelta
from app.models import Complaint, ComplaintHistory

def auto_escalate_complaints(app):
    """Auto-escalate complaints older than 3 days that are not resolved."""
    with app.app_context():
        three_days_ago = datetime.utcnow() - timedelta(days=3)
        pending_complaints = Complaint.query.filter(
            ~Complaint.status.in_(['Resolved', 'Escalated']),
            Complaint.date_posted <= three_days_ago,
            Complaint.is_deleted == False
        ).all()

        for c in pending_complaints:
            old_status = c.status
            c.status = 'Escalated'
            history = ComplaintHistory(
                complaint_id=c.id,
                old_status=old_status,
                new_status='Escalated',
                notes='System auto-escalation (> 3 days).',
                changed_by=None
            )
            app.db.session.add(history)
        app.db.session.commit()

def schedule_escalation(app, scheduler):
    """Schedule auto-escalation to run daily."""
    scheduler.add_job(
        func=auto_escalate_complaints,
        args=[app],
        trigger="interval",
        hours=24,
        id='escalation_job',
        replace_existing=True
    )