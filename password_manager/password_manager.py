"""
SyntecXHub Internship - Project 2: Secure Local Password Manager
Uses Fernet (AES-128-CBC + HMAC) with PBKDF2 key derivation
Stores encrypted JSON on disk (secure_vault.enc)
Commands: add, list, get, search [term], delete, quit
"""

import json
import os
import base64
import secrets
from getpass import getpass
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

VAULT_FILE = "secure_vault.enc"
SALT_SIZE = 16
KDF_ITERATIONS = 600_000  # Strong for local use in 2026

def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def create_new_vault(master_password: str):
    if os.path.exists(VAULT_FILE):
        print("[!] Vault already exists. Delete secure_vault.enc to create new.")
        return False
    salt = secrets.token_bytes(SALT_SIZE)
    key = derive_key(master_password, salt)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(b"[]")  # empty list
    with open(VAULT_FILE, "wb") as f:
        f.write(base64.b64encode(salt) + b"\n" + encrypted)
    print("[+] New vault created successfully.")
    return True

def load_vault(master_password: str):
    if not os.path.exists(VAULT_FILE):
        print("[!] No vault found. Type 'create' to make one.")
        return None, None, None
    with open(VAULT_FILE, "rb") as f:
        data = f.read().split(b"\n", 1)
        if len(data) != 2:
            print("[!] Vault file corrupted.")
            return None, None, None
        salt_b64, encrypted = data
    salt = base64.b64decode(salt_b64)
    key = derive_key(master_password, salt)
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(encrypted).decode()
        entries = json.loads(decrypted)
        return entries, fernet, salt
    except InvalidToken:
        print("[!] Incorrect master password or corrupted vault.")
        return None, None, None

def save_vault(entries, fernet, salt):
    encrypted = fernet.encrypt(json.dumps(entries).encode())
    with open(VAULT_FILE, "wb") as f:
        f.write(base64.b64encode(salt) + b"\n" + encrypted)

def main():
    print("=== Secure Local Password Manager (Fernet + PBKDF2) ===")
    print("Commands: create | add | list | get | search [term] | delete | quit\n")

    master_pw = getpass("Master password: ").strip()

    if master_pw.lower() == "create":
        new_pw = getpass("Choose a strong master password: ").strip()
        create_new_vault(new_pw)
        return

    entries, fernet, salt = load_vault(master_pw)
    if entries is None:
        return

    while True:
        cmd_input = input("\n> ").strip()
        cmd_parts = cmd_input.split(maxsplit=1)
        cmd = cmd_parts[0].lower() if cmd_parts else ""

        if cmd == "quit":
            print("Goodbye.")
            break

        elif cmd == "add":
            site = input("Site/Service: ").strip()
            username = input("Username/Email: ").strip()
            password = getpass("Password: ").strip()
            entries.append({"site": site, "username": username, "password": password})
            save_vault(entries, fernet, salt)
            print("[+] Entry added and vault re-encrypted.")

        elif cmd == "list":
            if not entries:
                print("Vault is empty.")
                continue
            print("\nStored entries:")
            for i, e in enumerate(entries, 1):
                print(f"  {i}. {e['site']}  |  {e['username']}")

        elif cmd == "get":
            site = input("Site/Service to retrieve: ").strip().lower()
            found = [e for e in entries if site in e["site"].lower()]
            if not found:
                print("No matching entries.")
            for e in found:
                print(f"\nSite    : {e['site']}")
                print(f"Username: {e['username']}")
                print(f"Password: {e['password']}")

        elif cmd == "search":
            # Option B: accept term on same line or prompt if missing
            if len(cmd_parts) > 1:
                term = cmd_parts[1].strip().lower()
            else:
                term = input("Search term (site or username): ").strip().lower()

            if not term:
                print("No search term provided.")
                continue

            found = [e for e in entries if term in e["site"].lower() or term in e["username"].lower()]
            if not found:
                print("No matches.")
            else:
                print(f"\nFound {len(found)} match(es):")
                for e in found:
                    print(f"  • {e['site']} ({e['username']})")

        elif cmd == "delete":
            site = input("Site/Service to delete: ").strip().lower()
            before_len = len(entries)
            entries = [e for e in entries if site not in e["site"].lower()]
            if len(entries) < before_len:
                save_vault(entries, fernet, salt)
                print(f"[+] Deleted {before_len - len(entries)} entry(ies).")
            else:
                print("No matching entries to delete.")

        else:
            print("Unknown command. Try: add, list, get, search [term], delete, quit")

if __name__ == "__main__":
    main()