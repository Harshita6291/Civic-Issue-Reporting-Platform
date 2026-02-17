from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from collections import Counter

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
        issue = {
            'full_name': request.form.get('full_name'),
            'aadhaar': request.form.get('aadhaar'),
            'mobile': request.form.get('mobile'),
            'address': request.form.get('address'),
            'pincode': request.form.get('pincode'),
            'description': request.form.get('description'),
            'category': request.form.get('category'),
            'location': request.form.get('location'),
            'urgency': request.form.get('urgency'),
            'status': 'Pending', # Default status
        }
        issues_file = 'issues.json'
        if os.path.exists(issues_file):
            with open(issues_file, 'r') as f:
                issues = json.load(f)
        else:
            issues = []
        issues.append(issue)
        with open(issues_file, 'w') as f:
            json.dump(issues, f, indent=2)
        return redirect(url_for('citizen_confirmation'))
    return render_template('citizen_register.html')

@app.route('/citizen/confirmation')
def citizen_confirmation():
    return render_template('citizen_confirmation.html')

# Authority Portal with subportals
@app.route('/authority')
def authority_dashboard():
    issues = []
    try:
        with open('issues.json', 'r') as f:
            issues = json.load(f)
    except Exception:
        pass
    # KPIs
    total_issues = len(issues)
    pending = sum(1 for i in issues if i.get('status') == 'Pending')
    in_progress = sum(1 for i in issues if i.get('status') == 'In Progress')
    resolved = sum(1 for i in issues if i.get('status') == 'Resolved')
    # Department breakdown
    dept_counts = Counter(i.get('category') for i in issues)
    # Workload (same as department breakdown for now)
    return render_template('authority_dashboard.html', issues=issues, total_issues=total_issues, pending=pending, in_progress=in_progress, resolved=resolved, dept_counts=dept_counts)

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

# Worker Portal
@app.route('/worker')
def worker_portal():
    return render_template('worker.html')

if __name__ == '__main__':
    app.run(debug=True)
