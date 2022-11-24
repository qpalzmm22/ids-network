"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session
import sqlite3 as sql


con = sql.connect("data.db", check_same_thread = False)
cur = con.cursor()

statement = f"CREATE TABLE IF NOT EXISTS users('username' TEXT, 'password' TEXT);"
cur.execute(statement)

app = Flask(__name__)

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

        statement = f"SELECT username from users WHERE username='{name}' AND password = '{passw}';"
        print(statement)
        cur.execute(statement)
        

        if not cur.fetchone():  # An empty result evaluates to False.
            print("Login Failed")
            return redirect(url_for('home'))
        else:
            print("Login Success")
            session['logged_in'] = True
            return redirect(url_for('home'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':

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
    #app.debug = True
    # with app.app_context() :
    #     db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    
