import socket
import time
import pandas as pd
import threading
import datetime
from colorama import init, Fore

init(convert=True)

SERVER_PORT = 2022
SERVER_IP = 'localhost'
stocks = {}
repeating = 1

print(Fore.GREEN + "\n-------------------- || Server Started || -------------------\n")


# Function to receive signal from client to initiate connection
def recv_signal(client_socket):
    recv_sig = client_socket.recv(1024).decode()


def client_side(client_socket, client_id):
    global amount, stCode
    client_socket.send(get_dict().encode())

    while True:
        data = client_socket.recv(1024).decode()
        args = data.split()

        if len(args) >= 2:
            stCode, amount = args[:2]
            amount = float(amount)
            if stCode in stocks:
                client_socket.send(bid_control(stocks[stCode], client_id, amount).encode())
            else:
                client_socket.send("Invalid Stock Code {}".format(stCode).encode())
        else:
            client_socket.send("Invalid command. Usage: <stock_code> <bid_amount>".encode())


def get_dict():
    result = Fore.YELLOW + "\n| Stock Code |    Price    |   security code   |\n________________________________________________\n"
    sorted_stocks = sorted(stocks.items(), key=lambda x: (x[0], x[1]['security']))  # Sort stocks based on stock codes and security codes
    for stCode, stock in sorted_stocks:
        result += "| {} |  {}  |  {}  |\n".format(stock['code'].ljust(10), str(stock['current']).ljust(10), str(stock['security']).ljust(14))
    return result



def countdown():
    for i in range(240, -1, -1):
        minutes, seconds = divmod(i, 60)
        time.sleep(1)
        print(Fore.YELLOW + f"You have {minutes:3} minutes & {seconds:00} seconds to bid", end='\r')
        if i == 60:
            print(Fore.RED + "\nOne minute remaining..\n")
    print(Fore.RED + "\n" + "Time's up! You can't add a bid now.. ⏱️ ")
    max_bids = get_max_bids()
    df = pd.DataFrame(max_bids)
    print(df)


def bid_control(stock, user_id, bid):
    timer_thread = threading.Thread(target=countdown)

    global repeating
    if repeating == 1:
        timer_thread.start()
        repeating += 1
    if stock['current'] >= bid:
        return (Fore.RED + "Invalid bid amount! Bid a value higher than the current price..")

    current_time = time.time()
    stock['current'] = bid
    stock['bids'].append({'user_id': user_id, 'bid': bid, 'when': time.time()})
    timeinJust = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d  %H:%M:%S')
    file = open("save.txt", "a")
    file.write("{}\t{}\t{}\t{}\n".format(timeinJust, stock['code'].ljust(6), user_id, bid))
    file.close()

    max_bid = 0
    max_user = None
    for bid_info in stock['bids']:
        if bid_info['bid'] > max_bid:
            max_bid = bid_info['bid']
            max_user = bid_info['user_id']

    return "New value: {} bid for {} by {}. Maximum bid is {} by {}\n".format(bid, stock['code'], user_id, max_bid,
                                                                               max_user)


def get_max_bids():
    max_bids = []
    for stCode, stock in stocks.items():
        max_bid = 0
        max_user = None
        for bid_info in stock['bids']:
            if bid_info['bid'] > max_bid:
                max_bid = bid_info['bid']
                max_user = bid_info['user_id']
        max_bids.append({'stock code': stCode, 'max bid': max_bid, 'client id': max_user})
    return max_bids


def main():
    global stocks
    end = time.time() + 60

    data = pd.read_csv('st.csv')  # Read the CSV file using pandas
    stocks = {}

    for i, row in data.iterrows():
        stCode = row['Symbol']
        price = row['Price']
        security = row['Security']
        profit = row['Profit']

        stocks[stCode] = {
            'code': stCode,
            'price': price,
            'security': security,
            'profit': profit,
            'end': end,
            'current': price,
            'bids': []
        }
    # Create a new socket using the AF_INET (IPv4) and SOCK_STREAM (TCP) socket type
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    clients = {}
    while True:
        client_socket, client_address = server_socket.accept()
        client_id = client_socket.recv(1024).decode()
        clients[client_id] = client_socket

        thread = threading.Thread(target=client_side, args=(client_socket, client_id))
        thread.start()


if __name__ == '__main__':
    main()
