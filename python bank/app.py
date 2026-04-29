from flask import *
import os,json

app = Flask(__name__)
app.secret_key = "secret123"
# Temporary storage

def load_accounts():
    if os.path.exists('accounts.json'):
        try:
            with open('accounts.json', 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return{}
    return {}

def save_accounts(accounts):
    with open('accounts.json', 'w') as f:
        json.dump(accounts,f, indent=4)
accounts = load_accounts()

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

        save_accounts(accounts)

        return redirect(url_for('login'))

    return render_template('create.html')

# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        accnum = request.form['accnum']
        pin = request.form['pin']

        if accnum in accounts and accounts[accnum]['pin'] == pin:
            session['user'] = accnum
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid account number or pin"

    return render_template('login.html', error=error)

# ------------------ DASHBOARD ------------------
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        accnum = session['user']
        user = accounts.get(accnum)

        return render_template('dashboard.html', user=user, accnum=accnum)

    return redirect(url_for('login'))

@app.route('/deposit/<accnum>',methods=['POST'])
def deposit(accnum):
    user = accounts.get(accnum)
    if user:
        amount=int(request.form['amount'])
        user['balance'] += amount
        
        save_accounts(accounts)

    return redirect(url_for('dashboard',accnum=accnum))


@app.route('/withdraw/<accnum>',methods=['POST'])
def withdraw(accnum):
    user= accounts.get(accnum)
    if not user:
        flash("User not found", "error")
        return redirect(url_for('dashboard',accnum=accnum))
    amount = int(request.form['amount'])
    if amount <= user['balance']:
        user['balance'] -= amount
        save_accounts(accounts)

        flash("Withdrawal succcessful", "success")
    else:
        flash ("insufficient balance","error")

    return redirect(url_for('dashboard',accnum=accnum))

# ------------------ LOGOUT ------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ------------------ RUN APP ------------------
if __name__ == '__main__':
    app.run(debug=True)
