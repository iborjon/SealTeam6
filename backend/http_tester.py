import socket
from urllib.parse import urlparse

def send_http_request(url, method="GET"):
    parsed = urlparse(url)
    host = parsed.netloc
    path = parsed.path or "/"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 80))

        request = f"{method} {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
        s.send(request.encode())

        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        s.close()
        return response.decode(errors='ignore')
    except Exception as e:
        return f"Error: {e}"

# Example usage
if __name__ == "__main__":
    url = "http://example.com"
    print(send_http_request(url))
