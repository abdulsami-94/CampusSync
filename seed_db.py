import os
from app import create_app, db, bcrypt
from app.models import User

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
    print("Database seeding completed successfully.")
