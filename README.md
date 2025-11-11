# 💼 JobFinder – Flask-Based Careers Website (v2.0)

A full-stack web application that connects recruiters and job seekers — enabling recruiters to post jobs (after admin approval) and candidates to browse, apply, and manage applications.

---

## 🌐 Live Demo

👉 [View the deployed site on Render](https://job-search-webapp-v2.onrender.com/)

---

## 🚀 Key Features

### 👩‍💻 For Candidates
- 🔍 **View All Job Listings** — dynamically loaded from the database  
- 📄 **Detailed Job Pages** — title, location, salary, company, and requirements  
- 📝 **Apply to Jobs** — via an interactive application form  
- 💾 **Applications Stored Securely** in MongoDB  
- 📨 **View Application Status** (Approved/Rejected by Recruiter)

---

### 🧑‍💼 For Recruiters
- 🏢 **Recruiter Signup & Login** — secure registration with company details  
- 🧾 **Post Job Listings** — create and manage openings easily  
- ✏️ **Edit / Delete Jobs** — maintain listings dynamically  
- ⏳ **Admin Approval System** — recruiters must be approved by the admin before posting jobs  
- 📬 **View Applications Received** — see who applied to your posted jobs  

---

### 🧑‍💻 For Admin
- ✅ **Approve / Reject Recruiters** before they gain access  
- 🗂️ **Monitor Job Postings & Applications**  
- 🧹 **Delete Recruiters / Jobs / Applications** as needed  

---

## 🛠️ Tech Stack

| Layer      | Technology        |
|-------------|-------------------|
| Backend     | Python (Flask)    |
| Frontend    | HTML, CSS, Bootstrap 5 |
| Database    | MongoDB (Atlas)   |
| Authentication | Flask Sessions |
| Deployment  | Render            |

---

## 🗂️ Project Structure

```
jobfinder/
├── app.py                       # Main Flask app & routes
├── database.py                  # MongoDB connection and operations
├── templates/                   # Jinja2 templates
│   ├── home.html
│   ├── jobpage.html
│   ├── recruiter_register.html
│   ├── recruiter_dashboard.html
│   ├── admin_dashboard.html
│   ├── application_form.html
│   └── application_submitted.html
├── static/                      # CSS, images, JS files
│   └── style.css
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

### 🏠 Home Page (Jobs for Candidates)
```python
@app.route("/")
def home():
    jobs = jobs_collection.find({})
    return render_template("home.html", jobs=jobs)
```

### 💼 Recruiter Registration
```python
@app.route("/recruiter/register", methods=["GET", "POST"])
def recruiter_register():
    if request.method == "POST":
        recruiters_collection.insert_one({...})
```

### 🔑 Admin Approval Flow
```python
@app.route("/admin/approve/<id>")
def approve_recruiter(id):
    recruiters_collection.update_one({"_id": ObjectId(id)}, {"$set": {"approved": True}})
```

### 🗑️ Job Deletion
```python
@app.route("/delete_job/<id>")
def delete_job(id):
    jobs_collection.delete_one({"_id": ObjectId(id)})
```

---

## ✅ Current Status

- [x] Job listings & details  
- [x] Application form (MongoDB integrated)  
- [x] Recruiter registration & login  
- [x] Admin approval flow  
- [x] Job posting + deletion  
- [x] Deployed on Render  

---

## 🧩 Upcoming Enhancements

- 📎 Resume upload & download feature  
- 🔍 Search & filter jobs by location or type  
- ✉️ Email notifications (on approval/application)  
- 📊 Recruiter analytics dashboard  

---

## 👩‍💻 Built With

Flask • MongoDB • Bootstrap 5 • Render • ❤️ and sleepless debugging nights

---

## 📬 Contact

**Roopashree R**  
📧 [roopashree.r2004@gmail.com](mailto:roopashree.r2004@gmail.com)  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/roopashree-r-66848b286)

---
