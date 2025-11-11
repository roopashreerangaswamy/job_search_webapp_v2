from flask import Flask, render_template, jsonify, request,redirect,flash, session, url_for
from database import db,load_jobs_from_db , load_job_from_db, add_application_to_db, add_user_to_db, get_user_by_email, add_pending_recruiter_to_db, add_job_to_db,get_jobs_by_recruiter, delete_job, get_applications_for_job
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy.exc
import os
from bson.objectid import ObjectId

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")




@app.route('/')
def hello_world():
    jobs = load_jobs_from_db()
    return render_template('home.html', jobs=jobs)


@app.route('/api/jobs')
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)





@app.route("/job/<job_id>/apply", methods=["GET", "POST"])
def apply_to_job(job_id):
    # ✅ Step 1: Check if user is logged in
    if 'user_id' not in session:
        flash("Please log in to apply for jobs.", "warning")
        return redirect('/login')

    job = load_job_from_db(job_id)
    if not job:
        return "Job not found", 404

    # ✅ Step 2: Handle POST request (form submission)
    if request.method == "POST":
        application_data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "linkedin": request.form.get("linkedin"),
            "education": request.form.get("education"),
            "workexp": request.form.get("workexp"),
            "reason": request.form["reason"],
        }
        add_application_to_db(job_id, application_data)
        return render_template("application_submitted.html", application=application_data, job=job)

    # ✅ Step 3: Show form if GET request
    return render_template("application_form.html", job=job)



@app.route('/job/<id>')
def show_job(id):
    job = load_job_from_db(id)
    if not job:
        return "Not Found", 404
    return render_template('jobpage.html', job=job)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # 🚨 Check for empty fields
        if not email or not password:
            flash('Please enter both email and password.', 'danger')
            return redirect('/login')

        user = get_user_by_email(email)

        # 🚨 Check if user exists and password matches
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user.get('_id', ''))
            session['user_name'] = user.get('name', 'User')
            session['role'] = user.get('role', 'user')

            flash('Login successful!', 'success')

            # ✅ Redirect based on role
            if session['role'] == 'recruiter':
                return redirect('/recruiter/dashboard')
            elif session['role'] == 'admin':
                return redirect('/admin/dashboard')
            else:
                return redirect('/')
        else:
            flash('Invalid email or password.', 'danger')
            return redirect('/login')

    return render_template('login.html')

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        try:
            add_user_to_db(name, email, password)
            flash("Registered successfully!", "success")
            return redirect('/')
        except sqlalchemy.exc.IntegrityError:
            flash("Email already exists!", "danger")
            return redirect('/register')

    return render_template('register.html')


@app.route('/for_recruiters')
def for_recruiters():
    return render_template('for_recruiters.html')



@app.route('/recruiter_register', methods=['GET', 'POST'])
def recruiter_register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            company_name = request.form['company']  # Make sure this matches your form field

            hashed_pw = generate_password_hash(password)

            add_pending_recruiter_to_db(name, email, hashed_pw, company_name)
            return redirect(url_for('recruiter_pending'))
# simple “wait for approval” page

        except sqlalchemy.exc.IntegrityError:
            return "Email already exists. Please use a different one.", 400

        except KeyError as e:
            return f"Missing form field: {str(e)}", 400

        except Exception as e:
            return f"An unexpected error occurred: {str(e)}", 500

    return render_template('recruiter_register.html')


@app.route('/recruiter_login', methods=['GET', 'POST'])
def recruiter_login():
    error = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print("--- DEBUG recruiter_login ---")
        print(f"Email entered: {email}")
        print(f"Password entered: {bool(password)}")

        recruiter = db.recruiters.find_one({"email": email})
        print(f"Recruiter fetched from DB: {recruiter}")

        if recruiter:
            if check_password_hash(recruiter['password'], password or ""):
                if recruiter.get('status') == 'approved':
                    session['recruiter_email'] = recruiter['email']
                    session['recruiter_name'] = recruiter['name']
                    session['role'] = 'recruiter'
                    session['recruiter_status'] = "approved"
                    return redirect('/recruiter_dashboard')
                else:
                    return render_template('recruiter_pending.html', recruiter=recruiter)  
            else:
                error = "❌ Invalid password. Please try again."
        else:
            error = "⚠️ Recruiter not found. Please check your email."


    return render_template('recruiter_login.html', error=error)



@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        admin = db.admins.find_one({"email": email})
        if admin and check_password_hash(admin['password'], password or ""):
            session['admin_email'] = admin['email']
            session['admin_name'] = admin.get('name', 'Admin')
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid credentials."
    return render_template('admin_login.html', error=error)


if not db.admins.find_one({"email": "admin@hirebridge.com"}):
    hashed = generate_password_hash("admin123")
    db.admins.insert_one({
        "name": "Super Admin",
        "email": "admin@hirebridge.com",
        "password": hashed
    })
    print("✅ Admin account created: admin@hirebridge.com / admin123")




@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin_email' not in session:
        return redirect(url_for('admin_login'))
    pending_recruiters = list(db.recruiters.find({"status": "pending"}))
    return render_template('admin_dashboard.html', recruiters=pending_recruiters)



@app.route('/approve_recruiter/<recruiter_id>', methods=['POST'])
def approve_recruiter(recruiter_id):
    if 'admin_email' not in session:
        return redirect(url_for('admin_login'))
    db.recruiters.update_one({"_id": ObjectId(recruiter_id)}, {"$set": {"status": "approved"}})
    flash("Recruiter approved.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/reject_recruiter/<recruiter_id>', methods=['POST'])
def reject_recruiter(recruiter_id):
    if 'admin_email' not in session:
        return redirect(url_for('admin_login'))
    db.recruiters.update_one({"_id": ObjectId(recruiter_id)}, {"$set": {"status": "rejected"}})
    flash("Recruiter rejected.", "danger")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_email', None)
    session.pop('admin_name', None)
    flash("Admin logged out.", "info")
    return redirect(url_for('admin_login'))



@app.route('/recruiter_dashboard')
def recruiter_dashboard():
    if session.get('role') != 'recruiter' or session.get('recruiter_status') != 'approved':
        flash("Access denied. Only approved recruiters can view this page.", "danger")
        return redirect(url_for('recruiter_login'))

    recruiter_email = session.get('recruiter_email')
    jobs = get_jobs_by_recruiter(recruiter_email)

    # ✅ Convert ObjectId to string for template rendering
    for job in jobs:
        job['_id'] = str(job['_id'])

    return render_template('recruiter_dashboard.html', jobs=jobs)



# ---------------------- RECRUITER DASHBOARD ACTIONS ----------------------

@app.route('/recruiter/add_job', methods=['POST'])
def add_job():
    if session.get('role') != 'recruiter' or session.get('recruiter_status') != 'approved':
        flash("Access denied.", "danger")
        return redirect(url_for('recruiter_login'))

    title = request.form['title']
    location = request.form['location']
    salary = request.form['salary']
    description = request.form['description']

    add_job_to_db(session['recruiter_email'], title, location, salary, description)
    flash("Job added successfully!", "success")
    return redirect(url_for('recruiter_dashboard'))


@app.route('/recruiter/delete_job/<job_id>', methods=['POST'])
def delete_job_route(job_id):
    if session.get('role') != 'recruiter' or session.get('recruiter_status') != 'approved':
        flash("Access denied.", "danger")
        return redirect(url_for('recruiter_login'))

    delete_job(job_id, session['recruiter_email'])
    flash("Job deleted successfully!", "info")
    return redirect(url_for('recruiter_dashboard'))


@app.route('/recruiter/view_applications/<job_id>')
def view_applications(job_id):
    if session.get('role') != 'recruiter' or session.get('recruiter_status') != 'approved':
        flash("Access denied.", "danger")
        return redirect(url_for('recruiter_login'))

    # ✅ Fetch job details
    job = db.jobs.find_one({"_id": ObjectId(job_id)})  # or {"id": int(job_id)} if you use integers
    applications = get_applications_for_job(job_id)

    return render_template('recruiter_applications.html', job=job, applications=applications)




@app.route('/recruiter_pending')
def recruiter_pending():
    return render_template('recruiter_pending.html')





@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
