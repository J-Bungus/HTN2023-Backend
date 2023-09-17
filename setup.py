from db_functions import *

# Connect to the database
conn = snake_connect()
cursor = conn.cursor()
with open("./clear.sql", 'r') as sql_script:
    cursor.execute(sql_script.read())
    print("Cleared database")

# Create the database
with open ("./init.sql", 'r') as sql_script:
    cursor.execute(sql_script.read())
    print("Setup database")

# Close the connection
snake_close(conn)