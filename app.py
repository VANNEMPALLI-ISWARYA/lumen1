from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL database connection
db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="flaskdemo1")

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = db.cursor()
        cur.execute("SELECT * FROM users2 WHERE email=%s", (email,))
        account = cur.fetchone()
        if account:
            msg = 'Account already exists!'
        else:
            cur.execute("INSERT INTO users2 (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, password))  # Note: storing plain password for simplicity
            db.commit()
            cur.close()
            return redirect(url_for('login'))
        cur.close()
    return render_template('register.html', msg=msg)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = db.cursor()
        cur.execute("SELECT id, username, password FROM users2 WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()
        if user and password == user[2]:  # Plain-text password check
            session['logged_in'] = True
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            msg = 'Incorrect email or password!'
    return render_template('login.html', msg=msg)

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return render_template('dashboard.html', username=session.get('username'))
    return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
