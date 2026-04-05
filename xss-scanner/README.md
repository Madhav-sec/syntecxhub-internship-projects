\# Task 2: Web Vulnerability Scanner (Reflected XSS)



\*\*Submitted by:\*\* Madhav  

\*\*Date:\*\* APRIL 2026  



A web vulnerability scanner that detects Reflected XSS vulnerabilities by injecting payloads into forms and analyzing responses.



\## Features

\- Crawls forms on target page

\- Injects common XSS payloads

\- Detects reflected XSS by checking response for payload execution

\- Logs findings to `xss\_scan\_results.log`

\- Rate limiting to avoid overwhelming the target



\## Tested On

\- DVWA (Damn Vulnerable Web Application) - Low Security

\- URL: http://localhost/vulnerabilities/xss\_r/



\## How to Run

```bash

python xss\_scanner.py

## Screenshots

All screenshots are available in the `screenshots/` folder:

- `scanner_start.png` — Scanner starting with target URL
- `forms_detected.png` — Forms found on the target page
- `vulnerability_detected.png` — Vulnerability found with payload
- `scan_summary.png` — Final scan summary
- `scan_log.png` — Log file showing recorded findings

