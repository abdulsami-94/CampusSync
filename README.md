# CampusSync: College Campus Issue Management System

## 1. Project Title
**CampusSync: A Centralised College Campus Issue Management System**

## 2. Project Description
CampusSync is a web-based reporting and management framework designed to streamline the resolution of infrastructural and academic issues within a university campus environment. The system addresses the inefficiencies of traditional, paper-based, or decentralised reporting mechanisms by providing a unified digital platform. It facilitates communication between students, faculty (staff), and administration, ensuring accountability, transparency, and timely resolution of reported issues such as laboratory equipment malfunctions, classroom maintenance, and hostel infrastructure problems.

## 3. Features
* **Role-Based Access Control (RBAC):** Distinct interfaces and privileges for Administrators, Staff/Maintenance, and Students.
* **Centralised Issue Submission:** A streamlined portal for students to submit detailed complaints, including categorical classification, priority designation, and location tracking.
* **Algorithmic Duplicate Prevention:** Intelligent filtering mechanism that cross-references new submissions against existing unresolved cases based on location and title clustering to prevent database redundancy.
* **Lifecycle State Tracking:** Real-time visibility into the status of an issue transitioning from 'Pending' through 'In Progress' to 'Resolved'.
* **Automated Email Notifications:** Integration with SMTP protocols to dispatch automated resolution confirmations to the original reporter.
* **Historical Audit Trail:** Comprehensive logging of all status modifications for administrative oversight and performance analytics.

## 4. Tech Stack
* **Frontend:** HTML5, CSS3, Bootstrap 5 (Responsive Design Pattern)
* **Backend:** Python 3.11+, Flask (Micro web framework)
* **Database Management:** SQLite (Development) / PostgreSQL (Production) mapped via SQLAlchemy ORM
* **Authentication & Security:** Flask-Login (Session management), Flask-Bcrypt (Password hashing), Flask-WTF (CSRF Protection)
* **Communication:** Flask-Mail (SMTP notification routing)
* **Deployment Infrastructure:** Gunicorn WSGI, Render Cloud Hosting Platform

## 5. System Architecture Overview
The application follows a Model-View-Controller (MVC) architectural pattern:
* **Model:** SQLAlchemy manages the object-relational mapping, representing the `User`, `Complaint`, and `ComplaintHistory` schemas.
* **View:** Jinja2 templating engine renders dynamic HTML pages, populating them with contextual data tailored to the active user's role.
* **Controller:** Flask Blueprints (`auth.py`, `student.py`, `staff.py`, `admin.py`) dictate routing logic, handle HTTP requests, enforce access restrictions, and manipulate the Model layer.

## 6. Database Schema Overview
The relational database comprises three primary entities:

1. **User Model:** 
   * Stores credential data (`username`, `email`, hashed `password`).
   * Enforces role distinctions (`student`, `staff`, `admin`).
   * Maintains foreign key relationships to complaints initiated or assigned.

2. **Complaint Model:**
   * Serves as the core entity, holding the `title`, `description`, `category` (e.g., Hostel, Lab), `priority`, and geographic `location`.
   * Tracks progression timestamps (`date_posted`, `resolved_at`) and current `status` enum.
   * Links to the `User` model via `author_id` and an optional `assigned_to` key.

3. **ComplaintHistory Model:**
   * Acts as an immutable ledger.
   * Records every state change against a `complaint_id`, detailing the `old_status`, `new_status`, timestamp, and the actor responsible, ensuring compliance and analytical capability.

## 7. Installation Steps (Local Environment)

### Prerequisites
* Python 3.11 or higher
* `pip` (Python package installer)

### Setup Instructions
1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd CampusSync
   ```

2. **Initialise Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   Create a `.env` file in the root directory and populate it with local testing variables:
   ```env
   SECRET_KEY=local_development_key
   MAIL_SERVER=smtp.example.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your_email@example.com
   MAIL_PASSWORD=your_app_password
   ```

5. **Initialise Database & Seed Default Data:**
   ```bash
   python seed_db.py
   ```

6. **Execute Application:**
   ```bash
   export FLASK_APP=run.py
   export FLASK_DEBUG=1
   flask run --port=5000
   ```

## 8. Deployment Steps (Render Platform)
1. Ensure the repository contains a valid `requirements.txt` and `runtime.txt` (specifying e.g., `python-3.11.6`).
2. Verify the `Procfile` exists or configure Render's Start Command precisely as `gunicorn run:app`.
3. Connect the GitHub repository to a new Render Web Service instance.
4. Define Environment Variables within the Render dashboard:
   * `SECRET_KEY` (Cryptographically secure random string)
   * `DATABASE_URL` (Internal PostgreSQL connection string provided by Render)
   * `MAIL_*` configurations for SMTP access.
5. Deploy the application.

## 9. How Role-Based Access Works
The system implements strict access controls using `Flask-Login` decorators combined with custom role verification functions. When a resource is requested (e.g., the Admin Dashboard), the routing controller verifies the authenticated session via `@login_required` and subsequently evaluates the `current_user.role` attribute. Attempting lateral privilege escalation (e.g., a student requesting the staff dashboard) results in an HTTP 403 Forbidden abort or an immediate redirection to the authentication gateway.

## 10. How Duplicate Filtering Works
To mitigate database bloat and redundant maintenance requests, the submission controller executes a pre-insertion validation query. Upon receiving a POST request for a new issue, the ORM queries the `Complaint` table for existing records matching the exact structural combination of the incoming `title` and `location` parameters, filtered further to exclude records where the status is currently 'Resolved'. If a match is flagged, the transaction is halted, and the user receives a warning notification.

## 11. How Email Notification Works
When a staff member or administrator updates a complaint's status to 'Resolved', the controller invokes `Flask-Mail` modules. The application dynamically constructs an email payload referencing the original `Complaint.author.email`, the `Complaint.title`, and the time of resolution. This packet is transferred securely over TLS via the SMTP credentials provided securely defined in the host's environment variables.

## 12. Folder Structure Explanation
```text
CampusSync/
├── app/
│   ├── templates/          # Jinja2 HTML View templates separated by role
│   ├── static/             # Static assets (CSS, JS, Uploaded context images)
│   ├── __init__.py         # Application factory pattern and extension initialisation
│   ├── models.py           # SQLAlchemy database schema declarations
│   ├── auth.py             # User registration and session controllers
│   ├── student.py          # Student interface routing
│   ├── staff.py            # Maintenance staff interface routing
│   └── admin.py            # Administrative oversight routing
├── instance/               # Local SQLite database housing
├── config.py               # Centralised configuration parsing
├── run.py                  # WSGI entry point execution script
├── seed_db.py              # Automated database population script
├── requirements.txt        # Verified production and development dependencies
└── runtime.txt             # PaaS Python version specification
```

## 13. Future Enhancements
* **Machine Learning Categorisation:** Implement NLP models to auto-categorise issue descriptions, reducing human filing errors.
* **Geospatial Mapping:** Integrate a campus map API to allow precise pin-drop reporting of external infrastructure faults.
* **Service Level Agreement (SLA) Tracking:** Introduce timers that trigger automatic escalations to the Dean/Administration if high-priority infrastructure remains unresolved within 48 hours.
* **Mobile Application Deployment:** Encapsulate the web views into a reactive native container for iOS and Android platforms via progressive web application (PWA) standards.

## 14. Conclusion
CampusSync demonstrates a practical application of modern web development frameworks to solve real-world institutional logistics. By enforcing strict data integrity, securing session states, and structuring code maintainability through the MVC pattern, this application serves as a robust proof-of-concept for enterprise-grade campus management software.
