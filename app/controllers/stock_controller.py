from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database.models.user_model import User
from app import db
# import jsonify

# stock controller blueprint to be registered with api blueprint
stock = Blueprint("stock", __name__)

start_date="2023-01-01"
end_date="2024-01-01"
stocks_map = {
    "SBIN": {
        "code": "SBIN",
        "avg_price": 150.0,
        "cagr": 0.5
        },
    "ADANIENT": {
        "code": "ADANIENT",
        "avg_price": 2800.0,
        "cagr": 0.5
        },
    "BPCL": {
        "code": "BPCL",
        "avg_price": 3400.0,
        "cagr": 0.5
        },
    "ADANIPORTS": {
        "code": "ADANIPORTS",
        "avg_price": 300.0,
        "cagr": 0.5
        },
    "AXISBANK": {
        "code": "AXISBANK",
        "avg_price": 700.0,
        "cagr": 0.5
        },
    "BRITANNIA": {
        "code": "BRITANNIA",
        "avg_price": 350.0,
        "cagr": 0.5
        }
}
stocks = ["SBIN", "ADANIENT", "BPCL", "ADANIPORTS", "AXISBANK", "BRITANNIA"]
showing_stocks = []
selected_stocks = []
graph_stocks = []

@stock.route('/dashboard' , methods=['POST', 'GET'])
def dashboard():
    global showing_stocks, selected_stocks, graph_stocks
    showing_stocks = [stock for stock in stocks if stock not in selected_stocks]
    return render_template('home.html', all_stocks=stocks, showing_stocks=showing_stocks, selected_stocks=selected_stocks, graph_stocks=graph_stocks, stocks_map=stocks_map)

@stock.route('/setDate' , methods=['POST', 'GET'])
def set_date():
    global stocks, showing_stocks, selected_stocks, graph_stocks, stocks_map
    # make api call to to update stocks_map
    showing_stocks = stocks.copy()
    selected_stocks = []
    graph_stocks = []
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

@stock.route('/update_graph', methods=['GET'])
def update_graph():
    global graph_stocks, selected_stocks, showing_stocks
    graph_stocks = selected_stocks.copy()
    # return redirect(url_for('/.stock.dashboard'))
    return {'graph_stocks': graph_stocks, 'start_date':start_date, 'end_date':end_date}