#!/usr/bin/env python3
"""QUANTUM API - REST API for quantum system access"""
import json
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

try:
    from quantum_universe_manager import QuantumUniverseManager
    from quantum_zone_teleporter import QuantumZoneTeleporter
    from quantum_analytics import QuantumAnalytics
    from quantum_encryption import QuantumEncryption
    QUANTUM_AVAILABLE = True
except ImportError:
    QUANTUM_AVAILABLE = False

class QuantumAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Quantum API"""
    
    def __init__(self, *args, **kwargs):
        if QUANTUM_AVAILABLE:
            self.universe_manager = QuantumUniverseManager()
            self.teleporter = QuantumZoneTeleporter()
            self.analytics = QuantumAnalytics()
            self.encryption = QuantumEncryption()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/status':
            self.send_status()
        elif path == '/api/universes':
            self.send_universes()
        elif path == '/api/analytics':
            self.send_analytics()
        elif path == '/api/metrics':
            self.send_metrics()
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/universe/create':
            self.create_universe(data)
        elif path == '/api/teleport':
            self.teleport_zone(data)
        elif path == '/api/encrypt':
            self.encrypt_data(data)
        elif path == '/api/decrypt':
            self.decrypt_data(data)
        else:
            self.send_error(404, "Endpoint not found")
    
    def send_status(self):
        """Send system status"""
        status = {
            'status': 'online',
            'quantum_available': QUANTUM_AVAILABLE,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        self.send_json_response(status)
    
    def send_universes(self):
        """Send list of universes"""
        if not QUANTUM_AVAILABLE:
            self.send_error(503, "Quantum system unavailable")
            return
        
        universes = self.universe_manager.list_universes()
        self.send_json_response({'universes': universes})
    
    def send_analytics(self):
        """Send analytics data"""
        if not QUANTUM_AVAILABLE:
            self.send_error(503, "Quantum system unavailable")
            return
        
        metrics = self.analytics.get_metrics()
        self.send_json_response({'analytics': metrics})
    
    def send_metrics(self):
        """Send current metrics"""
        if not QUANTUM_AVAILABLE:
            self.send_error(503, "Quantum system unavailable")
            return
        
        metrics = self.analytics.get_metrics()
        self.send_json_response({'metrics': metrics})
    
    def create_universe(self, data):
        """Create new universe"""
        if not QUANTUM_AVAILABLE:
            self.send_error(503, "Quantum system unavailable")
            return
        
        name = data.get('name', 'New Universe')
        description = data.get('description', '')
        
        universe_id = self.universe_manager.create_universe(name, description)
        
        response = {
            'success': True,
            'universe_id': universe_id,
            'name': name
        }
        self.send_json_response(response)
    
    def teleport_zone(self, data):
        """Teleport to zone"""
        if not QUANTUM_AVAILABLE:
            self.send_error(503, "Quantum system unavailable")
            return
        
        zone = data.get('zone')
        if not zone:
            self.send_error(400, "Zone required")
            return
        
        success = self.teleporter.instant_zone_jump(zone)
        
        response = {
            'success': success,
            'zone': zone,
            'timestamp': datetime.now().isoformat()
        }
        self.send_json_response(response)
    
    def encrypt_data(self, data):
        """Encrypt data with quantum key"""
        if not QUANTUM_AVAILABLE:
            self.send_error(503, "Quantum system unavailable")
            return
        
        plaintext = data.get('data')
        if not plaintext:
            self.send_error(400, "Data required")
            return
        
        result = self.encryption.quantum_encrypt(plaintext)
        self.send_json_response(result)
    
    def decrypt_data(self, data):
        """Decrypt data with quantum key"""
        if not QUANTUM_AVAILABLE:
            self.send_error(503, "Quantum system unavailable")
            return
        
        encrypted = data.get('encrypted')
        key_id = data.get('key_id')
        
        if not encrypted or not key_id:
            self.send_error(400, "Encrypted data and key_id required")
            return
        
        decrypted = self.encryption.quantum_decrypt(encrypted, key_id)
        
        response = {
            'success': decrypted is not None,
            'data': decrypted
        }
        self.send_json_response(response)
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Log API requests"""
        log_file = Path("logs/quantum/api.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"[{ts}] {format % args}\n"
        
        with open(log_file, 'a') as f:
            f.write(msg)

class QuantumAPI:
    def __init__(self, host='0.0.0.0', port=8888):
        self.host = host
        self.port = port
        self.server = None
    
    def start(self):
        """Start API server"""
        print(f"🌐 Starting Quantum API Server...")
        print(f"   Host: {self.host}")
        print(f"   Port: {self.port}")
        print(f"\n📡 API Endpoints:")
        print(f"   GET  /api/status")
        print(f"   GET  /api/universes")
        print(f"   GET  /api/analytics")
        print(f"   GET  /api/metrics")
        print(f"   POST /api/universe/create")
        print(f"   POST /api/teleport")
        print(f"   POST /api/encrypt")
        print(f"   POST /api/decrypt")
        print(f"\n✅ Server running at http://{self.host}:{self.port}")
        print(f"   Press Ctrl+C to stop\n")
        
        self.server = HTTPServer((self.host, self.port), QuantumAPIHandler)
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down API server...")
            self.server.shutdown()

if __name__ == "__main__":
    api = QuantumAPI(host='0.0.0.0', port=8888)
    api.start()
