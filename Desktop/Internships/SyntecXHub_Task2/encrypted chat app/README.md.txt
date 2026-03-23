# SyntecXHub Internship - Task 2: Encrypted Chat App

Submitted by: Madhav  
Date: March 2026  

A secure real-time chat application where all messages are encrypted using *AES-256-GCM* before transmission over TCP sockets.

## Features Implemented

- TCP client-server communication
- AES-256-GCM encryption with authentication (confidentiality + integrity)
- Unique random nonce (IV) generated for every message
- Pre-shared key derivation using PBKDF2 (with high iteration count)
- Multi-client support (server uses threading for concurrency)
- Message logging (server logs both plain and encrypted payloads)
- Debug prints showing encrypted bytes (proof that messages are not sent in plain text)
- Graceful disconnection handling

## Tech Stack

- Python 3
- `socket`, `threading`
- `cryptography` library (AESGCM + PBKDF2HMAC)
- No external frameworks – pure Python

## Installation

```bash
pip install cryptography