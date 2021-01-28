import sys
import socket
import ssl
import re



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



def main() -> None:
    print("Hello Main")



if __name__ == "__main__":
    main()
