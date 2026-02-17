# Civic Issue Reporting Platform

## Project Overview
This platform enables citizens to report civic issues online, receive instant AI-powered self-help suggestions, and track the status of their complaints. Authorities can view, manage, and resolve complaints through a dedicated dashboard, improving transparency and efficiency in civic management.

---

## Tech Stack (Detailed)

### Backend
- **Python**: Main programming language for server-side logic.
- **Flask**: Micro web framework used for routing, request handling, and serving HTML templates.
- **google-generativeai (Gemini API)**: Used to generate actionable AI suggestions for citizens based on complaint details.
- **JSON**: Used for persistent storage of complaint data (`issues.json`).
- **uuid**: Generates unique ticket IDs for each complaint.
- **datetime**: Handles date and time for complaint submissions.
- **os**: Manages file paths and image uploads.

### Frontend
- **HTML5**: Structure and content of all web pages.
- **CSS3**: Custom styles for a modern, responsive UI.
- **Bootstrap**: CSS framework for responsive design and UI components.
- **JavaScript**: Handles dynamic UI actions, AJAX requests, and popups.
- **Jinja2 (Flask Templates)**: Renders dynamic content in HTML pages.

### Location Detection (Maps)
- **Manual Entry**: Users enter their location details in the complaint form.
- **(Optional) Geolocation API**: Can be integrated for auto-detecting user location using browser capabilities (not currently implemented).

### Image Upload
- **Flask File Uploads**: Handles multiple image uploads, saves them to `static/uploads/`, and links them to complaints in `issues.json`.

---

## Application Flow & Tech Stack Usage (Step-by-Step)

### 1. Landing Page (`landing.html`)
- **Tech Used**: HTML, CSS, Bootstrap, Flask
- **Purpose**: Entry point for users; links to Citizen and Authority portals.

### 2. Citizen Registration (`citizen_register.html`)
- **Tech Used**: HTML, CSS, Bootstrap, Flask, Jinja2
- **Features**: Form for submitting complaints, manual location entry, image upload, form validation.
- **Backend**: Flask route `/citizen/register` processes form, saves data to `issues.json`, and stores images.
- **Tools**: uuid (ticket ID), datetime (date), os (file management)

### 3. AI Suggestions (Gemini API)
- **Tech Used**: Python, Flask, google-generativeai
- **Features**: After complaint submission, Gemini API generates actionable self-help tips for citizens.
- **Backend**: Flask route `/get_ai_suggestions` calls Gemini API and returns suggestions.

### 4. Confirmation Page (`citizen_confirmation.html`)
- **Tech Used**: HTML, CSS, Bootstrap, JavaScript, Flask, Jinja2
- **Features**: Shows ticket ID, complaint status, AI suggestions, and two action buttons:
  - "Issue Resolved by AI": Updates status to resolved.
  - "Send Complaint to Authorities": Updates status to in progress and shows popup.
- **Backend**: Flask routes `/resolve_by_ai` and `/send_to_authority` handle status updates via AJAX.

### 5. Authority Dashboard (`authority_dashboard_new.html`)
- **Tech Used**: HTML, CSS, Bootstrap, JavaScript, Flask, Jinja2
- **Features**: KPIs (total, pending, in progress, resolved), department breakdown, recent issues.
- **Backend**: Flask route `/authority` loads and analyzes data from `issues.json`.

### 6. Authority Issues & Departments (`authority_issues.html`, `authority_departments.html`)
- **Tech Used**: HTML, CSS, Bootstrap, Flask, Jinja2
- **Features**: List and manage issues, view department workload.
- **Backend**: Flask routes `/authority/issues` and `/authority/departments`.

---

## Key Features & Tools
- **Unique Ticket ID**: Generated using Python's `uuid` for every complaint.
- **Image Upload**: Managed by Flask, images stored in `static/uploads/` and linked in `issues.json`.
- **AI-Powered Suggestions**: Gemini API provides actionable, self-help tips for citizens.
- **Dynamic Status Updates**: Status changes (Pending, In Progress, Resolved) handled via backend and reflected in dashboard KPIs.
- **Authority Dashboard**: Real-time KPIs, department analytics, and recent issues for efficient management.
- **Responsive UI**: Bootstrap ensures mobile-friendly and modern design.
- **Manual Location Entry**: Users provide location details; can be extended to use browser geolocation.

---

## How It Works (Script for Presentation)

1. **Introduction**
   - "Our project is a Civic Issue Reporting Platform designed to empower citizens to report local problems, receive instant AI-powered self-help suggestions, and track the status of their complaints. Authorities can efficiently manage and resolve these complaints through a dedicated dashboard."

2. **Landing Page**
   - "The user starts at the landing page, built with HTML, CSS, and Bootstrap, which provides access to both the Citizen and Authority portals."

3. **Citizen Registration**
   - "On the Citizen Portal, users fill out a registration form to report their issue. The form is built using HTML, Bootstrap, and Jinja2 for dynamic rendering. Users manually enter their location and can upload images related to the complaint. The backend, powered by Flask, processes the form, generates a unique ticket ID using Python's uuid, and saves all data in a JSON file."

4. **AI Suggestions**
   - "After submitting a complaint, the system uses the Gemini API via the google-generativeai Python package to generate actionable self-help suggestions. These are displayed on the confirmation page, helping citizens take immediate steps while waiting for authorities."

5. **Confirmation & Actions**
   - "The confirmation page shows the ticket ID, complaint status, and AI suggestions. Users can mark the issue as resolved by AI or send it to authorities for further action. These actions are handled via AJAX requests to Flask backend routes, which update the complaint status in the JSON file."

6. **Authority Dashboard**
   - "Authorities access their dashboard, which displays KPIs such as total issues, pending, in progress, and resolved counts. The dashboard is built with HTML, Bootstrap, and Jinja2, and the backend aggregates data from the JSON file for analytics."

7. **Issue Management**
   - "Authorities can view detailed lists of issues and department workloads, enabling efficient management and resolution of complaints."

8. **Conclusion**
   - "In summary, our platform leverages Python, Flask, Gemini AI, Bootstrap, and modern web technologies to create a seamless experience for both citizens and authorities, improving civic issue management and community engagement."

---

## Setup Instructions
1. Install Python and required packages:
   ```bash
   pip install flask google-generativeai
   ```
2. Run the Flask app:
   ```bash
   python app_step1.py
   ```
3. Access the app in your browser at `http://localhost:5000`

---

## File Structure
- `app_step1.py`: Main backend logic and routes.
- `issues.json`: Stores all complaints and their statuses.
- `templates/`: Contains all HTML templates for frontend pages.
- `static/uploads/`: Stores uploaded images.

---

## Credits
Developed by Harsh and team.
