import psycopg2
import asyncio
from models import JobListing

def connectToDatabase():
    return psycopg2.connect(host="localhost", database="listings", user="albertoortiz", password="")

def insertJob(job:JobListing):
    conn = connectToDatabase()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs VALUES (%s)", job.getValuesString())
    cursor.close()
    conn.close()

def insertJobs(jobs):
    conn = connectToDatabase()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs VALUES %s", __getValuesList(jobs))
    cursor.close()
    conn.close()

def __getValuesList(jobs):
    stringResult = ""
    for job in jobs:
        stringResult += "(%s),", job.getValuesString()
    return stringResult[:-1]

