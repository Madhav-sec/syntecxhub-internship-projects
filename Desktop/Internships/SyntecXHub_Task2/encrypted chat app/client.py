"""
SyntecXHub Internship - Encrypted Chat Client (Updated)
Connects to server, encrypts messages with AES (Fernet)
Shows encrypted payload before sending
"""

import socket
import threading
from cryptography.fernet import Fernet, InvalidToken
from colorama import init, Fore, Style
from datetime import datetime

init(autoreset=True)

# Same key as server
KEY = b'pRmgMa8T0INjTGwgv5ivyyG8ZK-taG7m6duijaDhp94='
fernet = Fernet(KEY)

HOST = '127.0.0.1'  # ← change to server IP if not local
PORT = 5555

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

def receive():
    while True:
        try:
            data = client.recv(4096)
            if not data:
                print(Fore.RED + f"[{get_timestamp()}] Disconnected from server")
                break

            # Show raw received bytes
            hex_data = data.hex()
            print(Fore.YELLOW + f"[{get_timestamp()}] Received raw encrypted: {hex_data[:60]}...")

            try:
                decrypted = fernet.decrypt(data).decode()
                print(Fore.GREEN + f"[{get_timestamp()}] {decrypted}")
            except InvalidToken:
                print(Fore.RED + f"[{get_timestamp()}] Invalid encrypted message received")
        except:
            print(Fore.RED + f"[{get_timestamp()}] Connection lost")
            break

def main():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(Fore.GREEN + f"[{get_timestamp()}] Connected to {HOST}:{PORT}")
    except Exception as e:
        print(Fore.RED + f"[{get_timestamp()}] Connection failed: {e}")
        return

    # Start receiving thread
    receive_thread = threading.Thread(target=receive, daemon=True)
    receive_thread.start()

    print(Fore.CYAN + "[*] Type messages below (type 'quit' to exit)")

    try:
        while True:
            message = input("")
            if message.lower() == 'quit':
                break
            if not message.strip():
                continue

            encrypted = fernet.encrypt(message.encode())
            hex_enc = encrypted.hex()

            print(Fore.YELLOW + f"[{get_timestamp()}] Sending encrypted: {hex_enc[:60]}...")
            client.send(encrypted)
    except KeyboardInterrupt:
        pass
    finally:
        print(Fore.RED + f"[{get_timestamp()}] Closing connection...")
        client.close()

if __name__ == "__main__":
    main()