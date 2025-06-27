from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db , load_job_from_db, add_application_to_db

app = Flask(__name__)





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
    job = load_job_from_db(id)

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

    return render_template("application_form.html", job=job)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
