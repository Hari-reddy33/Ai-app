import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from groq import Groq
import datetime
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Groq Client setup
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Database setup
DB_PATH = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS test_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            input_code TEXT NOT NULL,
            explanation TEXT,
            fix TEXT,
            optimization TEXT,
            metrics TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Helper function for Groq AI
def analyze_code_with_ai(code):
    prompt = f"""
    Analyze the following code:
    {code}
    
    Provide:
    1. Error Explanation: Identify syntax or logical errors.
    2. Bug Fix: Suggest corrected code.
    3. Optimization: Suggest optimized code.
    4. Metrics: Estimated Complexity (1-10), Efficiency (1-10), Readability (1-10).
    
    Format the response as JSON with keys: 'explanation', 'fix', 'optimization', 'metrics'.
    'metrics' should be a sub-object with keys: 'complexity', 'efficiency', 'readability'.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a senior software engineer and AI code analyst. Always respond in JSON format."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        full_name = request.form['full_name']
        phone = request.form['phone']
        address = request.form['address']
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password, full_name, phone, address) VALUES (?, ?, ?, ?, ?, ?)',
                         (username, email, password, full_name, phone, address))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or Email already exists.', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    logs_count = conn.execute('SELECT COUNT(*) FROM test_logs WHERE user_id = ?', (session['user_id'],)).fetchone()[0]
    last_log = conn.execute('SELECT * FROM test_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('dashboard.html', logs_count=logs_count, last_log=last_log)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)


def extract_code(block):
    """
    Extract multiline code string from AI JSON-like response.
    """
    if isinstance(block, dict):

        # If proper field exists
        if "code" in block and block["code"].strip():
            return block["code"]

        if "code" in block and block["code"].strip():
            return block["code"]

        # Otherwise grab the longest multiline key
        for k in block.keys():
            if "\n" in k and len(k) > 50:
                return k
    if isinstance(block, dict):

        # If proper field exists
        if "corrected_code" in block and block["corrected_code"].strip():
            return block["corrected_code"]

        if "optimized_code" in block and block["optimized_code"].strip():
            return block["optimized_code"]

        # Otherwise grab the longest multiline key
        for k in block.keys():
            if "\n" in k and len(k) > 50:
                return k

    return str(block)



@app.route('/test_data', methods=['GET', 'POST'])
def test_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    result = None
    if request.method == 'POST':
        code = request.form['code']
        result = analyze_code_with_ai(code)
        
        if 'error' not in result:
            conn = get_db_connection()
            # Ensure all AI fields are strings or JSON strings to avoid sqlite3.ProgrammingError
            explanation = json.dumps(result.get('explanation')) if isinstance(result.get('explanation'), (dict, list)) else str(result.get('explanation', ''))
            fix = json.dumps(result.get('fix')) if isinstance(result.get('fix'), (dict, list)) else str(result.get('fix', ''))
            optimization = json.dumps(result.get('optimization')) if isinstance(result.get('optimization'), (dict, list)) else str(result.get('optimization', ''))
            metrics_dict = result.get('metrics', {})
            metrics_json = json.dumps(metrics_dict)
            
            conn.execute('INSERT INTO test_logs (user_id, input_code, explanation, fix, optimization, metrics) VALUES (?, ?, ?, ?, ?, ?)',
                         (session['user_id'], code, explanation, fix, optimization, metrics_json))
            conn.commit()
            conn.close()
            
            # Update result for template rendering
            result['explanation'] = explanation
            # result['fix'] = fix
            # result['optimization'] = optimization
            result["fix"] = extract_code(result["fix"])
            result["optimization"] = extract_code(result["optimization"])
            result['metrics'] = metrics_dict
        else:
            flash(f"AI Error: {result['error']}", 'danger')
            
    return render_template('test_data.html', result=result)

@app.route('/logs')
def logs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    logs = conn.execute('SELECT * FROM test_logs WHERE user_id = ? ORDER BY timestamp DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('logs.html', logs=logs)

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    logs = conn.execute('SELECT metrics FROM test_logs WHERE user_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    
    metrics_data = []
    for log in logs:
        if log['metrics']:
            metrics_data.append(json.loads(log['metrics']))
            
    return render_template('reports.html', metrics_data=metrics_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
