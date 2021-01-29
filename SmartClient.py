#!/usr/bin/env python3
import sys
import socket
import ssl
import re
import argparse
from http.cookies import SimpleCookie

"""
UVIC
CSC 361 Assignment 1
Scott Appleton
V00728931
"""




def createSocketConnection(url: str, use_https: bool):
    """
    Creates a connection using given url and option to use https
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
        print("Error forming socket connection.")
        sys.exit()

    # If we want to use https set port to 443 or use default 80
    if use_https:
        port = 443
    else:
        port = 80

    # connect socket to our url and given port
    try:
        s.connect((url, port))
    except socket.error:
        raise Exception


    if use_https:
        try:
            s = ssl.wrap_socket(s)
        except ssl.SSLError:
            raise Exception
    return s


def send_http_request(url: str, path: str, version: str, use_https: bool) -> str:
    """
    Sends HTTP request to given url and returns response string
    """

    s = createSocketConnection(url, use_https)
    request = (f"HEAD {path} HTTP/{version}\r\nHost: {url}\r\n\r\n").encode()
    s.sendall(request)


    

    # store into byte string
    res = b""
    while True:
        
        try:
            data = s.recv(4096)
            if not data:
                break
            res += data
        except socket.timeout:
            break
    return res.decode("utf-8")

def getStatus(response: str):
    """
    Get status code from response of a request
    """
    return int(re.search(r"^(HTTP/1.[0|1])\s(\d+)", response).group(2))


def checkHTTPS(url: str) -> str:
    """
    Determines if HTTPS is supported
    """
    path = "/"
    loc = url
    

    # Send a request and get the response back
    response = send_http_request(loc, path, "1.1", use_https=True)
    statusCode = getStatus(response)
    if statusCode in [200, 404, 503, 505]:
        return "yes", response
    else:
        print(f"Exiting due to status: {statusCode}")
        sys.exit()




def checkHttp2(url: str):
    """
    Check if http2 is supported
    """

    context = ssl.create_default_context()
    # Set up the order of the TCP protocols we want to try to use.
    context.set_alpn_protocols(['h2', 'spdy/3','http/1.1'])
    # Create our socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Here we connect our socket to our context settings for http2 default
    secure_socket = context.wrap_socket(s, server_hostname=url)
    secure_socket.connect((url, 443))
   
    return secure_socket.selected_alpn_protocol() == "h2"

def checkHttp1(url: str):
    """ 
    Check if Http1.1 is supported
    """
    # Create context settings to apply to socket
    context = ssl.create_default_context()
    context.set_alpn_protocols(['http/1.1', 'spdy/3' 'h2'])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    secure_socket = context.wrap_socket(s, server_hostname=url)
    secure_socket.connect((url, 443))
   
    if secure_socket.selected_alpn_protocol() == 'http/1.1':
        return True
    elif secure_socket.selected_alpn_protocol() == None:
        return True
    else:
        return False







def main() -> None:

    # Grab url from command line input

    socket.setdefaulttimeout(3)
    url = sys.argv[1]


    supportsHttp2 = checkHttp2(url)
    supportsHttp1 = checkHttp1(url)
    supportsHTTPS, res = checkHTTPS(url)

  

  
    # print(res)
   
    parsedCookies= []

    headers = res.split("\r\n")
    for item in headers:
        if "Set-Cookie" not in item:
            continue
        else:
            parsedCookies.append(item)

  
    print(parsedCookies)

    




    if supportsHttp1:
        supportsHttp1 = "yes"
    else:
        supportsHttp1 = "no"

    if supportsHttp2:
        supportsHttp2 = "yes"
    else:
        supportsHttp2 = "no"

    print(f"Website: {url}")
    print(f"Supports HTTPS: {supportsHTTPS}")
    print(f"Supports http1.1: {supportsHttp1}")
    print(f"Suports http2: {supportsHttp2}")
    print(f"Print out a list of cookies here:")


if __name__ == "__main__":
    main()
