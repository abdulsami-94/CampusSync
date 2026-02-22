# CivicSync – Centralized Complaint Registration System

A full-stack web application built with Python Flask, SQLite, HTML, CSS (Bootstrap), and JavaScript (Chart.js), designed for managing civic complaints.

## Roles and Features

1. **Citizen Portal**:
   - Register logic & Login.
   - Submit new complaints with images and location data.
   - Edit pending complaints.
   - View history of their complaints.

2. **Admin Panel**:
   - Dashboard with visual analytics (Chart.js pie & bar charts).
   - Filter all complaints by status and category.
   - Assign complaints to staff members.
   - Export complaint data to CSV.

3. **Staff Panel**:
   - View assigned complaints.
   - Update complaint statuses (In Progress, Resolved, Escalated).
   - Add resolution notes.

4. **Advanced Escalation Logic**:
   - Any complaint not resolved within 3 days is automatically escalated when checked.
   - Full history tracking for every status change.

---

## Setup & Run Instructions

### 1. Requirements

Ensure you have Python 3 installed.

### 2. Create Virtual Environment & Install Dependencies

```bash
# Inside the CivicSync directory
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Initialize the Database with Sample Data

Run the seeding script to create the DB tables and populate it with sample users and complaints:

```bash
python seed_db.py
```

**Sample Accounts Created:**
- Admin: `admin@civicsync.com` / `admin123`
- Staff: `john.staff@civicsync.com` / `staff123`
- Citizen: `alice@example.com` / `citizen123`

### 4. Run the Application

```bash
python run.py
```

The app will be available at `http://127.0.0.1:5000/`.

---

## Architecture Overview
- `app/__init__.py`: App factory and extension initialization.
- `app/models.py`: Database definitions (User, Complaint, ComplaintHistory).
- `app/auth.py`: Authentication routes using Flask-Login.
- `app/citizen.py`, `app/admin.py`, `app/staff.py`: Role-specific routing and views.
- `app/templates/`: Jinja2 HTML templates utilizing Bootstrap 5.
- `app/static/`: Custom CSS, generic JS, and upload folder.
