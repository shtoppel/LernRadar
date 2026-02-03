import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = "uploads"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # We force the server to look only in the uploads folder.
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Media server started at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()