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
