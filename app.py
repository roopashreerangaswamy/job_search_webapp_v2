from flask import Flask, render_template, jsonify
app = Flask(__name__)
jobs = [
    {
        "title": "Software Engineer",
        "company": "CodeWorks",
        "location": "Bengaluru",
        "type": "Full-Time"
    },
    {
        "title": "Marketing Analyst",
        "company": "BrightAds",
        "location": "Mumbai",
        "type": "Internship"
    },
    {
        "title": "Graphic Designer",
        "company": "Creatify",
        "location": "Remote",
        "type": "Freelance"
    }
]
@app.route('/') 
def hello_world():
    return render_template('home.html',jobs=jobs)
@app.route('/api/jobs')
def list_jobs():
    return jsonify(jobs)
if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug=True)