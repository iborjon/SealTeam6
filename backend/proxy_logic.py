import socket
import ssl
import time
from urllib.parse import urlparse

request_history = []
response_history = []

def handle_proxy_request(url, method="GET"):
    parsed = urlparse(url)
    host = parsed.netloc
    path = parsed.path or "/"
    scheme = parsed.scheme or "http"
    port = 443 if scheme == "https" else 80

    body_data = ""
    headers = {
        "Host": host,
        "Connection": "close",
        "User-Agent": "PythonProxy/1.0"
    }

    # Handle POST/PUT body (optional for GET)
    if method in ["POST", "PUT"]:
        body_data = '{"example":"data"}'  # placeholder; you can later receive this from the request
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = str(len(body_data))

    # Build header string
    header_str = f"{method} {path} HTTP/1.1\r\n"
    for key, value in headers.items():
        header_str += f"{key}: {value}\r\n"
    header_str += "\r\n"  # End headers
    request_line = header_str + body_data

    request_history.append({
        "timestamp": time.time(),
        "method": method,
        "url": url
    })

    try:
        raw_sock = socket.create_connection((host, port), timeout=5)

        if scheme == "https":
            context = ssl.create_default_context()
            sock = context.wrap_socket(raw_sock, server_hostname=host)
        else:
            sock = raw_sock

        sock.sendall(request_line.encode())

        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data
        sock.close()

        status_line = response.split(b"\r\n")[0]
        status_code = int(status_line.split()[1])

        # Redirect handling (301/302)
        if status_code in [301, 302]:
            headers = response.decode(errors='ignore').split("\r\n")
            for header in headers:
                if header.lower().startswith("location:"):
                    redirect_url = header.split(":", 1)[1].strip()
                    if not redirect_url.startswith("http"):
                        redirect_url = f"{scheme}://{host}{redirect_url}"
                    if redirect_url.startswith("https://") or redirect_url.startswith("http://"):
                        return handle_proxy_request(redirect_url, method)

        header_end = response.find(b"\r\n\r\n")
        body = response[header_end + 4:] if header_end != -1 else b""

        response_history.append({
            "timestamp": time.time(),
            "status": str(status_code),
            "url": url
        })

        return {
            "status_code": status_code,
            "body": body.decode(errors='ignore')[:300]
        }

    except Exception as e:
        return {"error": str(e)}
