#!/usr/bin/env python3
"""
Wiki Drop Webhook Server - HTTP endpoint for URL ingestion.

Accepts POST requests with a URL, adds to wiki ingestion queue.

Usage:
    python3 webhook-server.py [port]
    # Default port: 8765

POST /wiki-drop
    Content-Type: application/json
    {"url": "https://example.com/article", "source": "telegram", "message_id": 123}
    
    Or:
    curl -X POST http://localhost:8765/wiki-drop \
      -H "Content-Type: application/json" \
      -d '{"url":"https://example.com/article","source":"browser-extension"}'

GET /health
    Returns {"status":"ok","queue_size":N,"processed":N}
"""
import json, os, sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path

# Import queue helpers
sys.path.insert(0, str(Path(__file__).parent))
from ingest import add_to_queue, load_queue, load_processed

HOST = "0.0.0.0"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765

class WikiDropHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Quiet logging with timestamp."""
        ts = datetime.now().strftime("%H:%M:%S")
        sys.stderr.write(f"[{ts}] {args[0]} {args[1]} {args[2]}\n")
    
    def _send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
    
    def do_GET(self):
        if self.path == "/health":
            queue = load_queue()
            proc = load_processed()
            self._send_json(200, {
                "status": "ok",
                "queue_size": len([i for i in queue if i['status'] == 'pending']),
                "total_processed": len(proc.get('by_sha256', {})),
                "wiki_path": os.environ.get("WIKI_PATH", "/mnt/i/hermes/wiki"),
                "server_time": datetime.now().isoformat()
            })
        else:
            self._send_json(404, {"error": "not_found"})
    
    def do_POST(self):
        if self.path != "/wiki-drop":
            self._send_json(404, {"error": "not_found"})
            return
        
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self._send_json(400, {"error": "empty_body"})
                return
            
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            url = data.get("url", "").strip()
            if not url:
                self._send_json(400, {"error": "missing_url"})
                return
            
            source = data.get("source", "webhook")
            message_id = data.get("message_id")
            
            success = add_to_queue(url, source=source, message_id=message_id)
            
            if success:
                queue = load_queue()
                pending = len([i for i in queue if i['status'] == 'pending'])
                self._send_json(200, {
                    "status": "queued",
                    "url": url,
                    "pending_in_queue": pending
                })
            else:
                self._send_json(200, {
                    "status": "duplicate",
                    "url": url,
                    "message": "Already in queue or processed"
                })
                
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid_json"})
        except Exception as e:
            self._send_json(500, {"error": str(e)})
    
    def do_OPTIONS(self):
        """CORS preflight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def main():
    server = HTTPServer((HOST, PORT), WikiDropHandler)
    print(f"━━━ Wiki Drop Webhook ━━━")
    print(f"  Server:  http://{HOST}:{PORT}")
    print(f"  Endpoint: POST /wiki-drop")
    print(f"  Health:  GET  /health")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Send URLs via:")
    print(f"  curl -X POST http://localhost:{PORT}/wiki-drop \\")
    print(f"    -H 'Content-Type: application/json' \\")
    print(f"    -d '{{\"url\":\"https://...\",\"source\":\"manual\"}}'")
    print()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()

if __name__ == "__main__":
    main()
