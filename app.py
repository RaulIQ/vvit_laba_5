import requests
from flask import Flask, render_template, request, redirect
import psycopg2

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="password",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()
app = Flask(__name__)

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        print(type(login), login)
        password = request.form.get('password')
        if not(name and login and password):
            return ('Your name or login or password not entered.')
        cursor.execute("SELECT * FROM service.users WHERE login=%s", (login,))
        records = list(cursor.fetchall())
        print(records)
        if records:
            return 'Login already exist. Please, create new login.'
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')