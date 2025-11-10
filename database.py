from pymongo import MongoClient
from bson.objectid import ObjectId
import os

MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client["hirebridge"]

# ---------------------- JOB FUNCTIONS ----------------------

def load_jobs_from_db():
    return list(db.jobs.find({}, {"_id": 0}))

def load_job_from_db(id):
    return db.jobs.find_one({"id": int(id)}, {"_id": 0})

def add_application_to_db(job_id, data):
    data["job_id"] = int(job_id)
    db.applications.insert_one(data)

# ---------------------- USER FUNCTIONS ----------------------

def add_user_to_db(name, email, hashed_password):
    db.users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": "user"
    })
    

def get_user_by_email(email):
    user = db.users.find_one({"email": email})
    if user:
        user['id'] = str(user['_id'])
    return user


# ---------------------- RECRUITER FUNCTIONS ----------------------

def add_pending_recruiter_to_db(name, email, hashed_password, company_name):
    recruiter = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "company_name": company_name,
        "status": "pending",
        "jobs_posted": [],
        "role": "recruiter"
    }
    db.recruiters.insert_one(recruiter)

def get_recruiter_by_email(email):
    recruiter = db.recruiters.find_one({"email": email})
    if recruiter:
        # Normalize keys for consistency
        recruiter['user_id'] = recruiter['_id']
        recruiter['name'] = recruiter.get('name', '')
        recruiter['status'] = recruiter.get('status', 'pending')
    return recruiter


def get_pending_recruiters():
    recruiters = list(db.recruiters.find(
        {"status": "pending"},
        {"_id": {"$toString": "$_id"}, "name": 1, "email": 1, "company_name": 1}
    ))
    return recruiters

def update_recruiter_status(recruiter_id, new_status):
    db.recruiters.update_one({"_id": ObjectId(recruiter_id)}, {"$set": {"status": new_status}})

def is_recruiter_approved(email):
    recruiter = db.recruiters.find_one({"email": email})
    return recruiter and recruiter["status"] == "approved"
