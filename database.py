import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sushanth6688",
    database="interview_platform"
)

cursor = db.cursor()

print("Database Connected Successfully")