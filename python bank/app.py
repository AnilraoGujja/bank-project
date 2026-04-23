from flask import *
app = Flask(__name__) #WHERE FILES LOCATED 
accounts = {} #STORES DATA
@app.route('/') #LINK
def home():
    return render_template('home.html') #CONNECTS FRONT AND BACKEND
@app.route('/create',methods=["post"]) #HANDLES FORM SUBMISSION AND DATA COMING FROM USER
def create():
    name=request.form['name']
    accnum = request.form['accnum']
    pin = request.form['pin']
    accounts[accnum]={
        "name":name,
        "pin":pin,
        "balance":0
    }
    from flask import redirect,url_for
    return redirect(url_for('login_page'))
@app.route('/login')
def login_page():
    return render_template('login.html')
@app.route('/login',methods=['POST'])
def login():
    accnum = request.form['accnum']
    pin = request.form['pin']
    if accnum in accounts and accounts[accnum]['pin']==pin:
        return f"Welcome {accounts[accnum]['name']}!login successful"
    else :
        return "invalid account number or pin"
    
if __name__=='__main__':
    app.run(debug=True) #STARTS FLASK SERVER