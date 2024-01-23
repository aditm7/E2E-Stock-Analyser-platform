from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.user_model import User
from backend import db

# stock controller blueprint to be registered with api blueprint
stock = Blueprint("stock", __name__)

stocks = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "FB"]
selected_stocks = []
graph_stocks = []

@stock.route('/dashboard' , methods=['POST', 'GET'])
def dashboard():
    if 'user_id' in session:
        return render_template('home.html', username=session['username'], all_stocks=stocks, filtered_stocks=stocks, selected_stocks=selected_stocks)
    else:
        return redirect(url_for('/api.auth.index'))

@stock.route('/search', methods=['POST'])
def search():
    query = request.form.get('search')
    results = [stock for stock in stocks if query.lower() in stock.lower()]
    return render_template('home.html', all_stocks=stocks, filtered_stocks=results, query=query, selected_stocks=selected_stocks)

@stock.route('/add_stocks', methods=['POST'])
def add_stocks():
    global graph_stocks, selected_stocks
    added_stocks = request.form.getlist('selected_stocks')
    selected_stocks.extend(added_stocks)
    return render_template('home.html', all_stocks=stocks, filtered_stocks=stocks, graph_stocks=graph_stocks, selected_stocks=selected_stocks)

@stock.route('/update_graph', methods=['POST'])
def update_graph():
    global graph_stocks, selected_stocks
    print(selected_stocks)
    graph_stocks = selected_stocks.copy()
    selected_stocks = []
    return render_template('home.html', all_stocks=stocks, filtered_stocks=stocks, graph_stocks=graph_stocks, selected_stocks=selected_stocks)

# @stock.route('/clear', methods=['POST'])
# def clear():
#     graph_stocks = []
#     selected_stocks = []
#     return render_template('home.html', all_stocks=stocks, filtered_stocks=stocks, graph_stocks=selected_stocks, selected_stocks=graph_stocks)