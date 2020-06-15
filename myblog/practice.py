from myblog import db, bcrypt, testing_myblog, create_myblog
import psycopg2
import sqlalchemy
import os

app = testing_myblog()
with app.app_context():
    db.drop_all()
    db.create_all()
    db.drop_all()
    # db.create_all()
    # engine = sqlalchemy.create_engine('postgresql://postgres:PythonIsBest4169@localhost:5432')
    # conn = engine.connect()
    # conn.execute("commit")
    # conn.execute(f"create database testing" )
    # conn.close()

