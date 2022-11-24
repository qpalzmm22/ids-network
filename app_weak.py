"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session
import sqlite3 as sql

# from flask_sqlalchemy import SQLAlchemy
# from instagram import getfollowedby, getname

con = sql.connect("data.db", check_same_thread = False)
cur = con.cursor()

statement = f"CREATE TABLE IF NOT EXISTS users('username' TEXT, 'password' TEXT);"
cur.execute(statement)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)


# class User(db.Model):
#     """ Create user table"""
#     id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(80), unique=True)
    # password = db.Column(db.String(80))

#     def __init__(self, username, password):
#         self.username = username
#         self.password = password


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_template('index.html', data=getfollowedby(username))
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        
        print("name : ", name)
        print("password : ", passw)

        statement = f"SELECT username from users WHERE username='{name}' AND Password = '{passw}';"
        cur.execute(statement)

        if not cur.fetchone():  # An empty result evaluates to False.
            session['logged_in'] = True
            return "Login Success"
        else:
            return "Login Failed.."

        # try:
        #     data = User.query.filter_by(username=name, password=passw).first()
        #     if data is not None:
        #         session['logged_in'] = True
        #         return redirect(url_for('home'))
        #     else:
        #         return 'Dont Login'
        # except:
        #     return "Dont Login"

@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        # new_user = User(username=request.form['username'], password=request.form['password'])

        # db.session.add(new_user)
        # db.session.commit()

        name = request.form['username']
        passw = request.form['password']

        statement = f"INSERT INTO users VALUES ('{name}','{passw}');"
        cur.execute(statement)

        return render_template('login.html')
    return render_template('register.html')

@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    # with app.app_context() :
    #     db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    
