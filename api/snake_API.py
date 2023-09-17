from flask import Flask, jsonify
import bcrypt
from db_functions import *
from flask import request

# Connect to the database
conn = snake_connect()
cursor = conn.cursor()

app = Flask(__name__)

ret = {
    "status": -1,
    "message": "",
    "data": None
}

@app.route('/', methods=['GET'])
def index():
    return ret

@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    cursor.execute("""
        SELECT Password
        FROM "Users"
        WHERE UserName = %s;
        """, (username,))
    
    fetched_password = cursor.fetchone()[0].encode('utf-8')

    if fetched_password is None:
        ret["status"] = 1
        ret["message"] = "User does not exist"
        ret["data"] = None

    elif bcrypt.hashpw(password.encode('utf-8'), fetched_password) == fetched_password:
        ret["status"] = 0
        ret["message"] = "Login successful"
        cursor.execute("""
            SELECT * FROM "Users"
            WHERE UserName = %s;
            """, (username,))
        
        ret["data"] = cursor.fetchone()

    else:
        ret["status"] = 1
        ret["message"] = "Incorrect password"
        ret["data"] = None
    
    return ret

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']

    # Check if username already exists
    cursor.execute("""
        SELECT UserName
        FROM "Users"
        WHERE UserName = %s;
        """, (username,))
    
    if cursor.fetchone() is not None:
        ret["status"] = 1
        ret["message"] = "Username already exists"
        ret["data"] = None
        return ret
    
    # Add salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    cursor.execute("""
        INSERT INTO "Users" (UserName, Password)
        VALUES (%s, %s)
        RETURNING id;
        """, (username, hashed_password.decode('utf-8')))
    
    userid = cursor.fetchone()[0]

    cursor.execute(""" INSERT INTO "Ownership" ("userid") VALUES (%s); """, (userid,))

    ret["status"] = 0
    ret["message"] = "Registration successful"
    ret["data"] = None
    conn.commit()
    return ret

@app.route('/post_score', methods=['POST'])
def post_score():
    username = request.json['username']
    score = request.json['score']

    # Find ID associated with the username
    cursor.execute("""
        SELECT "id"
        FROM "Users"
        WHERE UserName = %s;
        """, (username,))
    
    user_id = cursor.fetchone()[0]

    # Insert new score entry into database
    cursor.execute("""
        INSERT INTO "Scores" ("userid", "score", "date")
        VALUES (%s, %s, CURRENT_TIMESTAMP);
        """, (user_id, score))
    
    # Compute coins gained from score
    coins = int(score) // 3

    # Update user's coins
    cursor.execute("""
        UPDATE "Users" SET "coins" = "coins" + %s WHERE "id" = %s;
        """, (coins, user_id))
    
    ret["status"] = 0
    ret["message"] = "Score posted"
    ret["data"] = None
    conn.commit()
    return ret

@app.route('/personal_highscore', methods=['GET'])
def personal_highscore():
    username = request.json['username']

    cursor.execute("""
        SELECT "id"
        FROM "Users"
        WHERE UserName = %s;
        """, (username,))
    
    userid = cursor.fetchone()[0]

    cursor.execute("""
        SELECT "score"
        FROM "Scores"
        WHERE "userid" = %s
        ORDER BY Score DESC
        """, (userid,))
    
    highscore = cursor.fetchone()[0]

    ret["status"] = 0
    ret["message"] = "Highscore retrieved"
    ret["data"] = highscore

    return ret

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    cursor.execute("""
        SELECT "userid", "score" , "date"
        FROM "Scores"
        ORDER BY Score DESC;
        """)

    id_board = cursor.fetchmany(10)
    leaderboard = [[]] * len(id_board)

    for i in range (len(id_board)):
        cursor.execute("""
            SELECT "username" FROM "Users" WHERE "id" = %s;
        """, (id_board[i][0],))

        username = cursor.fetchone()[0]
        leaderboard[i] = [username, id_board[i][1], id_board[i][2]]

    ret["status"] = 0
    ret["message"] = "Leaderboard retrieved"
    ret["data"] = leaderboard

    return ret

@app.route('/get_cost', methods=['GET'])
def get_costs():
    skin_id = request.json['skin_id']

    # Find snake skin cost associated with id
    cursor.execute("""
        SELECT "skincost" FROM "Skins" WHERE "skinid" = %s;
        """, (skin_id,))
    
    cost = int(cursor.fetchone()[0])

    ret["status"] = 0
    ret["message"] = "Cost retrieved"
    ret["data"] = cost

    return ret

@app.route('/get_coins', methods=['GET'])
def get_coins():
    username = request.json['username']

    # Find ID associated with the username
    cursor.execute("""
        SELECT "id"
        FROM "Users"
        WHERE UserName = %s;
        """, (username,))
    
    user_id = cursor.fetchone()[0]

    # Retrieve coins
    cursor.execute("""
        SELECT "coins"
        FROM "Users"
        WHERE "id" = %s;
        """, (user_id,))
    
    coins = int(cursor.fetchone()[0])

    ret["status"] = 0
    ret["message"] = "Coins retrieved"
    ret["data"] = coins

    return ret

@app.route('/purchase-skin', methods=['POST'])
def purchase_skin():
    username = request.json['username']
    skin_id = int(request.json['skin_id'])

    # Find ID associated with the username
    cursor.execute("""
        SELECT "id" FROM "Users" WHERE "username" = %s; 
        """, (username,))
    
    user_id = cursor.fetchone()[0]
    
    # Find snake skin cost associated with id
    cursor.execute("""
        SELECT "skincost" FROM "Skins" WHERE "skinid" = %s;
        """, (skin_id,))

    cost = cursor.fetchone()[0]

    # Update skin ownership
    if (skin_id == 1):
        cursor.execute("""
            UPDATE "Ownership" SET "snakeskin" = TRUE WHERE "userid" = %s;
            """, (user_id,))
    elif (skin_id == 2):
        cursor.execute("""
            UPDATE "Ownership" SET "rockskin" = TRUE WHERE "userid" = %s;
            """, (user_id,))
    elif (skin_id == 3):
        cursor.execute("""
            UPDATE "Ownership" SET "rockskin2" = TRUE WHERE "userid" = %s;
            """, (user_id, ))
        
    cursor.execute("""
    UPDATE "Users" SET "coins" = "coins" - %s  WHERE "id" = %s;
    """, (cost, user_id))

    ret["status"] = 0
    ret["message"] = "Skin purchased"
    ret["data"] = None
    conn.commit()

    return ret

@app.route('/check_ownership', methods=['GET'])
def check_ownership():
    username = request.json['username']
    skin_id = int(request.json['skin_id'])

    # Find ID associated with the username
    cursor.execute("""
        SELECT "id" FROM "Users" WHERE "username" = %s;
        """, (username,))
    
    user_id = cursor.fetchone()[0]

    # Retrieve skin ownership
    owned = False

    if (skin_id == 1):
        cursor.execute("""
            SELECT "snakeskin" FROM "Ownership" WHERE "userid" = %s;
            """, (user_id,))
        owned = bool(cursor.fetchone()[0])
    elif (skin_id == 2):
        cursor.execute("""
            SELECT "rockskin1" FROM "Ownership" WHERE "userid" = %s;
            """, (user_id,))
        owned = bool(cursor.fetchone()[0])
    elif (skin_id == 3):
        cursor.execute("""
            SELECT "rockskin2" FROM "Ownership" WHERE "userid" = %s;
            """, (user_id,))
        owned = bool(cursor.fetchone()[0])
    
    ret["status"] = 0
    ret["message"] = "Ownership retrieved"
    ret["data"] = owned

    return ret