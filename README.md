# job_portal
Flask Job Portal  A multi-role web portal built with Flask and SQLite3. Features secure login for Seekers and Employers, a searchable job board, and a resume upload system. Employers can post vacancies, download resumes, and manage application statuses in real-time. Includes custom CSS and a dynamic Jinja2 dashboard.
🚀 Professional Job Portal Web Application
A full-stack web application built with Python, Flask, and SQLite3 that connects job seekers with employers. This platform features a dual-role authentication system, allowing for specialized workflows such as job posting, resume management, and application tracking.

✨ Key Features
👤 For Job Seekers
Secure Authentication: Register and log in as a "Job Seeker."

Dynamic Job Search: Search through listings by job title or location using a real-time search bar.

Resume Uploads: Apply for jobs by uploading resumes in PDF or DOC format (handled via Werkzeug).

Application Tracking: A personal dashboard to monitor the status of applications (Pending, Accepted, or Rejected).

🏢 For Employers
Job Management: Post new job opportunities with detailed descriptions, salary ranges, and company contact emails.

Applicant Management: View a list of all candidates who applied to their specific postings.

Resume Access: Securely download and review candidate resumes directly from the dashboard.

Hiring Workflow: Update application statuses in real-time to notify candidates of hiring decisions.

🛠️ Tech Stack
Backend: Python 3, Flask

Database: SQLite3

Frontend: HTML5, CSS3 (Custom Responsive Design), Jinja2 Templating

File Handling: Secure file uploads and downloads using Flask's static storage.

📂 Project Structure
Plaintext
job_portal/
├── app.py              # Main Flask application & routes
├── database.db         # SQLite database
├── init_db.py          # Database schema initialization script
├── static/
│   ├── css/style.css   # Global styling and layout
│   └── uploads/        # Secure storage for uploaded resumes
└── templates/          # Jinja2 HTML templates (Base, Index, Jobs, etc.)
⚙️ Installation & Setup
Clone the repository:

Bash
git clone https://github.com/your-username/job-portal.git
Initialize the database:

Bash
python init_db.py
Run the application:

Bash
python app.py
Access the portal: Navigate to http://127.0.0.1:5000 in your web browser.
