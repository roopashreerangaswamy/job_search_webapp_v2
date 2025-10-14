from flask import Flask, render_template, jsonify, request,redirect,flash, session, url_for
from database import load_jobs_from_db , load_job_from_db, add_application_to_db, add_user_to_db, get_user_by_email, add_pending_recruiter_to_db, get_pending_recruiters,update_recruiter_status, is_recruiter_approved
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy.exc
import os


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



@app.route('/job/<id>')
def show_job(id):
    job = load_job_from_db(id)
    if not job:
        return "Not Found", 404
    return render_template('jobpage.html', job=job)



@app.route("/job/<int:id>/apply", methods=["GET", "POST"])
def apply_to_job(id):
    # ✅ Step 1: Check if user is logged in
    if 'user_id' not in session:
        flash("Please log in to apply for jobs.", "warning")
        return redirect('/login')

    job = load_job_from_db(id)
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
        add_application_to_db(id, application_data)
        return render_template("application_submitted.html", application=application_data, job=job)

    # ✅ Step 3: Show form if GET request
    return render_template("application_form.html", job=job)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role']  # ✅ Fix here
            flash('Login successful!', 'success')
            if session['role'] == 'recruiter':
                return redirect('/recruiter/dashboard')
            else:
                return redirect('/')

            
        else:
            flash('Invalid credentials. Please try again.', 'danger')
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



@app.route('/recruiter_dashboard')
def recruiter_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if not is_recruiter_approved(user_id):
        return render_template('recruiter_pending.html')

    # ✅ Continue loading recruiter dashboard
    return render_template('recruiter_dashboard.html')



@app.route('/recruiter_pending')
def recruiter_pending():
    return render_template('recruiter_pending.html')


@app.route('/admin_recruiters')
def admin_recruiters():
    recruiters = get_pending_recruiters()
    return render_template("admin_recruiters.html", recruiters=recruiters)

@app.route('/admin/recruiters/<int:recruiter_id>/<string:action>')
def recruiter_action(recruiter_id, action):
    if action in ["approved", "rejected"]:
        update_recruiter_status(recruiter_id, action)
    return redirect(url_for('admin_recruiters'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
