# SyntecXHub Internship - Task 1 Projects

Submitted by:Madhav  
Date:March 2026 

Completed the first internship task for SyntecXHub: two projects demonstrating socket programming, concurrency, and secure encryption.

# Projects Overview

#  1. Port Scanner (TCP Port Scanner)
- Folder: [port_scanner](port_scanner)
- Description: A threaded TCP port scanner built with Python sockets and concurrent futures.
# Features
  - Scans single host or port range
  - Adjustable threads and timeout
  - Service name lookup for open ports
  - Logs results to file + console output
  - Tested on localhost (open ports 135/epmap & 445/microsoft-ds detected)
  # Main file: [port_scanner.py](port_scanner/port_scanner.py)
- README & Screenshots: Inside [port_scanner/README.md](port_scanner/README.md) and [screenshots](port_scanner/screenshots)

#  2. Password Manager (Secure Local Vault)
- Folder: [password_manager](password_manager)
- Description: A local password manager using AES encryption (Fernet) with PBKDF2 key derivation from a master password.
  # Features
  - Add, list, get, search, delete entries
  - Encrypted JSON storage (secure_vault.enc)
  - Master password required for decryption
  - All test/fake data used (no real credentials)
- # Main file: [password_manager.py](password_manager/password_manager.py)
- README & Screenshots: Inside [password_manager/README.md](password_manager/README.md) and [screenshots](password_manager/screenshots)

# Tech Stack
- Python 3
- Libraries: socket, concurrent.futures, cryptography (Fernet + PBKDF2)
- Tools: Git, GitHub, VS Code / Notepad

## How to Run (General)
1. Clone the repo:
   ```bash
   git clone https://github.com/Madhav-sec/syntecxhub-internship-projects.git
   

# Task 2: Encrypted Chat App

Submitted by: Madhav  
Date: March 2026  

A secure multi-client real-time chat application where all messages are encrypted using **AES-256-GCM** before being sent over TCP sockets.

# Features Implemented

- TCP client-server architecture
- AES-256-GCM encryption with authentication (confidentiality + integrity)
- Random nonce (IV) generated for every single message
- Key derived from passphrase using PBKDF2 (600,000 iterations)
- Server supports multiple clients concurrently using threading
- Server logs both plain and encrypted messages to `chat_log.txt`
- Debug prints show raw encrypted hex payload (proof that messages are encrypted on the wire)
- Graceful client disconnection and broadcast on leave/join

## Tech Stack

- Python 3
- socket, threading
- cryptography library (AESGCM + PBKDF2HMAC)
- No external frameworks – pure Python

## Installation

Install the only dependency:
```bash
pip install cryptography
