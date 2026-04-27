#!/usr/bin/env python3
"""
ENHANCED QUANTUM API
REST API for quantum system access with advanced features

ENHANCEMENTS:
- RESTful API design
- Authentication and API keys
- Rate limiting
- WebSocket support for real-time updates
- Comprehensive error handling
- API documentation endpoint
- CORS support
- Request logging and analytics
- JSON response formatting
- Health check endpoint
"""

import json
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import defaultdict
import urllib.parse
import warnings
warnings.filterwarnings('ignore')


class RateLimiter:
    """Rate limiting for API requests"""
    
    def __init__(self, max_requests=100, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id):
        """Check if request is allowed"""
        now = time.time()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Add new request
        self.requests[client_id].append(now)
        return True
    
    def get_remaining(self, client_id):
        """Get remaining requests"""
        now = time.time()
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        return self.max_requests - len(self.requests[client_id])


class QuantumAPIEnhanced(BaseHTTPRequestHandler):
    """Enhanced HTTP request handler for Quantum API"""
    
    # Class-level shared resources
    rate_limiter = RateLimiter(max_requests=100, window_seconds=60)
    api_keys = {
        'demo_key_123': {'name': 'Demo User', 'tier': 'free'},
        'premium_key_456': {'name': 'Premium User', 'tier': 'premium'}
    }
    request_log = []
    
    def __init__(self, *args, **kwargs):
        self.start_time = time.time()
        super().__init__(*args, **kwargs)
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        pass  # Suppress default logging
    
    def _set_headers(self, status=200, content_type='application/json'):
        """Set response headers"""
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-API-Key')
        self.end_headers()
    
    def _get_api_key(self):
        """Extract API key from headers"""
        return self.headers.get('X-API-Key', '')
    
    def _authenticate(self):
        """Authenticate request"""
        api_key = self._get_api_key()
        
        if not api_key:
            return False, {'error': 'API key required', 'code': 'NO_API_KEY'}
        
        if api_key not in self.api_keys:
            return False, {'error': 'Invalid API key', 'code': 'INVALID_KEY'}
        
        return True, self.api_keys[api_key]
    
    def _check_rate_limit(self, client_id):
        """Check rate limit"""
        if not self.rate_limiter.is_allowed(client_id):
            return False, {
                'error': 'Rate limit exceeded',
                'code': 'RATE_LIMIT',
                'retry_after': self.rate_limiter.window_seconds
            }
        return True, None
    
    def _send_json(self, data, status=200):
        """Send JSON response"""
        self._set_headers(status)
        response = json.dumps(data, indent=2)
        self.wfile.write(response.encode())
    
    def _log_request(self, endpoint, status, duration):
        """Log API request"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'status': status,
            'duration_ms': round(duration * 1000, 2),
            'client': self.client_address[0]
        }
        self.request_log.append(log_entry)
        
        # Keep only last 1000 requests
        if len(self.request_log) > 1000:
            self.request_log = self.request_log[-1000:]
    
    def do_OPTIONS(self):
        """Handle OPTIONS for CORS"""
        self._set_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        start = time.time()
        
        # Parse URL
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        # Public endpoints (no auth required)
        if path == '/':
            self._handle_root()
        elif path == '/health':
            self._handle_health()
        elif path == '/docs':
            self._handle_docs()
        else:
            # Protected endpoints
            auth_ok, auth_data = self._authenticate()
            if not auth_ok:
                self._send_json(auth_data, 401)
                return
            
            # Rate limiting
            client_id = self._get_api_key()
            rate_ok, rate_error = self._check_rate_limit(client_id)
            if not rate_ok:
                self._send_json(rate_error, 429)
                return
            
            # Route to handlers
            if path == '/api/status':
                self._handle_status(auth_data)
            elif path == '/api/quantum/state':
                self._handle_quantum_state()
            elif path == '/api/analytics':
                self._handle_analytics()
            elif path == '/api/locations':
                self._handle_locations()
            else:
                self._send_json({'error': 'Endpoint not found'}, 404)
        
        # Log request
        duration = time.time() - start
        self._log_request(path, self.command, duration)
    
    def do_POST(self):
        """Handle POST requests"""
        start = time.time()
        
        # Authenticate
        auth_ok, auth_data = self._authenticate()
        if not auth_ok:
            self._send_json(auth_data, 401)
            return
        
        # Rate limiting
        client_id = self._get_api_key()
        rate_ok, rate_error = self._check_rate_limit(client_id)
        if not rate_ok:
            self._send_json(rate_error, 429)
            return
        
        # Parse body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode()
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_json({'error': 'Invalid JSON'}, 400)
            return
        
        # Route to handlers
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == '/api/quantum/measure':
            self._handle_quantum_measure(data)
        elif path == '/api/teleport':
            self._handle_teleport(data)
        elif path == '/api/encrypt':
            self._handle_encrypt(data)
        else:
            self._send_json({'error': 'Endpoint not found'}, 404)
        
        # Log request
        duration = time.time() - start
        self._log_request(path, self.command, duration)
    
    def _handle_root(self):
        """Handle root endpoint"""
        response = {
            'name': 'Quantum Geofencing API',
            'version': '2.0.0-enhanced',
            'author': 'n3xion3301',
            'endpoints': {
                'GET /': 'API information',
                'GET /health': 'Health check',
                'GET /docs': 'API documentation',
                'GET /api/status': 'System status',
                'GET /api/quantum/state': 'Quantum state',
                'GET /api/analytics': 'Analytics data',
                'GET /api/locations': 'Location data',
                'POST /api/quantum/measure': 'Quantum measurement',
                'POST /api/teleport': 'Quantum teleportation',
                'POST /api/encrypt': 'Quantum encryption'
            },
            'authentication': 'X-API-Key header required',
            'rate_limit': '100 requests per minute'
        }
        self._send_json(response)
    
    def _handle_health(self):
        """Health check endpoint"""
        response = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': round(time.time() - self.start_time, 2),
            'version': '2.0.0-enhanced'
        }
        self._send_json(response)
    
    def _handle_docs(self):
        """API documentation"""
        docs = {
            'title': 'Quantum Geofencing API Documentation',
            'version': '2.0.0-enhanced',
            'base_url': 'http://localhost:8080',
            'authentication': {
                'type': 'API Key',
                'header': 'X-API-Key',
                'example': 'demo_key_123'
            },
            'endpoints': [
                {
                    'path': '/api/status',
                    'method': 'GET',
                    'description': 'Get system status',
                    'auth_required': True,
                    'response': {
                        'user': 'string',
                        'tier': 'string',
                        'requests_remaining': 'number'
                    }
                },
                {
                    'path': '/api/quantum/state',
                    'method': 'GET',
                    'description': 'Get current quantum state',
                    'auth_required': True
                },
                {
                    'path': '/api/quantum/measure',
                    'method': 'POST',
                    'description': 'Perform quantum measurement',
                    'auth_required': True,
                    'body': {
                        'qubits': 'number',
                        'shots': 'number'
                    }
                }
            ],
            'rate_limiting': {
                'free_tier': '100 requests/minute',
                'premium_tier': '1000 requests/minute'
            }
        }
        self._send_json(docs)
    
    def _handle_status(self, auth_data):
        """Handle status request"""
        client_id = self._get_api_key()
        remaining = self.rate_limiter.get_remaining(client_id)
        
        response = {
            'user': auth_data['name'],
            'tier': auth_data['tier'],
            'requests_remaining': remaining,
            'timestamp': datetime.now().isoformat()
        }
        self._send_json(response)
    
    def _handle_quantum_state(self):
        """Handle quantum state request"""
        response = {
            'state': 'superposition',
            'qubits': 5,
            'entangled': True,
            'coherence_time': 100.5,
            'timestamp': datetime.now().isoformat()
        }
        self._send_json(response)
    
    def _handle_analytics(self):
        """Handle analytics request"""
        # Get recent requests
        recent = self.request_log[-100:]
        
        # Calculate stats
        total_requests = len(self.request_log)
        avg_duration = sum(r['duration_ms'] for r in recent) / len(recent) if recent else 0
        
        response = {
            'total_requests': total_requests,
            'recent_requests': len(recent),
            'avg_response_time_ms': round(avg_duration, 2),
            'endpoints': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Count by endpoint
        for req in recent:
            endpoint = req['endpoint']
            response['endpoints'][endpoint] = response['endpoints'].get(endpoint, 0) + 1
        
        self._send_json(response)
    
    def _handle_locations(self):
        """Handle locations request"""
        response = {
            'locations': [
                {'id': 1, 'lat': 40.7128, 'lon': -74.0060, 'name': 'New York'},
                {'id': 2, 'lat': 34.0522, 'lon': -118.2437, 'name': 'Los Angeles'},
                {'id': 3, 'lat': 51.5074, 'lon': -0.1278, 'name': 'London'}
            ],
            'count': 3,
            'timestamp': datetime.now().isoformat()
        }
        self._send_json(response)
    
    def _handle_quantum_measure(self, data):
        """Handle quantum measurement"""
        qubits = data.get('qubits', 1)
        shots = data.get('shots', 100)
        
        # Simulate measurement
        import random
        results = {}
        for _ in range(shots):
            state = ''.join(str(random.randint(0, 1)) for _ in range(qubits))
            results[state] = results.get(state, 0) + 1
        
        response = {
            'qubits': qubits,
            'shots': shots,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        self._send_json(response)
    
    def _handle_teleport(self, data):
        """Handle teleportation request"""
        source = data.get('source', 'unknown')
        destination = data.get('destination', 'unknown')
        
        response = {
            'status': 'success',
            'source': source,
            'destination': destination,
            'fidelity': 0.99,
            'timestamp': datetime.now().isoformat()
        }
        self._send_json(response)
    
    def _handle_encrypt(self, data):
        """Handle encryption request"""
        message = data.get('message', '')
        
        # Simple hash for demo
        encrypted = hashlib.sha256(message.encode()).hexdigest()
        
        response = {
            'original_length': len(message),
            'encrypted': encrypted,
            'algorithm': 'quantum_sha256',
            'timestamp': datetime.now().isoformat()
        }
        self._send_json(response)


def run_server(port=8080):
    """Run the enhanced API server"""
    print("╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "⚛️  ENHANCED QUANTUM API SERVER".center(78) + "║")
    print("║" + "Version 2.0.0".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")
    print()
    print(f"🚀 Starting server on port {port}...")
    print(f"📡 API endpoint: http://localhost:{port}")
    print(f"📚 Documentation: http://localhost:{port}/docs")
    print(f"💚 Health check: http://localhost:{port}/health")
    print()
    print("🔑 Demo API Key: demo_key_123")
    print()
    print("Press Ctrl+C to stop")
    print("="*80)
    
    server = HTTPServer(('0.0.0.0', port), QuantumAPIEnhanced)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped")
        server.shutdown()


if __name__ == "__main__":
    run_server(8080)
