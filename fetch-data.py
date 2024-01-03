import json
from uuid import uuid4
import robin_stocks.robinhood as robin

def get_all_stock_orders():
    holdings = robin.build_holdings(with_dividends=True)
    orders = []

    for symbol, data in holdings.items():
        order = {'symbol': symbol, 'price': data['price'], 'quantity': data['quantity'], 
            'equity': data['equity'], 'percent_change': data['percent_change'], 'intraday_percent_change': data['intraday_percent_change'],
            'equity_change': data['equity_change'], 'type': data['type'], 'name': data['name'],
            'id': data['id'], 'pe_ratio': data['pe_ratio'], 'percentage': data['percentage']}
    
        if 'dividend' in data:
            order.update({'dividend': data['dividend']})
        orders.append(order)
    return orders

print("getting credentials...")
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

credentials = config_data.get('Credentials', {})
r_username = list(credentials.keys())[0]
r_password = credentials.get(r_username)

print("logging in...")
robin.login(r_username, r_password)
print("pulling data")

#Get all stock orders
all_stock_orders = get_all_stock_orders()

print("exporting...")
#Write to file
with open('allstockorders.txt', 'w') as order_file:
    for order in all_stock_orders:
        order_file.write(f"Symbol: {order['symbol']}, Price: {order['price']}, "
                         f"Quantity: {order['quantity']}, Equity: {order['equity']}, "
                         f"Percent Change: {order['percent_change']}, "
                         f"Intraday Percent Change: {order['intraday_percent_change']}, "
                         f"Equity Change: {order['equity_change']}, Type: {order['type']}, "
                         f"Name: {order['name']}, ID: {order['id']}, PE Ratio: {order['pe_ratio']}, "
                         f"Percentage: {order['percentage']}, Dividend: {order.get('dividend', 'N/A')}\n")
        
print("\nStocks have been written to allstockorders.txt\n")
robin.logout()
print("logged out")