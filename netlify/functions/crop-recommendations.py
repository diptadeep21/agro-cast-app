import json
import os
import requests

def average_conditions_from_forecast(forecast_data: dict):
    if not forecast_data or 'list' not in forecast_data:
        return { 'avgTemp': None, 'avgHumidity': None, 'avgRainfall': None }
    temps = []
    hums = []
    rains = []
    for item in forecast_data.get('list', [])[:24]:
        main = item.get('main', {})
        temps.append(main.get('temp'))
        hums.append(main.get('humidity'))
        rain_obj = item.get('rain', {})
        r = 0.0
        if isinstance(rain_obj, dict):
            r = rain_obj.get('3h') or rain_obj.get('1h') or 0.0
        rains.append(r)
    temps = [t for t in temps if isinstance(t, (int, float))]
    hums = [h for h in hums if isinstance(h, (int, float))]
    rains = [r for r in rains if isinstance(r, (int, float))]
    def avg(arr):
        return round(sum(arr)/len(arr), 1) if arr else None
    return { 'avgTemp': avg(temps), 'avgHumidity': avg(hums), 'avgRainfall': round(sum(rains), 1) if rains else None }

def recommend_crops_from_averages(avgTemp, avgHumidity, avgRainfall):
    crop_rules = [
        { 'name': 'Rice', 't': (20, 35), 'h': (70, 100), 'r_min': 15 },
        { 'name': 'Wheat', 't': (10, 25), 'h': (30, 70), 'r_min': 0 },
        { 'name': 'Maize', 't': (18, 32), 'h': (40, 80), 'r_min': 5 },
        { 'name': 'Cotton', 't': (20, 35), 'h': (40, 80), 'r_min': 5 },
        { 'name': 'Sugarcane', 't': (20, 35), 'h': (50, 90), 'r_min': 10 },
        { 'name': 'Sorghum (Jowar)', 't': (20, 35), 'h': (30, 70), 'r_min': 0 },
        { 'name': 'Pearl Millet (Bajra)', 't': (20, 35), 'h': (20, 60), 'r_min': 0 },
        { 'name': 'Pigeon Pea (Arhar)', 't': (18, 30), 'h': (40, 80), 'r_min': 5 },
        { 'name': 'Chickpea (Chana)', 't': (15, 25), 'h': (30, 60), 'r_min': 0 },
        { 'name': 'Mustard', 't': (10, 25), 'h': (30, 70), 'r_min': 0 },
        { 'name': 'Groundnut', 't': (20, 30), 'h': (40, 70), 'r_min': 5 },
        { 'name': 'Soybean', 't': (20, 30), 'h': (50, 80), 'r_min': 5 },
        { 'name': 'Barley', 't': (8, 22), 'h': (30, 60), 'r_min': 0 },
        { 'name': 'Tea', 't': (18, 28), 'h': (70, 100), 'r_min': 10 },
        { 'name': 'Coffee', 't': (18, 24), 'h': (60, 90), 'r_min': 10 },
        { 'name': 'Banana', 't': (20, 35), 'h': (60, 90), 'r_min': 10 },
        { 'name': 'Potato', 't': (10, 20), 'h': (40, 80), 'r_min': 0 },
        { 'name': 'Onion', 't': (13, 25), 'h': (40, 70), 'r_min': 0 },
        { 'name': 'Tomato', 't': (18, 28), 'h': (50, 80), 'r_min': 0 },
    ]
    recos = []
    for rule in crop_rules:
        t_ok = (avgTemp is not None) and (rule['t'][0] <= avgTemp <= rule['t'][1])
        h_ok = (avgHumidity is not None) and (rule['h'][0] <= avgHumidity <= rule['h'][1])
        r_ok = (avgRainfall is None) or (avgRainfall >= rule['r_min'])
        if t_ok and h_ok and r_ok:
            recos.append(rule['name'])
    return recos[:10]

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

def handler(event, context):
    api_key = os.environ.get('OPENWEATHER_API_KEY', '')
    
    params = event.get('queryStringParameters', {}) or {}
    city = params.get('city', '').strip()

    if not city:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'City is required'})
        }

    if not api_key:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'API key is not configured'})
        }

    f = get_forecast(api_key, city)
    if not f.get('ok'):
        return {
            'statusCode': 502,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': f.get('error', 'Failed to fetch forecast')})
        }

    averages = average_conditions_from_forecast(f.get('data'))
    recos = recommend_crops_from_averages(averages.get('avgTemp'), averages.get('avgHumidity'), averages.get('avgRainfall'))
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({ 'city': city, 'averages': averages, 'recommendedCrops': recos })
    }
