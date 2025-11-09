import json
import os
import requests
from http.server import BaseHTTPRequestHandler

def get_forecast(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        if response.status_code == 200:
            return { 'ok': True, 'data': data }
        else:
            message = data.get('message', 'Unable to fetch forecast') if isinstance(data, dict) else 'Unable to fetch forecast'
            return { 'ok': False, 'error': f"{response.status_code}: {message}" }
    except requests.Timeout:
        return { 'ok': False, 'error': 'Forecast request timed out.' }
    except Exception:
        return { 'ok': False, 'error': 'Unexpected error fetching forecast.' }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        api_key = os.environ.get('OPENWEATHER_API_KEY', '')
        if not api_key:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'API key is not configured'}).encode())
            return

        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        city = params.get('city', [''])[0]

        if not city:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'City is required'}).encode())
            return

        result = get_forecast(api_key, city)
        
        self.send_response(200 if result['ok'] else 502)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

