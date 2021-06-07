from flask import Flask,render_template, request, redirect, url_for, session , app ,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your secret key'
sg=''
mydb= mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "foodorder"
)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'foodorder'



mysql = MySQL(app)

@app.route('/form',methods =['GET', 'POST'])
def form():
    if request.method == 'POST':
        Username = request.form['Username']
        Password = request.form['Password']
        ContactNo = request.form['ContactNo']
        Email = request.form['Email']
        Address = request.form['Address']
        City = request.form['City']
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s)''',(Username,Password,ContactNo,Email,Address,City))
        mysql.connection.commit()
        cursor.close()
        ms='Registered Successfully.'
        return render_template('signin.html',ms=ms)
    return render_template('regform.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        Username = request.form['Username']
        Password = request.form['Password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE Username = % s AND Password = % s', (Username, Password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True

            session['Username'] = user['Username']
            session['Password'] = user['Password']
            msg = 'Logged in successfully !'
            s=session['Username']
            return redirect(url_for('hello',s=s))
            print( session['Username'])
        else:
            msg = 'Incorrect username / password !'
    return render_template('signin.html', msg = msg)
    print(msg)




@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/menu')
def Index():

        mycursor=mydb.cursor()
        mycursor.execute("SELECT * FROM menu")

        data = mycursor.fetchall()
        mycursor.close()
        return render_template('market.html',menu=data)

@app.route('/Ordered')
def Ordered():
    return render_template('Ordered.html')





app.run(host='localhost', port=5000)
