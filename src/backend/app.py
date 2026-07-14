from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def get_db_connection():
    conn = sqlite3.connect('auction.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create database and table if not exists
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            auction_id TEXT NOT NULL,
            bid_amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# API endpoint to add a new bid
@app.route('/bid', methods=['POST'])
def add_bid():
    data = request.get_json()
    auction_id = data['auction_id']
    bid_amount = data['bid_amount']

    if not auction_id or not bid_amount:
        return jsonify({'error': 'Auction ID and Bid Amount are required'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO bids (auction_id, bid_amount) VALUES (?, ?)', (auction_id, bid_amount))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Bid added successfully'}), 201

# API endpoint to get all bids
@app.route('/bids', methods=['GET'])
def get_bids():
    conn = get_db_connection()
    bids = conn.execute('SELECT * FROM bids').fetchall()
    conn.close()

    return jsonify([dict(bid) for bid in bids])

# Initialize database on startup
init_db()

if __name__ == '__main__':
    app.run(debug=True)
```

This is a basic Flask application with two API endpoints:

1. `/bid` (POST): Adds a new bid to the database.
2. `/bids` (GET): Retrieves all bids from the database.

The application uses SQLite as the database, and it initializes the database and table when the app starts. The `init_db` function creates a table named `bids` if it doesn't already exist.

To run this application, save the code to a file named `app.py`, then execute it using Python:

```sh
python app.py
```

The Flask development server will start, and you can interact with the API endpoints using tools like Postman or curl.