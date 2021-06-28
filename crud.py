import os
# DB_NAME=os.getenv('DB_NAME')
# DB_USER=os.getenv('DB_USER')
# DB_PASS=os.getenv('DB_PASS')

DB_NAME='test'
DB_USER='postgres'
DB_PASS='admin123'
import psycopg2
conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host='localhost')
cursor=conn.cursor()
def create(username,email,password):
    cursor.execute("INSERT INTO userdetails(username,email,password) VALUES(%s,%s,%s)",(username,email,password))
    conn.commit()
    return ""

def erase(email):
    cursor.execute("DELETE FROM userdetails WHERE email=(%s)",(email,))
    conn.commit()
    return "deleted"

def fetch(email):
    cursor.execute("select * from userdetails where email=(%s)",(email,))
    res=cursor.fetchall()
    return res


def check(username,email,password):
    cursor.execute("SELECT * FROM userdetails where email=(%s) and password=(%s) and username=(%s)",(email,password,username))
    res=cursor.fetchall()
    return res

