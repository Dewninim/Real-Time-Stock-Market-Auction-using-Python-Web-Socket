import socket
import threading
import csv
import time
import sys

# Read the stock information from the CSV file
stock_data = []
with open('C:\\Users\\SG\\Documents\\Downloads\\stocks.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    stock_data = list(csv_reader)

# Store the stock data in a dictionary
stocks = {}
for row in stock_data:
    stock_code = row['Symbol']
    base_price = row['Price']
    stock_security = row['Security']
    profit = row['Profit']
    stocks[stock_code] = {
        'Base Price': base_price,
        'Stock Security': stock_security,
        'Profit': profit,
        'Current Bid': base_price,
        'Bidder': '',
        'Bid Time': '',
        'bid_log': []
    }

# Store the last bid time for each client
client_last_bid_time = {}

# Define the countdown function
def countdown(t):
    t = int(t)  # Convert remaining_time to integer
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        sys.stdout.write('\r' + timer)
        sys.stdout.flush()
        time.sleep(1)
        t -= 1

    print('\rFire in the hole!!')

# Define a function to handle a client connection
def handle_client(conn, addr):
    print(f"New connection from {addr}")
    while True:
        # Send initial prompt to the client
        initial_prompt = "Enter ID: "
        conn.send(initial_prompt.encode())
        # Receive the ID from the client
        log_id = conn.recv(1024).decode().strip()
        if not log_id:
            print(f"No ID provided by {addr}")
            break
        print(f"Logged in: {log_id}")

        while True:
            # Send prompt for stock symbol to the client
            stock_symbol_prompt = "Enter stock symbol (or 'quit' to exit): "
            conn.send(stock_symbol_prompt.encode())
            # Receive the stock symbol from the client
            stock_symbol = conn.recv(1024).decode().strip()
            if stock_symbol == 'quit':
                break
            if stock_symbol not in stocks:
                response = f"{stock_symbol} not found"
                conn.send(response.encode())
                continue
            # Send prompt for bid amount to the client
            bid_amount_prompt = f"Enter bid amount for {stock_symbol}: "
            conn.send(bid_amount_prompt.encode())
            # Receive the bid amount from the client
            bid_amount = conn.recv(1024).decode().strip()
            # Send prompt for security code to the client
            security_code_prompt = "Enter security code: "
            conn.send(security_code_prompt.encode())
            # Receive the security code from the client
            security_code = conn.recv(1024).decode().strip()
            # Perform the necessary operations with the bid details
            # For example, you can update the current bid and bidder in the stocks dictionary
            if security_code == stocks[stock_symbol]['Stock Security']:
                if float(bid_amount) > float(stocks[stock_symbol]['Current Bid']):
                    stocks[stock_symbol]['Current Bid'] = bid_amount
                    stocks[stock_symbol]['Bidder'] = log_id
                    stocks[stock_symbol]['Bid Time'] = time.time()
                    remaining_time = countdown_time - (time.time() - stocks[stock_symbol]['Bid Time'])
                    if remaining_time < 60:
                        additional_time = 60
                        stocks[stock_symbol]['Bid Time'] += additional_time
                        remaining_time += additional_time
                        response = f"Bid placed successfully. Current highest bid: {stocks[stock_symbol]['Current Bid']}. Additional time: {additional_time} seconds"
                    else:
                        response = f"Bid placed successfully. Current highest bid: {stocks[stock_symbol]['Current Bid']}"
                    notify_clients(response)
                    # Update the last bid time for the client
                    client_last_bid_time[log_id] = time.time()
                else:
                    response = f"Your bid amount is not higher than the current highest bid."
            else:
                response = "Invalid security code"
            # Send the response to the client
            conn.send(response.encode())
            # Sleep for 60 seconds after placing the bid
            if response.startswith("Bid placed successfully"):
                print("Waiting for 5 minutes....")
                countdown_thread = threading.Thread(target=countdown, args=(remaining_time,))
                countdown_thread.start()
                countdown_thread.join()

    print(f"Connection from {addr} closed")
    conn.close()

# Notify all connected clients
def notify_clients(message):
    for client_conn in client_conns:
        try:
            client_conn.send(message.encode())
        except:
            continue

# Set up the server socket
SERVER_HOST = 'localhost'
SERVER_PORT = 2022
countdown_time = 300  # 5 minutes
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen()
print("Server started. Listening on port 2022...")

# Store client connections
client_conns = []

# Accept incoming connections and spawn a new thread for each client
while True:
    conn, addr = server.accept()
    client_conns.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
