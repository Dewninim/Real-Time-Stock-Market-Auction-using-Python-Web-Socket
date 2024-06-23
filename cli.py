import socket
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 2022

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))

while True:
    # Receive the initial prompt from the server
    initial_prompt = client_socket.recv(1024).decode()
    print(initial_prompt, end=' ')

    # Send the ID to the server
    log_id = input()
    client_socket.send(log_id.encode())

    while True:
        # Receive the stock symbol prompt from the server
        stock_symbol_prompt = client_socket.recv(1024).decode()
        print(stock_symbol_prompt, end=' ')

        # Send the stock symbol to the server
        stock_symbol = input()
        client_socket.send(stock_symbol.encode())

        if stock_symbol == 'quit':
            break

        # Receive the bid amount prompt from the server
        bid_amount_prompt = client_socket.recv(1024).decode()
        print(bid_amount_prompt, end=' ')

        # Send the bid amount to the server
        bid_amount = input()
        client_socket.send(bid_amount.encode())

        # Receive the security code prompt from the server
        security_code_prompt = client_socket.recv(1024).decode()
        print(security_code_prompt, end=' ')

        # Send the security code to the server
        security_code = input()
        client_socket.send(security_code.encode())

        # Receive the response from the server
        response = client_socket.recv(1024).decode()
        print(response)

        # Sleep for 5 minutes after placing the bid
        if response.startswith("Bid placed successfully"):
            print("Waiting for 5 minutes...")
            time.sleep(300)

    break

# Close the client socket
client_socket.close()

