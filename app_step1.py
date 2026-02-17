from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime
import uuid
import google.generativeai as genai
import requests

app = Flask(__name__)

@app.route('/get_ai_suggestions')
def get_ai_suggestions():
    ticket_id = request.args.get('ticket_id')
    lang = request.args.get('lang', 'en')
    issues_file = 'issues.json'
    issue = None
    if os.path.exists(issues_file):
        with open(issues_file, 'r') as f:
            issues = json.load(f)
            for i in issues:
                if i.get('ticket_id') == ticket_id:
                    issue = i
                    break
    if not issue:
        return jsonify({'suggestions': ['No complaint found.']})
    genai_api_key = "AIzaSyD7lGUGs-5S0BuFUVHXZFeO2uR9OdaICJQ"
    genai.configure(api_key=genai_api_key)
    if lang == 'hi':
        system_prompt = "आप एक नागरिक समस्या सहायक हैं। केवल वर्तमान शिकायत के विवरण के आधार पर सुझाव दें। सभी सुझाव हिंदी में दें।"
    else:
        system_prompt = "You are a civic issue assistant. Only provide suggestions based on the current complaint details. All suggestions should be in English."
    user_content = f"Complaint details: {json.dumps(issue)}"
    ai_suggestions = []
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content([
            system_prompt,
            user_content
        ])
        if hasattr(response, 'text'):
            ai_suggestions = [s.strip() for s in response.text.split('\n') if s.strip()]
    except Exception as e:
        ai_suggestions = ["AI suggestion unavailable."]
    return jsonify({'suggestions': ai_suggestions})

@app.route('/resolve_by_ai', methods=['POST'])
def resolve_by_ai():
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    issues_file = 'issues.json'
    updated = False
    if os.path.exists(issues_file):
        with open(issues_file, 'r') as f:
            issues = json.load(f)
        for issue in issues:
            if issue.get('ticket_id') == ticket_id and issue.get('status', 'Pending') != 'Resolved':
                issue['status'] = 'Resolved'
                updated = True
                break
        if updated:
            with open(issues_file, 'w') as f:
                json.dump(issues, f, indent=2)
    return jsonify({'success': updated})

@app.route('/send_to_authority', methods=['POST'])
def send_to_authority():
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    issues_file = 'issues.json'
    updated = False
    if os.path.exists(issues_file):
        with open(issues_file, 'r') as f:
            issues = json.load(f)
        for issue in issues:
            if issue.get('ticket_id') == ticket_id and issue.get('status', 'Pending'):
                issue['status'] = 'In Progress'
                updated = True
                break
        if updated:
            with open(issues_file, 'w') as f:
                json.dump(issues, f, indent=2)
    # Here you could add logic to notify authorities, for now just return success
    return jsonify({'success': updated})

@app.route('/')
def landing():
    return render_template('landing.html')

# Citizen Portal
@app.route('/citizen')
def citizen_portal():
    return render_template('citizen_login.html')

@app.route('/citizen/login', methods=['GET', 'POST'])
def citizen_login():
    return render_template('citizen_login.html')

@app.route('/citizen/register', methods=['GET', 'POST'])
def citizen_register():
    if request.method == 'POST':
        ticket_id = str(uuid.uuid4())
        issue = {
            'ticket_id': ticket_id,
            'full_name': request.form.get('full_name'),
            'aadhaar': request.form.get('aadhaar'),
            'mobile': request.form.get('mobile'),
            'address': request.form.get('address'),
            'pincode': request.form.get('pincode'),
            'description': request.form.get('description'),
            'category': request.form.get('category'),
            'location': request.form.get('location'),
            'urgency': request.form.get('urgency'),
            'date': datetime.now().strftime('%d-%m-%Y'),
        }
        # Handle image uploads
        image_paths = []
        if 'photos' in request.files:
            photos = request.files.getlist('photos')
            upload_folder = os.path.join('static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            for idx, photo in enumerate(photos):
                if photo and photo.filename:
                    ext = os.path.splitext(photo.filename)[1]
                    filename = f"{ticket_id}_{idx}{ext}"
                    save_path = os.path.join(upload_folder, filename)
                    photo.save(save_path)
                    image_paths.append(save_path)
        issue['images'] = image_paths
        issues_file = 'issues.json'
        if os.path.exists(issues_file):
            with open(issues_file, 'r') as f:
                issues = json.load(f)
        else:
            issues = []
        issues.append(issue)
        with open(issues_file, 'w') as f:
            json.dump(issues, f, indent=2)

        # Gemini API integration for AI suggestions using google-generativeai
        genai_api_key = "AIzaSyD7lGUGs-5S0BuFUVHXZFeO2uR9OdaICJQ"
        genai.configure(api_key=genai_api_key)
        system_prompt = "You are a civic issue assistant. Only provide actionable suggestions that the citizen and their neighbors can do themselves to mitigate or temporarily resolve the reported issue, based on the current complaint details. Do not suggest contacting authorities or departments unless absolutely necessary."
        user_content = f"Complaint details: {json.dumps(issue)}"
        ai_suggestions = []
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content([
                system_prompt,
                user_content
            ])
            if hasattr(response, 'text'):
                # Split into bullet points if possible
                ai_suggestions = [s.strip() for s in response.text.split('\n') if s.strip()]
        except Exception as e:
            ai_suggestions = ["AI suggestion unavailable."]

        return render_template('citizen_confirmation.html', ticket_id=issue['ticket_id'], ai_suggestions=ai_suggestions)
    else:
        return render_template('citizen_register.html')

@app.route('/citizen/confirmation')
def citizen_confirmation():
    # This route is now only used for GET, POST handles AI suggestions
    ticket_id = request.args.get('ticket_id')
    return render_template('citizen_confirmation.html', ticket_id=ticket_id)

# Authority Portal with subportals
@app.route('/authority')
def authority_dashboard():
    issues = []
    try:
        with open('issues.json', 'r') as f:
            issues = json.load(f)
    except Exception:
        pass
    # Calculate KPIs
    total_issues = len(issues)
    pending = sum(1 for i in issues if i.get('status', 'Pending') == 'Pending')
    in_progress = sum(1 for i in issues if i.get('status', 'Pending') == 'In Progress')
    resolved = sum(1 for i in issues if i.get('status', 'Pending') == 'Resolved')
    # Department breakdown
    dept_counts = {}
    for i in issues:
        dept = i.get('category', 'Other')
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    return render_template('authority_dashboard_new.html', issues=issues, total_issues=total_issues, pending=pending, in_progress=in_progress, resolved=resolved, dept_counts=dept_counts)

@app.route('/authority/issues')
def authority_issues():
    issues = []
    try:
        with open('issues.json', 'r') as f:
            issues = json.load(f)
    except Exception:
        pass
    return render_template('authority_issues.html', issues=issues)

@app.route('/authority/departments')
def authority_departments():
    return render_template('authority_departments.html')


if __name__ == '__main__':
    app.run(debug=True)
@app.route('/resolve_by_ai', methods=['POST'])
def resolve_by_ai():
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    issues_file = 'issues.json'
    updated = False
    if os.path.exists(issues_file):
        with open(issues_file, 'r') as f:
            issues = json.load(f)
        for issue in issues:
            if issue.get('ticket_id') == ticket_id and issue.get('status', 'Pending') != 'Resolved':
                issue['status'] = 'Resolved'
                updated = True
                break
        if updated:
            with open(issues_file, 'w') as f:
                json.dump(issues, f, indent=2)
    return jsonify({'success': updated})

@app.route('/send_to_authority', methods=['POST'])
def send_to_authority():
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    # Here you could add logic to notify authorities, for now just return success
    return jsonify({'success': True})

from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime
import uuid
import google.generativeai as genai
import requests

app = Flask(__name__)

@app.route('/get_ai_suggestions')
def get_ai_suggestions():
    ticket_id = request.args.get('ticket_id')
    lang = request.args.get('lang', 'en')
    issues_file = 'issues.json'
    issue = None
    if os.path.exists(issues_file):
        with open(issues_file, 'r') as f:
            issues = json.load(f)
            for i in issues:
                if i.get('ticket_id') == ticket_id:
                    issue = i
                    break
    if not issue:
        return jsonify({'suggestions': ['No complaint found.']})
    genai_api_key = "AIzaSyD7lGUGs-5S0BuFUVHXZFeO2uR9OdaICJQ"
    genai.configure(api_key=genai_api_key)
    if lang == 'hi':
        system_prompt = "आप एक नागरिक समस्या सहायक हैं। केवल वर्तमान शिकायत के विवरण के आधार पर सुझाव दें। सभी सुझाव हिंदी में दें।"
    else:
        system_prompt = "You are a civic issue assistant. Only provide suggestions based on the current complaint details. All suggestions should be in English."
    user_content = f"Complaint details: {json.dumps(issue)}"
    ai_suggestions = []
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content([
            system_prompt,
            user_content
        ])
        if hasattr(response, 'text'):
            ai_suggestions = [s.strip() for s in response.text.split('\n') if s.strip()]
    except Exception as e:
        ai_suggestions = ["AI suggestion unavailable."]
    return jsonify({'suggestions': ai_suggestions})
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime
import uuid
import google.generativeai as genai
import requests

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing.html')

# Citizen Portal
@app.route('/citizen')
def citizen_portal():
    return render_template('citizen_login.html')

@app.route('/citizen/login', methods=['GET', 'POST'])
def citizen_login():
    return render_template('citizen_login.html')

@app.route('/citizen/register', methods=['GET', 'POST'])
def citizen_register():
    if request.method == 'POST':
        ticket_id = str(uuid.uuid4())
        issue = {
            'ticket_id': ticket_id,
            'full_name': request.form.get('full_name'),
            'aadhaar': request.form.get('aadhaar'),
            'mobile': request.form.get('mobile'),
            'address': request.form.get('address'),
            'pincode': request.form.get('pincode'),
            'description': request.form.get('description'),
            'category': request.form.get('category'),
            'location': request.form.get('location'),
            'urgency': request.form.get('urgency'),
            'date': datetime.now().strftime('%d-%m-%Y'),
        }
        # Handle image uploads
        image_paths = []
        if 'photos' in request.files:
            photos = request.files.getlist('photos')
            upload_folder = os.path.join('static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            for idx, photo in enumerate(photos):
                if photo and photo.filename:
                    ext = os.path.splitext(photo.filename)[1]
                    filename = f"{ticket_id}_{idx}{ext}"
                    save_path = os.path.join(upload_folder, filename)
                    photo.save(save_path)
                    image_paths.append(save_path)
        issue['images'] = image_paths
        issues_file = 'issues.json'
        if os.path.exists(issues_file):
            with open(issues_file, 'r') as f:
                issues = json.load(f)
        else:
            issues = []
        issues.append(issue)
        with open(issues_file, 'w') as f:
            json.dump(issues, f, indent=2)

        # Gemini API integration for AI suggestions using google-generativeai
        genai_api_key = "AIzaSyD7lGUGs-5S0BuFUVHXZFeO2uR9OdaICJQ"
        genai.configure(api_key=genai_api_key)
        system_prompt = "You are a civic issue assistant. Only provide actionable suggestions that the citizen and their neighbors can do themselves to mitigate or temporarily resolve the reported issue, based on the current complaint details. Do not suggest contacting authorities or departments unless absolutely necessary."
        user_content = f"Complaint details: {json.dumps(issue)}"
        ai_suggestions = []
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content([
                system_prompt,
                user_content
            ])
            if hasattr(response, 'text'):
                # Split into bullet points if possible
                ai_suggestions = [s.strip() for s in response.text.split('\n') if s.strip()]
        except Exception as e:
            ai_suggestions = ["AI suggestion unavailable."]

        return render_template('citizen_confirmation.html', ticket_id=issue['ticket_id'], ai_suggestions=ai_suggestions)
    else:
        return render_template('citizen_register.html')

@app.route('/citizen/confirmation')
def citizen_confirmation():
    # This route is now only used for GET, POST handles AI suggestions
    ticket_id = request.args.get('ticket_id')
    return render_template('citizen_confirmation.html', ticket_id=ticket_id)

# Authority Portal with subportals
@app.route('/authority')
def authority_dashboard():
    issues = []
    try:
        with open('issues.json', 'r') as f:
            issues = json.load(f)
    except Exception:
        pass
    # Calculate KPIs
    total_issues = len(issues)
    pending = sum(1 for i in issues if i.get('status', 'Pending') == 'Pending')
    in_progress = sum(1 for i in issues if i.get('status', 'Pending') == 'In Progress')
    resolved = sum(1 for i in issues if i.get('status', 'Pending') == 'Resolved')
    # Department breakdown
    dept_counts = {}
    for i in issues:
        dept = i.get('category', 'Other')
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    return render_template('authority_dashboard_new.html', issues=issues, total_issues=total_issues, pending=pending, in_progress=in_progress, resolved=resolved, dept_counts=dept_counts)

@app.route('/authority/issues')
def authority_issues():
    issues = []
    try:
        with open('issues.json', 'r') as f:
            issues = json.load(f)
    except Exception:
        pass
    return render_template('authority_issues.html', issues=issues)

@app.route('/authority/departments')
def authority_departments():
    return render_template('authority_departments.html')


if __name__ == '__main__':
    app.run(debug=True)
