from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# Replace with your actual MongoDB URI
MONGO_URI = os.environ.get('db_connection_str')

client = MongoClient(MONGO_URI)
db = client["hirebridge"]

# ---------------------- JOB FUNCTIONS ----------------------

def load_jobs_from_db():
    jobs = list(db.jobs.find({}, {"_id": 0}))  # exclude _id for clean output
    return jobs


def load_job_from_db(id):
    job = db.jobs.find_one({"id": int(id)}, {"_id": 0})
    return job


def add_application_to_db(job_id, data):
    data["job_id"] = int(job_id)
    db.applications.insert_one(data)

# ---------------------- USER FUNCTIONS ----------------------

def add_user_to_db(name, email, hashed_password):
    db.users.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    })


def get_user_by_email(email):
    user = db.users.find_one({"email": email}, {"_id": 0})
    return user

# ---------------------- RECRUITER FUNCTIONS ----------------------

def add_pending_recruiter_to_db(name, email, hashed_password, company_name):
    # Step 1: Add user
    user = {
        "name": name,
        "email": email,
        "password": hashed_password
    }
    result = db.users.insert_one(user)
    user_id = result.inserted_id  # MongoDB's ObjectId

    # Step 2: Add recruiter with pending status
    recruiter = {
        "user_id": user_id,
        "company_name": company_name,
        "status": "pending"
    }
    db.recruiters.insert_one(recruiter)


def get_pending_recruiters():
    recruiters = db.recruiters.aggregate([
        {
            "$match": {"status": "pending"}
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user_info"
            }
        },
        {
            "$unwind": "$user_info"
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "name": "$user_info.name",
                "email": "$user_info.email",
                "company_name": 1
            }
        }
    ])
    return list(recruiters)


def update_recruiter_status(recruiter_id, new_status):
    db.recruiters.update_one(
        {"_id": ObjectId(recruiter_id)},
        {"$set": {"status": new_status}}
    )


def is_recruiter_approved(user_id):
    recruiter = db.recruiters.find_one({"user_id": ObjectId(user_id)})
    return recruiter and recruiter["status"] == "approved"
