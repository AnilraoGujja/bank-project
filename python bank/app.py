from flask import *
app = Flask(__name__) #WHERE FILES LOCATED 
accounts = {} #STORES DATA
@app.route('/') #LINK
def home():
    return render_template('login.html') #CONNECTS FRONT AND BACKEND
@app.route('/createpage')

def createpage():
    return render_template('createpage.html')



@app.route('/create',methods=["post"]) #HANDLES FORM SUBMISSION AND DATA COMING FROM USER
def create():
    name=request.form['name']
    accnum = request.form['accnum']
    pin = request.form['pin']
    accounts[accnum]={
        "name":name,
        "pin":pin,
        "balance":1000
    }
    
    return redirect(url_for('dashboard',accnum=accnum))
                            

@app.route('/login',methods=['POST'])
def login():
    
    accnum = request.form['accnum']
    pin = request.form['pin']
    if accnum in accounts and accounts[accnum]['pin']==pin:
        from flask import redirect, url_for
        return redirect(url_for('dashboard',accnum=accnum))
       
    else :
        return "invalid account number or pin"
    
@app.route('/dashboard/<accnum>')
def dashboard(accnum):
    user = accounts.get(accnum)
    if user :
        return render_template('dashboard.html',user=user,accnum=accnum)
    else:
        return "usernot found"
    
if __name__=='__main__':
    app.run(debug=True) #STARTS FLASK SERVER
