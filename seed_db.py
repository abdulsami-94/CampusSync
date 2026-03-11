import os
from app import create_app, db, bcrypt
from app.models import User, Complaint
from datetime import datetime, timedelta

# Ensure instance folder exists
os.makedirs(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'), exist_ok=True)
os.makedirs(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads'), exist_ok=True)

app = create_app()

with app.app_context():
    # Create database tables
    db.create_all()
    print("Database tables created.")

    # Create demo users with @asmedu.org emails
    admin_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
    admin_user = User(username='admin', email='admin@asmedu.org', password=admin_pw, role='admin')

    staff_pw = bcrypt.generate_password_hash('staff123').decode('utf-8')
    staff1 = User(username='it_support', email='it.support@asmedu.org', password=staff_pw, role='staff')
    staff2 = User(username='maintenance', email='maintenance@asmedu.org', password=staff_pw, role='staff')

    student_pw = bcrypt.generate_password_hash('student123').decode('utf-8')
    student1 = User(username='alice', email='alice.cs@asmedu.org', password=student_pw, role='student')
    student2 = User(username='bob', email='bob.ee@asmedu.org', password=student_pw, role='student')

    db.session.add_all([admin_user, staff1, staff2, student1, student2])
    db.session.commit()
    print("Created demo users:")
    print("- Admin: admin@asmedu.org / admin123")
    print("- Staff: it.support@asmedu.org / staff123")
    print("- Student: alice.cs@asmedu.org / student123")

    # Hardcode 10 complaints
    now = datetime.utcnow()
    complaints = [
        Complaint(title='Wi-Fi is extremely slow in main library', category='Wi-Fi / Internet', description='The wireless signal on the 2nd floor of the library drops constantly. Cannot study.', priority='High', location='Main Library 2nd Floor', status='Pending', user_id=student1.id, date_posted=now - timedelta(days=2)),
        Complaint(title='Projector broken in Room 301', category='Classrooms', description='The projector bulb burned out during class yesterday and hasn\'t been replaced.', priority='Medium', location='Building A, Room 301', status='In Progress', user_id=student2.id, date_posted=now - timedelta(days=1), assigned_to=staff1.id),
        Complaint(title='Water cooler not working', category='Washrooms', description='The water cooler near the engineering block is dispensing hot water.', priority='Low', location='Engineering Block Ground', status='Resolved', user_id=student1.id, date_posted=now - timedelta(days=5), date_resolved=now - timedelta(days=2)),
        Complaint(title='Keyboard missing keys in Lab 4', category='Computer Labs', description='PC #12 in lab 4 is missing the Spacebar and Enter keys.', priority='Medium', location='CS Lab 4', status='Pending', user_id=student2.id, date_posted=now - timedelta(hours=5)),
        Complaint(title='Canteen food quality issue', category='Canteen', description='Found stale bread being served at the main canteen today.', priority='High', location='Main Canteen', status='Pending', user_id=student1.id, date_posted=now - timedelta(hours=2)),
        Complaint(title='Power outage in Hostel B', category='Hostel', description='Entire left wing of Hostel B has no power since morning.', priority='High', location='Hostel B, Left Wing', status='In Progress', user_id=student2.id, date_posted=now - timedelta(days=1), assigned_to=staff2.id),
        Complaint(title='Basketball court net torn', category='Sports Facilities', description='The net on the north hoop of the outdoor basketball court is completely torn.', priority='Low', location='Outdoor Courts', status='Pending', user_id=student1.id, date_posted=now - timedelta(days=3)),
        Complaint(title='Broken chair in Library read room', category='Library', description='Several chairs have broken wheels and are dangerous to sit on.', priority='Medium', location='Library Reading Room 1', status='Resolved', user_id=student2.id, date_posted=now - timedelta(days=10), date_resolved=now - timedelta(days=8)),
        Complaint(title='Fluorescent light flickering', category='Electricity', description='Light above my desk is flickering rapidly, giving me headaches.', priority='Low', location='Room 105, Arts Block', status='Pending', user_id=student1.id, date_posted=now - timedelta(hours=10)),
        Complaint(title='Stray dogs near parking', category='Other', description='There are aggressive stray dogs near the student parking lot causing issues.', priority='Medium', location='Student Parking Lot', status='Pending', user_id=student2.id, date_posted=now - timedelta(days=4))
    ]
    
    db.session.add_all(complaints)
    db.session.commit()
    print("Seeded 10 dummy complaints.")
    print("Database seeding completed successfully.")
