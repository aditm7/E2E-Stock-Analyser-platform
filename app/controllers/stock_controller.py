from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from database.models.user_model import User
from app import db
from config.api_client import ApiClient

# stock controller blueprint to be registered with api blueprint.
stock = Blueprint("stock", __name__)

# Global parameters
start_date="2023-01-01"
end_date="2024-01-01"
stocks_map={}
stocks=[]
showing_stocks = []
selected_stocks = []
graph_stocks = []

# Creating a client that will send all the API requests to the server.
api_client = ApiClient()

@stock.route('/dashboard' , methods=['POST', 'GET'])
def dashboard():
    global stocks, showing_stocks, selected_stocks, graph_stocks, stocks_map
    # Fetch the list of stock symbols from the server.
    companies_list = api_client.get('all_companies')
    stocks = []
    stocks_map = {}
    # Update the stocks map to include stock symbols.
    for company in companies_list:
        symbol=company['symbol']
        stocks.append(symbol)
        stocks_map[symbol] = {
            "code":symbol,
            "cagr":float(0.0)
        }
    # Update the stocks map to include CAGR from the start and end dates.
    for stock in stocks:
        stock_obj = api_client.get("statistical_data", {"to_date":end_date,"from_date":start_date}, stock)
        stocks_map[stock]["cagr"] = stock_obj["cagr"]
    
    # Set the showing list of stocks.
    showing_stocks = [stock for stock in stocks if stock not in selected_stocks]
    # Render the home page.
    return render_template('home.html', all_stocks=stocks, showing_stocks=showing_stocks, selected_stocks=selected_stocks, graph_stocks=graph_stocks, stocks_map=stocks_map, from_date=start_date, to_date=end_date)

@stock.route('/process_date' , methods=['POST', 'GET'])
def process_date():
    global stocks, showing_stocks, selected_stocks, graph_stocks, stocks_map, start_date, end_date
    start_date = request.form.get('from_date')
    end_date = request.form.get('to_date')
    showing_stocks = stocks.copy()
    selected_stocks = []
    graph_stocks = []
    return redirect(url_for('/.stock.dashboard'))

@stock.route('/filter_stocks', methods=['GET'])
def filter_stocks():
    global showing_stocks, selected_stocks, graph_stocks

    from_cagr = float(request.args.get('from_cagr'))
    to_cagr = float(request.args.get('to_cagr'))

    showing_stocks = [stock for stock, data in stocks_map.items() if
                       data['cagr'] >= from_cagr and data['cagr'] <= to_cagr and stock not in selected_stocks]

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
    global graph_stocks, selected_stocks, showing_stocks, start_date, end_date
    graph_stocks = selected_stocks.copy()
    stockDataArray = []
    for stock in graph_stocks:
        stockData = api_client.get('market_data',{"to_date":end_date,"from_date":start_date}, stock)
        stockDataArray.append({'stock':stock, 'data':stockData})
    return {'stockDataArray': stockDataArray}