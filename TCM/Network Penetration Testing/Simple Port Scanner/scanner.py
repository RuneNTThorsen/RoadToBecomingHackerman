#!/bin/python3

import sys
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, CancelledError


if len(sys.argv) == 2:
    target: str = socket.gethostbyname(sys.argv[1])
else:
    print("Invalid amount of arguments.")
    print("Syntax: python scanner.py <IP-address>")
    sys.exit()

now: datetime = datetime.now()
current_time: str = now.strftime("%H:%M:%S")

print("-" * 50)
print("Scanning target " + target)
print("Time started: " + current_time)
print("-" * 50)


def test_port(target: str, port: int):
    s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result: int = s.connect_ex((target, port))
    if result == 0:
        print("Port {} is open".format(port))
    s.close()


lower_bound: int = 50
upper_bound: int = 85

results: list = []

try:
    with ThreadPoolExecutor() as executor:
        futures: dict = {executor.submit(test_port, target, i): i for i in range(lower_bound, upper_bound)}
        print("\nFinding and printing open ports.\n\n")
        for future in as_completed(futures):
            try:
                future.result()
            except socket.gaierror:
                print("Hostname could not be resolved.")
                sys.exit()
            except socket.error:
                print("Could not connect to server.")
                sys.exit()
            except CancelledError:
                print("A scan of one of the ports was cancelled")
except KeyboardInterrupt:
    print("\nExiting program.")
    sys.exit()
