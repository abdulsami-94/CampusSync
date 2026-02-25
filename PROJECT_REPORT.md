# CAMPUSSYNC - Complaint Management System
## Project Report

**Date:** 25 February 2026  
**Version:** 1.0  
**Institution:** ASM CSIT College  
**Developer:** Abdul Sami Shaikh  

---

## 📄 1. Software Requirements Specification (SRS)

### 1.1 Introduction

CampusSync is a comprehensive web-based complaint management system designed specifically for ASM CSIT College. The system facilitates efficient communication between students, staff, and administrators for handling campus-related issues and maintenance requests.

### 1.2 Purpose

The primary purpose of CampusSync is to:
- Provide students with an easy-to-use platform to report campus issues
- Enable administrators to efficiently manage and assign complaints
- Allow staff members to track and resolve assigned complaints
- Maintain transparency and accountability in complaint resolution
- Generate analytics for better campus maintenance planning

### 1.3 Scope

**In Scope:**
- User registration and authentication with role-based access
- Complaint submission with categories, priorities, and file uploads
- Admin dashboard with complaint management and analytics
- Staff dashboard for assigned complaint tracking
- Student dashboard for complaint monitoring
- Real-time status updates and notifications
- Responsive web interface for desktop and mobile access

**Out of Scope:**
- Mobile application development
- Integration with existing college management systems
- Automated complaint categorization using AI
- SMS/email notification system
- Multi-language support

### 1.4 Functional Requirements

#### User Management
- **FR1:** System shall allow user registration with email validation (@asmedu.org domain)
- **FR2:** System shall support three user roles: Admin, Staff, and Student
- **FR3:** System shall provide secure login/logout functionality
- **FR4:** System shall enforce role-based access control

#### Complaint Management
- **FR5:** Students shall submit complaints with title, category, description, priority, and location
- **FR6:** Students shall upload images with complaints (max 16MB)
- **FR7:** Admins shall view all complaints with filtering and search capabilities
- **FR8:** Admins shall assign complaints to staff members
- **FR9:** Admins shall reassign complaints to different staff members
- **FR10:** Staff shall update complaint status (Pending → In Progress → Resolved)
- **FR11:** System shall maintain complaint history and timestamps

#### Dashboard and Analytics
- **FR12:** Admins shall view complaint statistics (total, pending, resolved)
- **FR13:** System shall display complaint status breakdown (pie chart)
- **FR14:** System shall display complaint category breakdown (bar chart)
- **FR15:** Students shall view their complaint history with pagination

#### Security and Data Management
- **FR16:** System shall implement CSRF protection on all forms
- **FR17:** System shall hash passwords using bcrypt
- **FR18:** System shall support soft deletion of complaints
- **FR19:** System shall validate file uploads (image types only)

### 1.5 Non-functional Requirements

#### Performance
- **NFR1:** System shall handle up to 1000 concurrent users
- **NFR2:** Page load time shall not exceed 3 seconds
- **NFR3:** Database queries shall complete within 1 second

#### Usability
- **NFR4:** System shall be responsive on mobile devices
- **NFR5:** Interface shall follow Bootstrap design principles
- **NFR6:** System shall provide clear error messages and validation feedback

#### Security
- **NFR7:** System shall use HTTPS for production deployment
- **NFR8:** Session cookies shall be HTTPOnly and secure
- **NFR9:** Passwords shall be minimum 8 characters
- **NFR10:** File uploads shall be restricted to safe image formats

#### Reliability
- **NFR11:** System shall have 99% uptime
- **NFR12:** Database transactions shall be atomic
- **NFR13:** System shall handle database connection failures gracefully

### 1.6 System Constraints

#### Technical Constraints
- **SC1:** Must use Python Flask framework
- **SC2:** Must use SQLite database for simplicity
- **SC3:** Must be deployable on Heroku or similar PaaS
- **SC4:** Must support modern browsers (Chrome, Firefox, Safari, Edge)

#### Business Constraints
- **SC5:** Must restrict registration to @asmedu.org email domain
- **SC6:** Must maintain data integrity and user privacy
- **SC7:** Must be college-level project (not enterprise-grade)

---

## 📊 2. ER Diagram

### 2.1 Entities

#### User Entity
- **Attributes:**
  - id (Primary Key, Integer, Auto-increment)
  - username (String, 20 chars, Unique, Not Null)
  - email (String, 120 chars, Unique, Not Null)
  - password (String, 60 chars, Not Null)
  - role (String, 20 chars, Not Null) - Values: 'admin', 'staff', 'student'

#### Complaint Entity
- **Attributes:**
  - id (Primary Key, Integer, Auto-increment)
  - title (String, 100 chars, Not Null)
  - category (String, 50 chars, Not Null)
  - description (Text, Not Null)
  - priority (String, 20 chars, Not Null) - Values: 'Low', 'Medium', 'High'
  - location (String, 100 chars, Not Null)
  - image_file (String, 100 chars, Nullable)
  - date_posted (DateTime, Not Null, Default: Current UTC)
  - status (String, 20 chars, Not Null) - Values: 'Pending', 'In Progress', 'Resolved'
  - user_id (Foreign Key → User.id, Not Null)
  - assigned_to (Foreign Key → User.id, Nullable)
  - is_deleted (Boolean, Not Null, Default: False)

### 2.2 Relationships

#### User → Complaint (One-to-Many)
- **Type:** One user can submit many complaints
- **Cardinality:** 1:N
- **Foreign Key:** Complaint.user_id → User.id

#### User → Complaint (Assignment, One-to-Many)
- **Type:** One staff member can be assigned many complaints
- **Cardinality:** 1:N
- **Foreign Key:** Complaint.assigned_to → User.id

### 2.3 ER Diagram Representation

```
┌─────────────┐       ┌─────────────┐
│    User     │       │  Complaint  │
├─────────────┤       ├─────────────┤
│ id (PK)     │◄────┐ │ id (PK)     │
│ username    │     │ │ title       │
│ email       │     │ │ category    │
│ password    │     │ │ description │
│ role        │     │ │ priority    │
└─────────────┘     │ │ location    │
                    │ │ image_file  │
                    │ │ date_posted │
                    │ │ status      │
                    │ │ user_id (FK)│
                    └─────────────┘
                          │
                          │ assigned_to (FK)
                          ▼
                    ┌─────────────┐
                    │    User     │
                    │  (Staff)    │
                    └─────────────┘
```

---

## 🧩 3. Module Diagram

### 3.1 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CampusSync Web Application               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Presentation  │  │   Business      │  │   Data      │  │
│  │   Layer         │  │   Logic Layer   │  │   Layer     │  │
│  │                 │  │                 │  │             │  │
│  │  • Templates    │  │  • Flask Routes │  │  • SQLite   │  │
│  │  • Static Files │  │  • Controllers  │  │  • Models   │  │
│  │  • Bootstrap    │  │  • Validation   │  │  • ORM      │  │
│  │  • Chart.js     │  │  • Security     │  │             │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Flask-WTF     │  │   Flask-Login   │  │   Bcrypt    │  │
│  │   (Forms)       │  │   (Auth)        │  │   (Crypto)  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Module Breakdown

#### 3.2.1 Authentication Module (auth.py)
- **Functions:**
  - User registration with email domain validation
  - Secure login/logout with session management
  - Password hashing and verification
  - Role-based redirection after login

#### 3.2.2 Admin Module (admin.py)
- **Functions:**
  - Complaint listing with filtering and pagination
  - Staff assignment and reassignment
  - Complaint soft deletion
  - Analytics data aggregation
  - Dashboard statistics generation

#### 3.2.3 Staff Module (staff.py)
- **Functions:**
  - Assigned complaint viewing
  - Status updates (In Progress → Resolved)
  - Complaint details display
  - Task management interface

#### 3.2.4 Student Module (student.py)
- **Functions:**
  - Complaint submission with file upload
  - Personal complaint history
  - Complaint editing (pending status only)
  - Complaint details viewing

#### 3.2.5 Models Module (models.py)
- **Classes:**
  - User model with role-based relationships
  - Complaint model with soft delete functionality
  - Database initialization and user loader

#### 3.2.6 Configuration Module (config.py)
- **Settings:**
  - Database configuration
  - Security settings (CSRF, sessions)
  - File upload configuration
  - Email domain restrictions

---

## ⏳ 4. Estimation

### 4.1 Time Estimation

#### Development Phases
- **Planning & Design:** 2 weeks
  - Requirements gathering: 3 days
  - ER diagram design: 2 days
  - UI/UX wireframing: 3 days
  - Technology selection: 2 days
  - Project setup: 2 days

- **Backend Development:** 4 weeks
  - Database models: 1 week
  - Authentication system: 1 week
  - API endpoints: 1 week
  - Business logic: 1 week

- **Frontend Development:** 3 weeks
  - Base templates: 1 week
  - Role-specific dashboards: 1 week
  - Forms and validation: 1 week

- **Integration & Testing:** 2 weeks
  - Module integration: 1 week
  - Testing and debugging: 1 week

- **Deployment & Documentation:** 1 week
  - Production deployment: 3 days
  - Documentation: 4 days

**Total Estimated Time:** 12 weeks (3 months)

### 4.2 Development Phases Timeline

```
Week 1-2:   Planning & Design Phase
Week 3-6:   Backend Development
Week 7-9:   Frontend Development
Week 10-11: Integration & Testing
Week 12:    Deployment & Documentation
```

### 4.3 Resource Requirements

#### Human Resources
- **1 Full-stack Developer:** Python Flask expertise
- **1 UI/UX Designer:** Bootstrap and responsive design
- **1 Database Administrator:** SQLite optimization
- **1 QA Tester:** Manual testing and validation

#### Hardware Resources
- **Development Machine:** MacBook Pro with 16GB RAM
- **Testing Environment:** Local development server
- **Production Server:** Heroku free tier or VPS

#### Software Resources
- **Development Tools:** VS Code, Git, Postman
- **Database Tools:** SQLite Browser, DBeaver
- **Version Control:** GitHub repository
- **Documentation:** Markdown, Draw.io

---

## 💰 5. Cost Estimation

### 5.1 Development Cost (Hypothetical)

#### Human Resource Costs
- **Senior Developer:** $50/hour × 480 hours = $24,000
- **UI/UX Designer:** $40/hour × 160 hours = $6,400
- **QA Tester:** $30/hour × 80 hours = $2,400
- **Project Manager:** $60/hour × 40 hours = $2,400

**Total Human Cost:** $35,200

#### Tool and Software Costs
- **Development Tools:** VS Code (Free), GitHub (Free) = $0
- **Domain & Hosting:** Heroku Free Tier = $0
- **SSL Certificate:** Let's Encrypt (Free) = $0
- **Design Tools:** Figma (Free tier) = $0

**Total Tool Cost:** $0

#### Training and Miscellaneous
- **Online Courses:** Udemy Flask courses = $50
- **Books/Documentation:** Online resources = $0
- **Miscellaneous:** Internet, electricity = $200

**Total Miscellaneous Cost:** $250

**Total Development Cost:** $35,450

### 5.2 Hardware/Software Cost

#### Hardware Requirements
- **Development Workstation:** Already owned = $0
- **Testing Devices:** Mobile phones for responsive testing = $0
- **Backup Storage:** External HDD = $50

#### Software Licenses
- **Operating System:** macOS (Already owned) = $0
- **Database Software:** SQLite (Free) = $0
- **Development IDE:** VS Code (Free) = $0
- **Version Control:** Git (Free) = $0

**Total Hardware/Software Cost:** $50

### 5.3 Maintenance Cost

#### Annual Maintenance Costs
- **Hosting:** Heroku Hobby ($7/month) = $84/year
- **Domain Renewal:** Free (GitHub Pages) = $0
- **SSL Certificate:** Free (Let's Encrypt) = $0
- **Backup Storage:** Additional cloud storage = $20/year
- **Security Updates:** Developer time (4 hours/year) = $200

**Total Annual Maintenance Cost:** $304

#### 3-Year Maintenance Projection
- **Year 1:** $304
- **Year 2:** $350 (10% increase)
- **Year 3:** $400 (15% increase)

**Total 3-Year Maintenance Cost:** $1,054

### 5.4 Cost Breakdown Summary

| Category | Cost | Percentage |
|----------|------|------------|
| Development | $35,450 | 97% |
| Hardware/Software | $50 | 0.1% |
| Maintenance (3 years) | $1,054 | 2.9% |
| **Total** | **$36,554** | **100%** |

---

## 🛠 6. Technology Used

### 6.1 Platform
- **Operating System:** macOS (Development), Linux (Production)
- **Web Server:** Gunicorn (Production), Flask development server (Development)
- **Deployment Platform:** Heroku / Railway / DigitalOcean
- **Version Control:** Git with GitHub

### 6.2 Programming Language
- **Primary Language:** Python 3.9+
- **Web Framework:** Flask 3.0.2
- **Template Engine:** Jinja2 (built-in with Flask)
- **Scripting:** Bash/Shell for deployment scripts

### 6.3 Database
- **Database Type:** SQLite 3 (Development & Production)
- **ORM:** SQLAlchemy 2.0.46
- **Migration Tool:** Flask-Migrate (Alembic)
- **Database Browser:** DB Browser for SQLite

### 6.4 Tools and Libraries

#### Backend Libraries
- **Authentication:** Flask-Login 0.6.3
- **Forms:** Flask-WTF 1.2.1
- **Password Hashing:** Flask-Bcrypt 1.0.1
- **Database:** Flask-SQLAlchemy 3.1.1
- **Pagination:** Flask-Paginate 2024.4.12
- **Email Validation:** WTForms Email Validator

#### Frontend Libraries
- **CSS Framework:** Bootstrap 5.3
- **JavaScript Library:** Chart.js 4.4.0 (for analytics)
- **Icons:** Bootstrap Icons (CDN)
- **Responsive Design:** Bootstrap Grid System

#### Development Tools
- **IDE:** Visual Studio Code
- **Version Control:** Git
- **API Testing:** Postman / Insomnia
- **Database GUI:** SQLite Browser
- **Documentation:** Markdown, Draw.io

#### Deployment Tools
- **Containerization:** Docker (optional)
- **CI/CD:** GitHub Actions (optional)
- **Monitoring:** Heroku Logs
- **Backup:** Automated database dumps

---

## 🧪 7. Testing

### 7.1 Test Cases

#### Authentication Test Cases

**TC-AUTH-001: User Registration**
- **Description:** Test user registration with valid @asmedu.org email
- **Preconditions:** User not registered
- **Steps:**
  1. Navigate to registration page
  2. Enter valid details with @asmedu.org email
  3. Submit form
- **Expected Result:** User created, redirected to login
- **Status:** ✅ Pass

**TC-AUTH-002: Invalid Email Domain**
- **Description:** Test registration with invalid email domain
- **Preconditions:** None
- **Steps:**
  1. Attempt registration with @gmail.com email
  2. Submit form
- **Expected Result:** Error message "Only ASM CSIT emails allowed"
- **Status:** ✅ Pass

**TC-AUTH-003: Admin Login Redirect**
- **Description:** Test admin login redirects to admin dashboard
- **Preconditions:** Admin user exists
- **Steps:**
  1. Login as admin (admin@asmedu.org / admin123)
  2. Submit login form
- **Expected Result:** Redirected to /admin/dashboard
- **Status:** ✅ Pass

#### Complaint Management Test Cases

**TC-COMP-001: Student Complaint Submission**
- **Description:** Test complaint creation with file upload
- **Preconditions:** Student logged in
- **Steps:**
  1. Navigate to complaint creation page
  2. Fill all required fields
  3. Upload image file
  4. Submit form
- **Expected Result:** Complaint created, success message shown
- **Status:** ✅ Pass

**TC-COMP-002: Admin Complaint Assignment**
- **Description:** Test assigning complaint to staff
- **Preconditions:** Admin logged in, complaint exists
- **Steps:**
  1. Navigate to admin dashboard
  2. Click "Assign" on unassigned complaint
  3. Select staff member
  4. Submit assignment
- **Expected Result:** Complaint assigned, status changed to "In Progress"
- **Status:** ✅ Pass

**TC-COMP-003: Staff Status Update**
- **Description:** Test staff updating complaint status
- **Preconditions:** Staff logged in, complaint assigned
- **Steps:**
  1. Navigate to staff dashboard
  2. Click "Update Status" on assigned complaint
  3. Change status to "Resolved"
  4. Submit update
- **Expected Result:** Status updated successfully
- **Status:** ✅ Pass

#### Security Test Cases

**TC-SEC-001: CSRF Protection**
- **Description:** Test CSRF token validation
- **Preconditions:** User logged in
- **Steps:**
  1. Attempt form submission without CSRF token
  2. Attempt form submission with invalid CSRF token
- **Expected Result:** Requests rejected with 400 Bad Request
- **Status:** ✅ Pass

**TC-SEC-002: Role-Based Access Control**
- **Description:** Test student cannot access admin routes
- **Preconditions:** Student logged in
- **Steps:**
  1. Attempt to access /admin/dashboard
- **Expected Result:** Redirected to login or 403 Forbidden
- **Status:** ✅ Pass

### 7.2 Sample Outputs

#### Database Contents (via view_db.py)
```
============================================================
CAMPUSSYNC DATABASE VIEWER
============================================================

👥 USERS:
----------------------------------------
ID:  6 | admin           | admin@asmedu.org          | admin
ID:  7 | it_support      | it.support@asmedu.org     | staff
ID:  8 | maintenance     | maintenance@asmedu.org    | staff
ID:  9 | alice           | alice.cs@asmedu.org       | student
ID: 10 | bob             | bob.ee@asmedu.org         | student
ID: 11 | Sami            | sami@asmedu.org           | student

📋 COMPLAINTS:
----------------------------------------
ID:  1 | Water           | Water Supply    | ✅ Resolved     | it_support   | False
ID:  2 | LAB PC          | Electricity     | 🔄 In Progress  | maintenance  | False
============================================================
```

#### Flask Application Output
```
Database tables created.
Created demo users:
- Admin: admin@asmedu.org / admin123
- Staff: it.support@asmedu.org / staff123
- Student: alice.cs@asmedu.org / student123
Database seeding completed successfully.
 * Serving Flask app 'run'
 * Debug mode: on
 * Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)
```

### 7.3 Screenshots

#### Login Page
```
┌─────────────────────────────────────────────────────────────┐
│                    CampusSync Login                         │
├─────────────────────────────────────────────────────────────┤
│  Email: [admin@asmedu.org]                                  │
│  Password: [••••••••]                                       │
│  [✓] Remember Me                                            │
│                                                             │
│  [Login]                    [Register New Account]          │
└─────────────────────────────────────────────────────────────┘
```

#### Admin Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│                    Admin Dashboard                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ Total: 2    │ │ Pending: 0  │ │ Resolved: 1 │            │
│  │ Complaints  │ │ Complaints  │ │ Complaints  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│                                                             │
│  ┌─────────────────┐ ┌─────────────────┐                    │
│  │ Status Pie Chart│ │ Category Bar    │                    │
│  │ ✅ 50% Resolved │ │ Chart           │                    │
│  │ 🔄 50% Progress │ │ Water Supply: 1 │                    │
│  │                 │ │ Electricity: 1  │                    │
│  └─────────────────┘ └─────────────────┘                    │
│                                                             │
│  Complaints Table:                                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ ID │ Title    │ Status     │ Assigned To │ Actions │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │ 1  │ Water    │ ✅ Resolved │ it_support  │ Delete  │    │
│  │ 2  │ LAB PC   │ 🔄 Progress │ maintenance │ Delete  │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

#### Student Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│                    My Complaints                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Title: LAB PC Issue                                 │    │
│  │ Category: Electricity                               │    │
│  │ Status: 🔄 In Progress                              │    │
│  │ Assigned To: maintenance                            │    │
│  │ Date: 2026-02-25                                    │    │
│  │ [View Details] [Edit]                               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  [Register New Complaint]                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 8. Conclusion

CampusSync represents a comprehensive solution for complaint management at ASM CSIT College. The system successfully implements all required features with a focus on simplicity, security, and user experience.

### Key Achievements
- ✅ Complete role-based access control system
- ✅ Responsive web interface with Bootstrap
- ✅ Secure authentication with CSRF protection
- ✅ Comprehensive complaint management workflow
- ✅ Visual analytics dashboard for administrators
- ✅ File upload functionality with validation
- ✅ Soft delete functionality for data integrity

### Technical Highlights
- **Framework:** Flask 3.0 with modern Python practices
- **Database:** SQLite with SQLAlchemy ORM
- **Security:** bcrypt hashing, CSRF protection, role-based access
- **UI/UX:** Bootstrap 5 with Chart.js analytics
- **Deployment:** Ready for Heroku/Railway deployment

### Future Enhancements
- Email notifications for status updates
- Mobile application development
- Advanced analytics and reporting
- Integration with college management systems
- Multi-language support

The project demonstrates solid software engineering practices and is ready for college-level deployment and demonstration.

---

**End of Report**