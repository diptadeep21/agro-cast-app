import json
import os
import requests

def handler(event, context):
    api_key = os.environ.get('OPENWEATHER_API_KEY', '')
    if not api_key:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'API key is not configured'})
        }

    # Parse query parameters
    city = event.get('queryStringParameters', {}).get('city', '') if event.get('queryStringParameters') else ''
    
    if not city:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'City is required'})
        }

    # Get weather data
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            result = { 'ok': True, 'data': data }
            status_code = 200
        else:
            message = data.get('message', 'Unable to fetch weather data') if isinstance(data, dict) else 'Unable to fetch weather data'
            result = { 'ok': False, 'error': f"{response.status_code}: {message}" }
            status_code = 502
    except requests.Timeout:
        result = { 'ok': False, 'error': 'Request timed out. Please try again.' }
        status_code = 504
    except Exception as e:
        result = { 'ok': False, 'error': 'Unexpected error fetching weather data.' }
        status_code = 500
    
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(result)
    }
