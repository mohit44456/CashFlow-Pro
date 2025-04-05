from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO transactions (date, category, amount, description) VALUES (?, ?, ?, ?)',
                   (data['date'], data['category'], data['amount'], data['description']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Transaction added successfully!"})

@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)