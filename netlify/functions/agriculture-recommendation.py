import json
import os
import requests

# Include agriculture logic directly in the function
def build_agriculture_recommendation(crop: str, temperature: float, humidity: float, rainfall: float):
    alerts = []
    try:
        t = float(temperature)
        h = float(humidity)
        r = float(rainfall)
    except Exception:
        t, h, r = 0.0, 0.0, 0.0

    if h > 85:
        alerts.append('High humidity — fungal disease risk')
    if t <= 2:
        alerts.append('Frost risk ahead')
    if t >= 40:
        alerts.append('Extreme heat — heat stress risk')

    recommendation = None
    
    # Crop-specific logic (simplified - includes main crops)
    if crop == 'Rice':
        if t < 15:
            recommendation = 'Rice: Too cold — germination will be slow. Use nursery beds or delay sowing until temp rises above 18°C.'
        elif t > 38:
            recommendation = 'Rice: Extreme heat stress — provide shade netting for seedlings, increase irrigation frequency to 2-3 times daily.'
        elif h < 60:
            recommendation = 'Rice: Low humidity — increase irrigation to maintain field water level at 5-7 cm depth.'
        elif 20 <= t <= 32 and 70 <= h <= 95 and r >= 10:
            recommendation = 'Rice: Excellent conditions for transplanting or direct sowing. Maintain 5 cm water depth.'
        else:
            recommendation = 'Rice: Moderate conditions — maintain field water level and monitor for blast disease if humidity > 80%.'
    elif crop == 'Wheat':
        if t > 30:
            recommendation = 'Wheat: Too hot — heat stress during grain filling. Avoid sowing; standing crop needs irrigation every 5-7 days.'
        elif t < 8:
            recommendation = 'Wheat: Too cold — slow growth. Use early-maturing varieties or delay sowing by 1-2 weeks.'
        elif 12 <= t <= 22 and 40 <= h <= 65 and r < 10:
            recommendation = 'Wheat: Ideal sowing conditions — optimal temperature and moderate humidity for germination.'
        else:
            recommendation = 'Wheat: Suboptimal — if sowing, ensure good drainage and use disease-resistant varieties.'
    elif crop == 'Maize':
        if t < 15:
            recommendation = 'Maize: Cold stress — delayed germination. Wait for temperature above 18°C or use seed treatment.'
        elif t > 35:
            recommendation = 'Maize: Heat stress during pollination — critical irrigation needed at flowering stage to prevent yield loss.'
        elif 20 <= t <= 30 and 50 <= h <= 75 and 5 <= r <= 20:
            recommendation = 'Maize: Good conditions for sowing — warm temperature with adequate moisture.'
        else:
            recommendation = 'Maize: Moderate conditions — proceed with sowing if soil moisture is adequate.'
    else:
        # Generic recommendation for other crops
        if t < 10:
            recommendation = f'{crop}: Too cold — wait for warmer conditions.'
        elif t > 35:
            recommendation = f'{crop}: Too hot — provide shade or increase irrigation.'
        elif h > 85:
            recommendation = f'{crop}: High humidity — monitor for fungal diseases.'
        else:
            recommendation = f'{crop}: Analyze temperature ({t}°C), humidity ({h}%), and rainfall ({r}mm) against crop-specific requirements.'

    if recommendation is None:
        recommendation = f'{crop}: Analyze temperature ({t}°C), humidity ({h}%), and rainfall ({r}mm) against crop-specific requirements before proceeding.'

    irrigation = 'Maintain current irrigation schedule.'
    if r < 3 and t > 32:
        irrigation = 'Increase irrigation frequency due to hot and dry conditions.'
    elif r >= 10:
        irrigation = 'Delay irrigation — sufficient recent rainfall.'
    elif r < 5 and t > 28:
        irrigation = 'Moderate irrigation needed — maintain soil moisture.'

    fertilizer = 'Apply NPK as per schedule.'
    if r >= 10:
        fertilizer = 'Avoid nitrogen today — rain may leach nutrients.'
    elif h > 85:
        fertilizer = 'Delay foliar sprays — high humidity can reduce efficacy.'
    elif t > 30:
        fertilizer = 'Reduce nitrogen during heat stress — focus on potassium for stress tolerance.'

    sowing_window = 'Neutral'
    if crop == 'Rice' and 20 <= t <= 35 and r > 10:
        sowing_window = 'Favorable for sowing/transplanting.'
    elif crop == 'Wheat' and 10 <= t <= 25 and r < 10:
        sowing_window = 'Favorable cool and relatively dry window.'
    elif crop == 'Maize' and 18 <= t <= 30 and r >= 5:
        sowing_window = 'Favorable — warm with some moisture.'

    pest_disease_risks = []
    if h > 85:
        pest_disease_risks.append('Fungal diseases likely — ensure field airflow and monitor leaves.')
    if crop == 'Cotton' and h > 75:
        pest_disease_risks.append('Whiteflies/aphids risk — inspect underside of leaves.')
    if crop == 'Rice' and 25 <= t <= 32 and h > 80:
        pest_disease_risks.append('Blast/BLB risk — maintain proper spacing and drainage.')

    post_harvest = None
    if h < 60 and r == 0:
        post_harvest = 'Good window for harvesting/drying — low humidity and no rain.'

    return {
        'crop': crop,
        'recommendation': recommendation,
        'alerts': alerts,
        'irrigation': irrigation,
        'fertilizer': fertilizer,
        'sowingWindow': sowing_window,
        'pestDiseaseRisks': pest_disease_risks,
        'postHarvest': post_harvest
    }

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
    except Exception:
        return { 'ok': False, 'error': 'Unexpected error fetching forecast.' }

def handler(event, context):
    api_key = os.environ.get('OPENWEATHER_API_KEY', '')
    
    params = event.get('queryStringParameters', {}) or {}
    crop = params.get('crop', '').strip()
    temperature = params.get('temperature')
    humidity = params.get('humidity')
    rainfall = params.get('rainfall')
    city = params.get('city', '').strip()

    try:
        temperature = float(temperature) if temperature else None
        humidity = float(humidity) if humidity else None
        rainfall = float(rainfall) if rainfall else None
    except (ValueError, TypeError):
        temperature = None
        humidity = None
        rainfall = None

    if not crop or temperature is None or humidity is None:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Missing required parameters: crop, temperature, humidity'})
        }

    used_rainfall = rainfall if rainfall is not None else 0.0
    if (rainfall is None or rainfall == 0.0) and city and api_key:
        f = get_forecast(api_key, city)
        if f.get('ok'):
            av = average_conditions_from_forecast(f.get('data'))
            if av.get('avgRainfall') is not None:
                used_rainfall = float(av.get('avgRainfall'))
    
    if used_rainfall is None:
        used_rainfall = 0.0

    result = build_agriculture_recommendation(crop, temperature, humidity, used_rainfall)
    result['usedRainfall'] = used_rainfall
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(result)
    }
