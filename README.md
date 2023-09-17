# Snake API Documentation

## Overview
The Snake API is used to perform CRUD operations on the PostgresSQL database. The database contains user login information, user scores, and skin information. This API performs operations on all these tables using Flask and psycopg2.

## Endpoints
Base URL (temporary): http://127.0.0.1:5000

### Registration
This is the registration endpoint for the game

**Note**: If registration is successful, an entry in the Ownership table is automatically generated and each skin defaulted to false.
**URL**: /register
**Method**: POST
**Parameters**:
* username
* password

**Response Messages:**
* "Username already exists"
* "Registration successful"

**Response Format (200 OK):**
```python
{
    "data": None,
    "message": "Registration successful",
    "status": 0
}
{
    "data": None,
    "message": "Username already exists",
    "status": 1
}
```

### Login
This is the login endpoint for the game.

**URL**: /login
**Method**: POST
**Parameters**:
* username
* password
**Response Messages:**
* "User does not exist"
* "Incorrect password"
* "Login successful"

**Response Format (200 OK):**
```python
{
    "data": [<id>, <username>, <hashed password>, <coins>],
    "message": "Login successful",
    "status": 0
}

{
    "data": None,
    "message": "User does not exist"
    "status": 1
}
```

### Inserting Scores
This endpoint inserts scores into the database.

**URL**: /post_score
**Method**: POST
**Parameters**:
* username
* score

**Response Format (200 OK):**
```python
{
    "data": None,
    "message": "Score posted",
    "status": 0
}   
```

### Personal Highscore
This endpoint returns the user's highscore

**URL**: /personal_highscore
**Method**: GET
**Parameters**:
* username

**Response Format (200 OK):**
```python
{
    "data": 15,
    "message": "Highscore retrieved",
    "status": 0
}
```

### Leaderboard
This endpoint returns a list of the top 10 scores in the database

**URL**: /leaderboard
**Method**: GET
**Parameters**:
* None

**Response Format (200 OK):**
```python
{
    "data": [["JBungus", 14, "Sun, 17 Sep 2023"], ...],
    "message": "Leaderboard retrieved",
    "status": 0
}
```
### Skin cost
This endpoint returns the cost of a particular skin

**URL**: /get_cost
**Method**: GET
**Parameters**:
* skinid

**Response Format (200 OK):**
```python
{
    "data": 21,
    "message": "Cost retrieved",
    "status": 0
}
```

### Get coin count
This endpoint returns the number of coins that the user owns

**URL**: /get_coins
**Method**: GET
**Parameters**:
* username

**Response Format (200 OK):**
```python
{
    "data": 23,
    "message": "Coins retrieved",
    "status": 0
}
```

### Purchase skins
This endpoint updates the skin ownership for a particular user and adjusts their coins accordingly.

**Note**: The caller must ensure that the user can afford to purhcase the skin using the get_coins and get_cost endpoints.
**URL**: /purchase-skin
**Method**: POST
**Parameters**:
* username
* skinid

**Response Format (200 OK):**
```python
{
    "data": None,
    "message": "Skin purchased",
    "status": 0
}
```

### Check skin ownership
This endpoint determines whether a particular user owns a skin

**URL**: /check_ownership
**Method**: GET
**Parameters**:
* username

**Response Format (200 OK):**
```python
{
    "data": True,
    "message": "Ownership retrieved",
    "status": 0
}
```