# Bidding System

A command-line bidding system built using Python sockets, enabling real-time communication between clients and a server for auction-based transactions.

## Features
- User authentication and session management
- Create, manage, and delete auctions
- Place bids on active auctions
- Real-time bid updates using socket communication
- Secure and reliable bidding process
- Admin controls for auction and user management

## Technologies Used
- **Programming Language**: Python
- **Networking**: Python `socket` module
- **Concurrency**: `threading` for handling multiple clients

## Installation

### Prerequisites
- Python (>=3.8)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/DilshanAberathna/Bidding-system.git
   cd Bidding-system
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the server:
   ```sh
   python server.py
   ```
4. Run a client instance:
   ```sh
   python client.py
   ```

## Usage
1. Start the server (`server.py`).
2. Run multiple client instances (`client.py`).
3. Register/Login as a user.
4. Create an auction with a starting bid and time limit.
5. Place bids on available auctions.
6. Track auction progress and winners in real-time.

## Contribution
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes.
4. Push to your branch and create a Pull Request.


---

