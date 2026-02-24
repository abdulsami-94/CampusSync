from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Create database tables in development
    with app.app_context():
        db.create_all()
        print('Database tables created.')

    # Run the application
    app.run(debug=True, port=8000)
