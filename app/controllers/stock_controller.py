from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database.models.user_model import User
from app import db
# import jsonify

# stock controller blueprint to be registered with api blueprint
stock = Blueprint("stock", __name__)

stocks_map = {
    "AAPL": {
        "code": "AAPL",
        "avg_price": 150.0,
        "cagr": 0.5
        },
    "GOOGL": {
        "code": "GOOGL",
        "avg_price": 2800.0,
        "cagr": 0.5
        },
    "AMZN": {
        "code": "AMZN",
        "avg_price": 3400.0,
        "cagr": 0.5
        },
    "MSFT": {
        "code": "MSFT",
        "avg_price": 300.0,
        "cagr": 0.5
        },
    "TSLA": {
        "code": "TSLA",
        "avg_price": 700.0,
        "cagr": 0.5
        },
    "FB": {
        "code": "FB",
        "avg_price": 350.0,
        "cagr": 0.5
        }
}
stocks = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "FB"]
showing_stocks = []
selected_stocks = []
graph_stocks = []

@stock.route('/dashboard' , methods=['POST', 'GET'])
def dashboard():
    global showing_stocks, selected_stocks, graph_stocks
    showing_stocks = [stock for stock in stocks if stock not in selected_stocks]
    return render_template('home.html', all_stocks=stocks, showing_stocks=showing_stocks, selected_stocks=selected_stocks, graph_stocks=graph_stocks, stocks_map=stocks_map)


@stock.route('/filter_stocks', methods=['GET'])
def filter_stocks():
    global showing_stocks, selected_stocks, graph_stocks

    from_price = float(request.args.get('from_price'))
    to_price = float(request.args.get('to_price'))

    showing_stocks = [stock for stock, data in stocks_map.items() if
                       data['avg_price'] >= from_price and data['avg_price'] <= to_price and stock not in selected_stocks]

    return {'new_showing_stocks': showing_stocks, 'stocks_map': stocks_map}

@stock.route('/select_stock', methods=['GET'])
def select_stock():
    global showing_stocks, selected_stocks, graph_stocks
    selected_stock = request.args.get('selected_stock')
    if selected_stock and selected_stock not in selected_stocks:
        selected_stocks.append(selected_stock)
    if selected_stock in showing_stocks:
        showing_stocks.remove(selected_stock)
    return {'new_showing_stocks': showing_stocks, 'new_selected_stocks': selected_stocks, 'stocks_map': stocks_map}


@stock.route('/remove_stock', methods=['GET'])
def remove_stock():
    global showing_stocks, selected_stocks, graph_stocks
    removed_stock = request.args.get('removed_stock')
    if removed_stock in selected_stocks:
        selected_stocks.remove(removed_stock)
    if removed_stock not in showing_stocks:
        showing_stocks.append(removed_stock)
    return {'new_showing_stocks': showing_stocks, 'new_selected_stocks': selected_stocks, 'stocks_map': stocks_map}

@stock.route('/reset_filter', methods=['GET'])
def clear():
    global graph_stocks, selected_stocks, showing_stocks
    # graph_stocks = []
    selected_stocks = []
    showing_stocks = stocks.copy()
    return {'new_showing_stocks': showing_stocks, 'new_selected_stocks': selected_stocks, 'stocks_map': stocks_map}

@stock.route('/show_all_stocks', methods=['GET'])
def show_all_stocks():
    global graph_stocks, selected_stocks, showing_stocks
    showing_stocks = [stock for stock in stocks if stock not in selected_stocks]
    return {'new_showing_stocks': showing_stocks, 'stocks_map': stocks_map}

@stock.route('/update_graph', methods=['POST'])
def update_graph():
    global graph_stocks, selected_stocks, showing_stocks
    print(selected_stocks)
    graph_stocks = selected_stocks.copy()
    # selected_stocks = []
    return redirect(url_for('/.stock.dashboard'))