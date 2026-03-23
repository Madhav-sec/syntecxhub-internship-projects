"""
SyntecXHub Internship - Encrypted Chat Server (Updated)
AES-encrypted multi-client chat using Fernet + TCP sockets + threading
Shows encrypted payload in debug output to prove encryption
"""

import socket
import threading
from cryptography.fernet import Fernet, InvalidToken
import base64
import logging
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# Pre-shared key (for demo only – in production use proper key exchange)
KEY = b'pRmgMa8T0INjTGwgv5ivyyG8ZK-taG7m6duijaDhp94='
fernet = Fernet(KEY)

HOST = '0.0.0.0'
PORT = 5555

logging.basicConfig(
    filename='chat_log.txt',
    level=logging.INFO,
    format='%(asctime)s | %(message)s'
)

clients = []           # list of (conn, addr, username)
lock = threading.Lock()

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

def broadcast(message, sender_conn=None, sender_addr=None):
    """Broadcast encrypted message to all clients except sender"""
    encrypted = fernet.encrypt(message.encode())
    with lock:
        for client_conn, client_addr, _ in clients:
            if client_conn != sender_conn:
                try:
                    client_conn.send(encrypted)
                except:
                    pass  # silent fail - will be cleaned up later

    # Log to file (plain text for audit)
    log_msg = f"{get_timestamp()} | {sender_addr or 'Server'} → Broadcast: {message}"
    logging.info(log_msg)
    print(Fore.CYAN + log_msg)

def handle_client(conn, addr):
    """Handle one client connection"""
    username = f"{addr[0]}:{addr[1]}"
    print(Fore.GREEN + f"[{get_timestamp()}] New connection: {username}")

    with lock:
        clients.append((conn, addr, username))
        count = len(clients)
    broadcast(f"User {username} joined the chat! ({count} online)")

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            try:
                # Show what was received (encrypted)
                hex_data = data.hex()
                print(Fore.YELLOW + f"[{get_timestamp()}] [{username}] Received encrypted: {hex_data[:60]}...")

                decrypted = fernet.decrypt(data).decode()
                msg = f"[{get_timestamp()}] {username}: {decrypted}"
                print(Fore.WHITE + msg)
                broadcast(decrypted, conn, username)
            except InvalidToken:
                print(Fore.RED + f"[{get_timestamp()}] [{username}] Invalid token (possible tampering)")
                break
            except Exception as e:
                print(Fore.RED + f"[{get_timestamp()}] [{username}] Error: {e}")
                break
    finally:
        with lock:
            if (conn, addr, username) in clients:
                clients.remove((conn, addr, username))
        conn.close()
        print(Fore.RED + f"[{get_timestamp()}] {username} disconnected")
        broadcast(f"User {username} left the chat! ({len(clients)} online)")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(Fore.CYAN + f"[*] Server listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Server shutting down...")
    finally:
        server.close()

if __name__ == "__main__":
    main()