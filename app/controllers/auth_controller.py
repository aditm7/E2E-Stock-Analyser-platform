from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from database.models.user_model import User
from app import db

# auth controller blueprint to be registered with api blueprint
auth = Blueprint("auth", __name__)

@auth.route('/')
def index():
    from config.api_client import ApiClient
    client = ApiClient()
    load = {"from_date":"2024-01-25","to_date":"2024-01-25"}
    
    print(client.get("market_data",load,"SBIN"))
    return render_template("login.html")

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        new_user = User(username=username, password_hash=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('/.auth.index'))

    return render_template('register.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('/.auth.index'))
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect(url_for('/.stock.dashboard'))
    else:
        flash('Invalid username or password')
        return redirect(url_for('/.auth.index'))

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('/.auth.index'))