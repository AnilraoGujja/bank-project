from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

# Temporary storage
accounts = {}

# ------------------ HOME ------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ------------------ CREATE ACCOUNT ------------------
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        accnum = request.form['accnum']
        pin = request.form['pin']

        if accnum in accounts:
            return "Account already exists!"

        accounts[accnum] = {
            "name": name,
            "pin": pin,
            "balance": 1000
        }

        return redirect(url_for('login'))

    return render_template('create.html')

# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        accnum = request.form['accnum']
        pin = request.form['pin']

        if accnum in accounts and accounts[accnum]['pin'] == pin:
            session['user'] = accnum
            return redirect(url_for('dashboard'))
        else:
            return "Invalid account number or pin"

    return render_template('login.html')

# ------------------ DASHBOARD ------------------
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        accnum = session['user']
        user = accounts.get(accnum)

        return render_template('dashboard.html', user=user, accnum=accnum)

    return redirect(url_for('login'))

# ------------------ LOGOUT ------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ------------------ RUN APP ------------------
if __name__ == '__main__':
    app.run(debug=True)