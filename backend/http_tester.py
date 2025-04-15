import socket
from urllib.parse import urlparse

def send_http_request(url, method="GET", headers=None):
    parsed = urlparse(url)
    host = parsed.netloc
    path = parsed.path or "/"

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, 80))

        # Build header string
        header_lines = [
            f"{method} {path} HTTP/1.0",
            f"Host: {host}",
        ]

        if headers:
            for key, value in headers.items():
                header_lines.append(f"{key}: {value}")

        header_lines.append("\r\n")  # Ends headers
        request = "\r\n".join(header_lines)

        s.send(request.encode())

        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        s.close()

        decoded = response.decode(errors='ignore')
        header_end = decoded.find("\r\n\r\n")
        headers_text = decoded[:header_end]
        body = decoded[header_end+4:] if header_end != -1 else decoded

        status_line = headers_text.splitlines()[0]
        parts = status_line.split()
        status_code = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 0

        return {
            "status_code": status_code,
            "body": body
        }

    except Exception as e:
        return {
            "status_code": 0,
            "body": f"Error: {e}"
        }

# Example usage
if __name__ == "__main__":
    url = "http://example.com"
    print(send_http_request(url))
