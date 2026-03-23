"""
SyntecXHub Internship - Project 1: TCP Port Scanner
Features: threaded scanning, port range, timeout handling, logging, basic service name lookup
Uses concurrent.futures for cleaner concurrency (modern Python approach)
"""

import socket
import concurrent.futures
import argparse
import sys
import time
from datetime import datetime

def get_service_name(port):
    """Try to get common service name for port (optional enhancement)"""
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"

def scan_port(target, port, timeout=1.0):
    """Scan a single port and return result tuple"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()

        if result == 0:
            service = get_service_name(port)
            return port, "open", service
        else:
            return port, "closed/timeout", "N/A"
    except Exception as e:
        return port, f"error ({str(e)})", "N/A"

def main():
    parser = argparse.ArgumentParser(description="Improved Threaded TCP Port Scanner")
    parser.add_argument("target", help="Target host (IP or domain name)")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=200, help="Max concurrent threads (default: 200)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout per port in seconds (default: 1.0)")
    parser.add_argument("--output", default="port_scan_results.txt", help="Log file (default: port_scan_results.txt)")
    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"[!] Error: Cannot resolve hostname '{args.target}'")
        sys.exit(1)

    print(f"\n[+] Scanning {args.target} ({target_ip}) | Ports {args.start}-{args.end}")
    print(f"[+] Using up to {args.threads} threads | Timeout: {args.timeout}s")
    print(f"[+] Results will be saved to: {args.output}\n")

    open_ports = []
    start_time = time.time()

    ports = range(args.start, args.end + 1)

    # Write header to log
    with open(args.output, "a", encoding="utf-8") as f:
        f.write(f"\n=== Scan started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        f.write(f"Target: {args.target} ({target_ip})\n")
        f.write(f"Ports: {args.start}-{args.end}\n\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_port = {executor.submit(scan_port, target_ip, port, args.timeout): port for port in ports}

        completed = 0
        total = len(ports)

        for future in concurrent.futures.as_completed(future_to_port):
            port, status, service = future.result()
            completed += 1

            msg = f"Port {port:>5} | {status:<12} | Service: {service}"
            print(msg)

            with open(args.output, "a", encoding="utf-8") as f:
                f.write(f"{msg}\n")

            if "open" in status:
                open_ports.append((port, service))

            # Simple progress
            if completed % 100 == 0 or completed == total:
                print(f"Progress: {completed}/{total} ({completed/total*100:.1f}%)")

    duration = time.time() - start_time
    print(f"\n[+] Scan finished in {duration:.2f} seconds")
    print(f"[+] Open ports found: {len(open_ports)}")

    if open_ports:
        print("\nOpen ports summary:")
        for port, service in sorted(open_ports):
            print(f"  • {port:>5} ({service})")

    with open(args.output, "a", encoding="utf-8") as f:
        f.write(f"\nScan completed in {duration:.2f}s | Open ports: {len(open_ports)}\n")

if __name__ == "__main__":
    main()