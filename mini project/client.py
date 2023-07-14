import socket
import sys
from colorama import init, Fore

SERVER_PORT = 2022
SERVER_IP = 'localhost'

init(convert=True)
sys_data = []

# Send data to server
def send_data(data):
    client_socket.send(data.encode())

# Receive data from server
def receive_data():
    return client_socket.recv(1024).decode()

# Create the connection
def start_connection(client_address):
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    client_id = input(Fore.LIGHTBLUE_EX + '\nEnter Client ID: ')
    send_data(client_id)

    server_response = receive_data()
    print(server_response)

    return client_id, client_address

def main():
    # Get client address
    client_address = socket.gethostbyname(socket.gethostname())

    # Initializing the connection
    client_id, client_address = start_connection(client_address)

    while True:
        stock_code = input(Fore.BLUE + 'Enter Stock Code: ').upper()
        bid_amount = input(Fore.BLUE + 'Enter Bid Amount: ')
        security_code = input(Fore.BLUE + 'Enter security code: ')
        send_data(stock_code + ' ' + bid_amount + ' ' + security_code)
        server_response = receive_data()

        # Append values to the dictionary
        sys_data.append({"Code": stock_code, "Value": bid_amount, "sec_code":security_code})

        print(server_response)

        next_bid = input(Fore.GREEN + 'Take a chance again for WIN? (Yes / No): ')
        if next_bid.upper() == "NO":
            print(Fore.BLUE + "Server has stopped....Have a nice day!")
            sys.exit()

if __name__ == '__main__':
    main()

