import socket
import re
import ssl
import sys
from bs4 import BeautifulSoup
import urllib3 
from tinydb import TinyDB, Query

db = TinyDB('./cache.json')
# User = Query()

def send_http_request(host, port, path):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Establishing websocket connection:", host, port, path, '\n')

    if port == 443:
        client_socket = ssl.wrap_socket(client_socket)

    try:
        client_socket.settimeout(2)
        client_socket.connect((host, port))

        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        client_socket.send(request.encode())

        response = b""
        
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                response += data
            
            except socket.timeout:
                break

        resp_data = response.decode('utf-8', errors='ignore')

        # Check for 301 redirect
        while resp_data.startswith("HTTP/1.1 301") or resp_data.startswith("HTTP/1.1 302"):
            # Extract new URL from the Location header
            location_header = re.search(r'Location: (.+)\r\n', resp_data)
            if location_header:
                new_url = location_header.group(1)
                print(f"Received 301 Redirect. Redirecting to: {new_url}")
                # Parse new URL to get host, port, and path
                parsed_url = urllib3.util.parse_url(new_url)
                new_host = parsed_url.hostname
                new_port = parsed_url.port if parsed_url.port else 443
                new_path = '/search?q='+parameter
                # Recursively call send_http_request with the new URL
                return send_http_request(new_host, new_port, new_path)

        return resp_data
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    flag = sys.argv[1]
    if (sys.argv.__len__() > 2):
        parameter = sys.argv[2]
    else:
        parameter = ''
    # print (flag)

if (flag == "-u"):
    response = send_http_request('mechim.github.io', 443, '/')
    
if (flag == "-s"):
    # print (send_http_request('google.com', 443, '/search?q=cats'))
    response = send_http_request('google.com', 443, '/search?q='+parameter)
    http_info = response.split('<!doctype html>')[0]
    cache_obj = {'http_info': http_info}
    db.insert(cache_obj)
    
    soup = BeautifulSoup(response, 'html.parser')
    for h3 in soup.find_all('h3'):
        print(h3.get_text())

if (flag == "-h"):
    print("go2web -u <URL>         # make an HTTP request to the specified URL and print the response\ngo2web -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results\ngo2web -h               # show this help")