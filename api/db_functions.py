import psycopg2
from dotenv import load_dotenv
import os

def snake_connect():
    # Load environment variables
    load_dotenv()
    
    # Connection strings info
    host = os.getenv("HOSTNAME")
    user = os.getenv("DB_USER")
    dbname = os.getenv("DB_NAME")
    password = os.getenv("PASSWORD")
    sslmode = os.getenv("MODE")

    # Connect to the database
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    conn = psycopg2.connect(conn_string)
    print("Established connection to database")

    return conn

def snake_close(conn):
    conn.commit()
    conn.close()

    print("Closed connection to database")
    print("Done")