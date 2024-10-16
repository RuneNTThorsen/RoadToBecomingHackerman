#!/bin/python3

import sys
import socket
from datetime import datetime


if len(sys.argv) == 2:
    target: str = socket.gethostbyname(sys.argv[1])
else:
    print("Invalid amount of arguments.")
    print("Syntax: python scanner.py <IP-address>")
    sys.exit()

print("-" * 50)
print("Scanning target " + target)
print("Time started: " + str(datetime.now))
print("-" * 50)

try:
    for port in range(50,85):
        s: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result: int = s.connect_ex((target, port))
        print("Checking port {}".format(port))
        if result == 0:
            print("Port {} is open".format(port))
        s.close()
except KeyBoardInterrupt:
    print("\nExiting program.")
    sys.exit()
except socket.gaierror:
    print("Hostname could not be resolved.")
    sys.exit()
except socket.error:
    print("Could not connect to server.")
    sys.exit()
