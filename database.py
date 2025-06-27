from sqlalchemy import create_engine, text
from sqlalchemy.engine import result
import os

engine = create_engine(os.environ["db_connection_str"])


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    jobs = []
    for row in result.all():
      jobs.append(dict(row._mapping))
  return jobs

def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(
      text(f"SELECT * FROM jobs WHERE id = {id}")
    )
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0]._mapping)

def add_application_to_db(job_id, data):
  with engine.begin() as conn:  # 🔥 THIS auto-commits!
    query = text("""
        INSERT INTO applications (job_id, name, email, linkedin, education, workexp, reason)
        VALUES (:job_id, :name, :email, :linkedin, :education, :workexp, :reason)
    """)
    conn.execute(query, {
        "job_id": job_id,
        "name": data["name"],
        "email": data["email"],
        "linkedin": data["linkedin"],
        "education": data["education"],
        "workexp": data["workexp"],
        "reason": data["reason"]
    })
