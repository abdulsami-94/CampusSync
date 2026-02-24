import pytest
from app import create_app, db
from app.models import User, Complaint

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    with app.app_context():
        db.create_all()  # Use create_all for in-memory testing
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_valid_email(app):
    with app.app_context():
        from app.auth import validate_email_domain
        assert validate_email_domain('student@asmedu.org') == True
        assert validate_email_domain('student@gmail.com') == False

def test_password_validation(app):
    with app.app_context():
        from app.auth import validate_password
        valid, msg = validate_password('Password123')
        assert valid == True
        valid, msg = validate_password('pass')
        assert valid == False

def test_complaint_creation(app):
    with app.app_context():
        user = User(username='test', email='test@asmedu.org', password='hashed', role='student')
        db.session.add(user)
        db.session.commit()

        complaint = Complaint(title='Test', category='Test', description='Test',
                            location='Test', author=user)
        db.session.add(complaint)
        db.session.commit()

        assert complaint.id is not None
        assert complaint.status == 'Pending'