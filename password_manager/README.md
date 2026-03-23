SyntecXHub Internship - Project 2: Password Manager



Submitted by: Madhav  



Date: March 2026  



\# Project Overview

A secure local password manager that stores credentials encrypted on disk using strong symmetric encryption (Fernet: AES-128-CBC + HMAC-SHA256).  

Requires a master password to access / decrypt entries. All data is stored in `secure\_vault.enc` as encrypted JSON.



\# Features Implemented

\- Master password authentication

\- Secure key derivation (PBKDF2-SHA512 with 600,000 iterations + random salt)

\- Add new password entries

\- List all stored entries

\- Retrieve (get) full details of an entry

\- Search entries by site or username (partial match)

\- Delete entries

\- Encrypted local storage (JSON encrypted with Fernet)



\# How to Run

1\. Install dependency (once):

&nbsp;  bash

&nbsp;  pip install cryptography

