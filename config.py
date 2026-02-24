import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Basic security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database: Simple SQLite setup
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'campussync.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File uploads
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    # Basic security settings
    WTF_CSRF_ENABLED = True

    # Email domain restriction for ASM CSIT
    ALLOWED_EMAIL_DOMAIN = 'asmedu.org'
