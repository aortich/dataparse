import psycopg2
import asyncio
from models import JobListing

async def insertJobListing(job:JobListing):
    conn = psycopg2.connect(host="localhost", database="listings", user="albertoortiz", password="")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs VALUES (%s)", job.getValuesString())
    cursor.close()
    conn.close()
    

