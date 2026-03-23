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
