from flask import *
import os, json
import random, time

app = Flask(__name__)
app.secret_key = "secret123"

# ------------------ OTP FUNCTION ------------------
def generate_otp():
    return str(random.randint(100000, 999999))

# ------------------ STORAGE ------------------
def load_accounts():
    if os.path.exists('accounts.json'):
        try:
            with open('accounts.json', 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_accounts(accounts):
    with open('accounts.json', 'w') as f:
        json.dump(accounts, f, indent=4)

accounts = load_accounts()

# ------------------ HOME ------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ------------------ CREATE ACCOUNT ------------------
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        accnum = request.form.get('accnum')
        pin = request.form.get('pin')

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

# ------------------ LOGIN WITH OTP ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    show_otp = False

    # Reset OTP on fresh visit
    if request.method == 'GET':
        session.pop('otp', None)
        session.pop('otp_time', None)
        session.pop('temp_user', None)

    if request.method == 'POST':

        # ---------------- STEP 1: LOGIN ----------------
        if 'otp' not in session:
            accnum = request.form.get('accnum')
            pin = request.form.get('pin')

            if accnum in accounts and accounts[accnum]['pin'] == pin:
                otp = generate_otp()

                session['otp'] = otp
                session['otp_time'] = time.time()
                session['temp_user'] = accnum

                print("Your OTP is:", otp)  # Replace with SMS

                show_otp = True
            else:
                error = "Invalid account number or pin"

        # ---------------- STEP 2: OTP VERIFY ----------------
        else:
            show_otp = True
            otp_input = request.form.get('otp')

            if not otp_input:
                error = "Please enter OTP"

            elif time.time() - session.get('otp_time', 0) > 300:
                error = "OTP expired"
                session.clear()

            elif otp_input == session.get('otp'):
                session['user'] = session['temp_user']

                # Clear temp session data
                session.pop('temp_user', None)
                session.pop('otp', None)
                session.pop('otp_time', None)

                return redirect(url_for('dashboard'))
            else:
                error = "Invalid OTP"

    return render_template('login.html', error=error, show_otp=show_otp)

# ------------------ DASHBOARD ------------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    accnum = session['user']
    user = accounts.get(accnum)

    return render_template('dashboard.html', user=user, accnum=accnum)

# ------------------ DEPOSIT ------------------
@app.route('/deposit/<accnum>', methods=['POST'])
def deposit(accnum):
    if 'user' not in session or session['user'] != accnum:
        return redirect(url_for('login'))

    user = accounts.get(accnum)

    try:
        amount = int(request.form.get('amount', 0))
        if amount > 0:
            user['balance'] += amount
            save_accounts(accounts)
            flash("Deposit successful", "success")
        else:
            flash("Enter valid amount", "error")
    except:
        flash("Invalid input", "error")

    return redirect(url_for('dashboard'))

# ------------------ WITHDRAW ------------------
@app.route('/withdraw/<accnum>', methods=['POST'])
def withdraw(accnum):
    if 'user' not in session or session['user'] != accnum:
        return redirect(url_for('login'))

    user = accounts.get(accnum)

    try:
        amount = int(request.form.get('amount', 0))

        if amount <= 0:
            flash("Enter valid amount", "error")

        elif amount <= user['balance']:
            user['balance'] -= amount
            save_accounts(accounts)
            flash("Withdrawal successful", "success")

        else:
            flash("Insufficient balance", "error")

    except:
        flash("Invalid input", "error")

    return redirect(url_for('dashboard'))

# ------------------ LOGOUT ------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------ RUN ------------------
if __name__ == '__main__':
    app.run(debug=True)