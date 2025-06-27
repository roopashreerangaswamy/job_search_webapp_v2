
# 💼 JobFinder – Flask-Based Careers Website

A full-stack web application that allows companies to post job listings and users to view job details and apply directly via an application form.

---

## 🚀 Features

- 🔍 View all job openings with dynamic pages
- 📄 See detailed job descriptions (title, location, salary, etc.)
- 📝 Apply to any job via a structured application form
- 💾 Store applications in a MySQL database
- 📦 Backend built with Python & Flask
- 🎨 Frontend styled with Bootstrap 5
- ✅ Fully dynamic, database-connected website

---

## 🛠️ Tech Stack

| Layer      | Technology        |
|------------|-------------------|
| Backend    | Python, Flask     |
| Frontend   | HTML, CSS, Bootstrap |
| Database   | MySQL             |
| ORM        | SQLAlchemy (text-based) |
| Deployment | Replit / Railway / Render (optional) |

---

## 🗂️ Project Structure

```
jobfinder/
├── app.py                # Main Flask app with route handling
├── database.py           # DB interaction logic (jobs & applications)
├── templates/            # HTML templates (Jinja2)
│   ├── home.html
│   ├── jobpage.html
│   ├── application_form.html
│   ├── application_submitted.html
│   ├── nav.html
│   └── footer.html
├── static/               # Images, CSS, other static assets
│   └── banner.jpg
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---



## 🧠 How It Works

### 🔗 View Jobs
```python
@app.route("/")
def home():
    jobs = load_jobs_from_db()
    return render_template("home.html", jobs=jobs)
```

### 📄 View Single Job
```python
@app.route("/job/<int:id>")
def job_detail(id):
    job = load_job_from_db(id)
    return render_template("jobpage.html", job=job)
```

### ✍️ Apply to a Job
```python
@app.route("/job/<int:id>/apply", methods=["GET", "POST"])
def apply_to_job(id):
    if request.method == "POST":
        # Save application to DB
```

---

## 🧪 Sample SQL Tables

### `jobs` Table
```sql
CREATE TABLE jobs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(250),
  location VARCHAR(250),
  salary INT,
  currency VARCHAR(10),
  company VARCHAR(100),
  job_type VARCHAR(50),
  responsibilities TEXT,
  requirements TEXT
);
```

### `applications` Table
```sql
CREATE TABLE applications (
  id INT AUTO_INCREMENT PRIMARY KEY,
  job_id INT,
  name VARCHAR(100),
  email VARCHAR(100),
  linkedin VARCHAR(200),
  education TEXT,
  workexp TEXT,
  reason TEXT
);
```

---

## ✅ Status

- [x] Job listings
- [x] Job detail pages
- [x] Application form (with validation)
- [x] Store applications in MySQL
- [x] Clean UI with Bootstrap

---

## 🧩 Future Improvements

- Admin dashboard to view all applications
- Resume file upload support
- Authentication for employers/applicants
- Email confirmation on application
- Add search & filter by location/job type

---

## 👩‍💻 Made With

Flask, MySQL, Bootstrap, and a **lot of 💪 learning!**

---

## 📬 Contact

Built by **Roopashree.R**  
📧 roopashree.r2004@gmail.com  
🌐 [https://www.linkedin.com/in/roopashree-r-66848b286?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app]

---
