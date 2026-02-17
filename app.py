
from flask import Flask, render_template, request, redirect, url_for


import json
import os
app = Flask(__name__)

# Landing page with three portal options
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
        # Collect form data
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
        }
        # Save to issues.json
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


# Authority Portal
@app.route('/authority')
def authority_portal():
    issues = []
    try:
        with open('issues.json', 'r') as f:
            issues = json.load(f)
    except Exception:
        pass
    return render_template('authority.html', issues=issues)

# Worker Portal
@app.route('/worker')
def worker_portal():
    return render_template('worker.html')

if __name__ == '__main__':
    app.run(debug=True)
