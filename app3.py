from flask import Flask, render_template, request,url_for ,flash #NEW IMPORT -- request
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField
from forms import ContactForm 					# NEW IMPORT LINE
from flaskext.mysql import MySQL
from flask.ext.login import login_user, login_required, logout_user, LoginManager

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'WebDesign'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '223119'
app.config['MYSQL_DATABASE_DB'] = 'EmpData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

login_manager = LoginManager()  #don't understand
login_manager.init_app(app)     #don't understand
login_manager.login_view = "user.login"



#decorator that links...
@app.route('/')          								#This is the main URL
def default():
    return render_template("index.html", name = "index", title = "HOME PAGE")			#The argument should be in templates folder

@app.route('/index')          								#This is the main URL
def index():
    return render_template("index.html", name = "index", title = "HOME PAGE")			#The argument should be in templates folder

@app.route('/mypage')          								#This is the main URL
def community():
    return render_template("mypage.html", name = "mypage", title = "MYPAGE PAGE")			#The argument should be in templates folder

@app.route('/history')          								#This is the main URL
def history():
    return render_template("history.html", name = "history", title = "HISTORY PAGE")			#The argument should be in templates folder

@app.route('/tools')          								#This is the main URL
def tools():
    return render_template("tools.html", name = "tools", title = "TOOLS PAGE")			#The argument should be in templates folder

@app.route('/masterpieces')          								#This is the main URL
def masterpieces():
    return render_template("masterpieces.html", name = "masterpieces", title = "MASTERPIECES PAGE")

@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def pageNotFound(e):
    return render_template('500.html'), 500

@login_manager.user_loader    #don't understand
def load_user(user_id):
    return User.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = ContactForm()

    if request.method == 'POST':
        newusername = form.name.data
        newpassword = form.password.data
        print form.name.data
        print form.password.data
        # cursor = mysql.connect().cursor()
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user (userName,password) VALUES ('{0}', '{1}')".format(newusername,newpassword))
        conn.commit()
        return 'Congratulations, you have successfully registered!'

    elif request.method == 'GET':
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = ContactForm()

    if request.method == 'POST':
        username = form.name.data
        password = form.password.data
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()   # define after this ?
        if data is None:
            return "Username or Password is wrong"
        else:
            login_user(user) #user is not defined, where the hell to define it?
            flash('Logged in successfully')
            return render_template('login.html', data=data, form=form)

    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/logout')
@login_required         # means after user login?
def logout():
    session.pop('logged_in',None)
    flash('You were logged out.')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)		#debug=True is optional