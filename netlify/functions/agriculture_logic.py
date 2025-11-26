# Shared agriculture logic for Netlify functions

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
    
    # Rice: Needs high temp (20-35°C), high humidity (70-100%), good rainfall
    if crop == 'Rice':
        if t < 15:
            recommendation = 'Rice: Too cold — germination will be slow. Use nursery beds or delay sowing until temp rises above 18°C.'
        elif t > 38:
            recommendation = 'Rice: Extreme heat stress — provide shade netting for seedlings, increase irrigation frequency to 2-3 times daily.'
        elif h < 60:
            recommendation = 'Rice: Low humidity — increase irrigation to maintain field water level at 5-7 cm depth.'
        elif r < 5 and t > 28:
            recommendation = 'Rice: Hot and dry — critical irrigation needed. Maintain 5 cm standing water to prevent heat stress.'
        elif 20 <= t <= 32 and 70 <= h <= 95 and r >= 10:
            recommendation = 'Rice: Excellent conditions for transplanting or direct sowing. Maintain 5 cm water depth.'
        elif r > 25:
            recommendation = 'Rice: Heavy rainfall — ensure proper drainage. Delay nitrogen application to prevent leaching.'
        else:
            recommendation = 'Rice: Moderate conditions — maintain field water level and monitor for blast disease if humidity > 80%.'
    
    # Wheat: Cool season (10-25°C), moderate humidity (40-70%), low rainfall preferred
    elif crop == 'Wheat':
        if t > 30:
            recommendation = 'Wheat: Too hot — heat stress during grain filling. Avoid sowing; standing crop needs irrigation every 5-7 days.'
        elif t < 8:
            recommendation = 'Wheat: Too cold — slow growth. Use early-maturing varieties or delay sowing by 1-2 weeks.'
        elif h > 80:
            recommendation = 'Wheat: High humidity — high risk of rust and powdery mildew. Apply preventive fungicides.'
        elif r > 15:
            recommendation = 'Wheat: Excess moisture — delay sowing; ensure well-drained soil. Avoid waterlogging.'
        elif 12 <= t <= 22 and 40 <= h <= 65 and r < 10:
            recommendation = 'Wheat: Ideal sowing conditions — optimal temperature and moderate humidity for germination.'
        else:
            recommendation = 'Wheat: Suboptimal — if sowing, ensure good drainage and use disease-resistant varieties.'
    
    # Maize: Warm (18-32°C), moderate humidity (50-80%), moderate rainfall
    elif crop == 'Maize':
        if t < 15:
            recommendation = 'Maize: Cold stress — delayed germination. Wait for temperature above 18°C or use seed treatment.'
        elif t > 35:
            recommendation = 'Maize: Heat stress during pollination — critical irrigation needed at flowering stage to prevent yield loss.'
        elif h < 40 and t > 28:
            recommendation = 'Maize: Hot and dry — increase irrigation to 3-4 times weekly. Mulching recommended.'
        elif h > 85:
            recommendation = 'Maize: High humidity — monitor for downy mildew and leaf blight. Ensure good air circulation.'
        elif 20 <= t <= 30 and 50 <= h <= 75 and 5 <= r <= 20:
            recommendation = 'Maize: Good conditions for sowing — warm temperature with adequate moisture.'
        elif r > 25:
            recommendation = 'Maize: Heavy rain — delay sowing; waterlogging will damage roots. Ensure drainage.'
        else:
            recommendation = 'Maize: Moderate conditions — proceed with sowing if soil moisture is adequate.'
    
    # Cotton: Warm (20-35°C), moderate humidity (50-80%), moderate rainfall
    elif crop == 'Cotton':
        if t < 18:
            recommendation = 'Cotton: Cold conditions — delayed germination. Use seed treatment or delay by 10-15 days.'
        elif t > 38:
            recommendation = 'Cotton: Extreme heat — boll shedding risk. Increase irrigation frequency to daily during flowering.'
        elif h > 85:
            recommendation = 'Cotton: Very high humidity — high risk of bacterial blight and boll rot. Space plants wider for airflow.'
        elif h < 45 and t > 30:
            recommendation = 'Cotton: Hot and dry — critical irrigation needed. Target 6-8 irrigations during crop cycle.'
        elif 22 <= t <= 32 and 55 <= h <= 75 and 5 <= r <= 15:
            recommendation = 'Cotton: Optimal conditions — ideal for sowing with good boll development expected.'
        elif r > 20:
            recommendation = 'Cotton: Excess rain — delay sowing; waterlogging causes root rot. Ensure raised beds.'
        else:
            recommendation = 'Cotton: Suitable conditions — ensure adequate spacing and monitor for whitefly infestation.'
    
    # Sugarcane: Warm (20-35°C), high humidity (60-90%), high rainfall preferred
    elif crop == 'Sugarcane':
        if t < 18:
            recommendation = 'Sugarcane: Cold stress — slow ratooning. Delay planting until temperature rises above 20°C.'
        elif t > 38:
            recommendation = 'Sugarcane: Extreme heat — reduce tillering. Increase irrigation to maintain soil moisture.'
        elif h < 50 and t > 30:
            recommendation = 'Sugarcane: Hot and dry — critical irrigation needed. Maintain 60-70% soil moisture.'
        elif r < 5 and t > 28:
            recommendation = 'Sugarcane: Moisture deficit — increase irrigation frequency to weekly. Mulch recommended.'
        elif 24 <= t <= 32 and 65 <= h <= 85 and r >= 10:
            recommendation = 'Sugarcane: Excellent conditions — optimal for planting/ratooning with good cane growth expected.'
        else:
            recommendation = 'Sugarcane: Moderate conditions — maintain regular irrigation schedule.'
    
    # Sorghum (Jowar): Warm (20-35°C), moderate humidity (30-70%), drought tolerant
    elif crop == 'Sorghum (Jowar)':
        if t < 18:
            recommendation = 'Sorghum: Cold conditions — delayed emergence. Wait for temperature above 20°C.'
        elif t > 38:
            recommendation = 'Sorghum: Extreme heat — reduce irrigation to avoid waterlogging; drought-tolerant but needs some moisture.'
        elif h > 80:
            recommendation = 'Sorghum: High humidity — monitor for grain mold and anthracnose in panicle stage.'
        elif 22 <= t <= 32 and 40 <= h <= 65 and r < 15:
            recommendation = 'Sorghum: Ideal drought-tolerant conditions — good for rainfed or minimal irrigation.'
        else:
            recommendation = 'Sorghum: Suitable — drought-tolerant crop, proceed with sowing if soil has some moisture.'
    
    # Pearl Millet (Bajra): Hot (25-35°C), low humidity (20-60%), very drought tolerant
    elif crop == 'Pearl Millet (Bajra)':
        if t < 20:
            recommendation = 'Bajra: Too cold — germination will be poor. Wait for temperature above 22°C.'
        elif h > 70:
            recommendation = 'Bajra: High humidity — downy mildew risk. Use resistant varieties or treat seeds.'
        elif 25 <= t <= 35 and 30 <= h <= 55 and r < 10:
            recommendation = 'Bajra: Perfect conditions — ideal for this drought-tolerant crop. Minimal irrigation needed.'
        else:
            recommendation = 'Bajra: Suitable — very drought-tolerant, can proceed with sowing even in dry conditions.'
    
    # Pigeon Pea (Arhar): Warm (18-30°C), moderate humidity (40-80%), moderate rainfall
    elif crop == 'Pigeon Pea (Arhar)':
        if t < 15:
            recommendation = 'Arhar: Cold conditions — slow growth. Delay sowing until temperature rises above 18°C.'
        elif t > 32:
            recommendation = 'Arhar: Heat stress — flower drop may occur. Provide partial shade or increase irrigation.'
        elif h > 85:
            recommendation = 'Arhar: High humidity — wilt disease risk. Ensure well-drained soil and wider spacing.'
        elif 20 <= t <= 28 and 50 <= h <= 75 and 5 <= r <= 15:
            recommendation = 'Arhar: Good conditions — suitable for sowing with proper spacing for branching.'
        else:
            recommendation = 'Arhar: Moderate conditions — proceed with sowing, ensure good drainage.'
    
    # Chickpea (Chana): Cool (15-25°C), moderate humidity (30-60%), low rainfall preferred
    elif crop == 'Chickpea (Chana)':
        if t > 28:
            recommendation = 'Chana: Too hot — heat stress during pod filling. Avoid sowing; use early-maturing varieties if needed.'
        elif t < 10:
            recommendation = 'Chana: Too cold — slow growth. Wait for temperature above 12°C.'
        elif h > 70:
            recommendation = 'Chana: High humidity — ascochyta blight risk. Use treated seeds and resistant varieties.'
        elif r > 12:
            recommendation = 'Chana: Excess moisture — delay sowing; ensure well-drained soil to prevent root rot.'
        elif 15 <= t <= 22 and 35 <= h <= 55 and r < 8:
            recommendation = 'Chana: Ideal conditions — perfect for rabi sowing with good pod development expected.'
        else:
            recommendation = 'Chana: Suitable — proceed with sowing, ensure good drainage.'
    
    # Mustard: Cool (10-25°C), moderate humidity (30-70%), low rainfall
    elif crop == 'Mustard':
        if t > 28:
            recommendation = 'Mustard: Too hot — poor seed set. Avoid sowing; standing crop needs irrigation.'
        elif t < 8:
            recommendation = 'Mustard: Too cold — slow growth. Delay sowing until temperature above 10°C.'
        elif h > 75:
            recommendation = 'Mustard: High humidity — white rust and alternaria blight risk. Apply preventive sprays.'
        elif r > 10:
            recommendation = 'Mustard: Excess moisture — delay sowing; ensure drainage to prevent root diseases.'
        elif 12 <= t <= 22 and 40 <= h <= 65 and r < 8:
            recommendation = 'Mustard: Excellent conditions — ideal for rabi sowing with good oil content expected.'
        else:
            recommendation = 'Mustard: Suitable — proceed with sowing, monitor for aphids.'
    
    # Groundnut: Warm (20-30°C), moderate humidity (40-70%), moderate rainfall
    elif crop == 'Groundnut':
        if t < 18:
            recommendation = 'Groundnut: Cold conditions — poor germination. Wait for temperature above 20°C.'
        elif t > 35:
            recommendation = 'Groundnut: Heat stress — flower drop. Increase irrigation frequency to maintain soil moisture.'
        elif h > 80:
            recommendation = 'Groundnut: High humidity — leaf spot and rust risk. Use wider spacing and fungicides.'
        elif r > 20:
            recommendation = 'Groundnut: Excess rain — delay sowing; waterlogging causes pod rot. Ensure raised beds.'
        elif 22 <= t <= 28 and 45 <= h <= 65 and 5 <= r <= 15:
            recommendation = 'Groundnut: Good conditions — suitable for sowing with proper spacing for pegging.'
        else:
            recommendation = 'Groundnut: Moderate conditions — proceed with sowing, ensure good drainage.'
    
    # Soybean: Warm (20-30°C), moderate humidity (50-80%), moderate rainfall
    elif crop == 'Soybean':
        if t < 18:
            recommendation = 'Soybean: Cold conditions — slow emergence. Wait for temperature above 20°C.'
        elif t > 32:
            recommendation = 'Soybean: Heat stress — flower and pod drop. Increase irrigation during flowering.'
        elif h > 85:
            recommendation = 'Soybean: High humidity — bacterial blight and rust risk. Use resistant varieties.'
        elif 22 <= t <= 28 and 55 <= h <= 75 and 5 <= r <= 15:
            recommendation = 'Soybean: Optimal conditions — ideal for sowing with good nodulation expected.'
        else:
            recommendation = 'Soybean: Suitable — proceed with sowing, ensure proper seed inoculation.'
    
    # Barley: Cool (8-22°C), moderate humidity (30-60%), low rainfall
    elif crop == 'Barley':
        if t > 25:
            recommendation = 'Barley: Too hot — poor grain quality. Avoid sowing; use early varieties if needed.'
        elif t < 5:
            recommendation = 'Barley: Too cold — delayed emergence. Wait for temperature above 8°C.'
        elif h > 70:
            recommendation = 'Barley: High humidity — powdery mildew and rust risk. Apply preventive fungicides.'
        elif r > 12:
            recommendation = 'Barley: Excess moisture — delay sowing; ensure well-drained soil.'
        elif 10 <= t <= 20 and 35 <= h <= 55 and r < 8:
            recommendation = 'Barley: Ideal conditions — perfect for rabi sowing with good malting quality expected.'
        else:
            recommendation = 'Barley: Suitable — proceed with sowing, ensure good drainage.'
    
    # Tea: Moderate (18-28°C), high humidity (70-100%), high rainfall
    elif crop == 'Tea':
        if t < 15:
            recommendation = 'Tea: Cold stress — reduced growth. Protect young plants or delay planting.'
        elif t > 30:
            recommendation = 'Tea: Heat stress — sunscald on leaves. Provide shade netting or increase irrigation.'
        elif h < 60:
            recommendation = 'Tea: Low humidity — reduced quality. Increase irrigation to maintain humidity > 70%.'
        elif r < 8:
            recommendation = 'Tea: Moisture deficit — critical irrigation needed. Maintain 60-70% soil moisture.'
        elif 20 <= t <= 26 and 75 <= h <= 95 and r >= 10:
            recommendation = 'Tea: Excellent conditions — optimal for new flush growth with good quality expected.'
        else:
            recommendation = 'Tea: Moderate conditions — maintain regular irrigation and shade management.'
    
    # Coffee: Moderate (18-24°C), high humidity (60-90%), high rainfall
    elif crop == 'Coffee':
        if t > 26:
            recommendation = 'Coffee: Heat stress — berry drop. Provide shade trees or increase irrigation.'
        elif t < 15:
            recommendation = 'Coffee: Cold stress — delayed flowering. Protect plants or delay planting.'
        elif h < 55:
            recommendation = 'Coffee: Low humidity — reduced bean quality. Increase irrigation to maintain humidity.'
        elif r < 8:
            recommendation = 'Coffee: Moisture deficit — critical irrigation needed, especially during flowering.'
        elif 18 <= t <= 24 and 65 <= h <= 85 and r >= 10:
            recommendation = 'Coffee: Optimal conditions — ideal for flowering and berry development.'
        else:
            recommendation = 'Coffee: Suitable — maintain shade and regular irrigation schedule.'
    
    # Banana: Warm (20-35°C), high humidity (60-90%), high rainfall
    elif crop == 'Banana':
        if t < 18:
            recommendation = 'Banana: Cold stress — slow growth. Protect plants or delay planting.'
        elif t > 38:
            recommendation = 'Banana: Extreme heat — leaf scorch. Increase irrigation to daily and provide shade.'
        elif h < 55:
            recommendation = 'Banana: Low humidity — reduced bunch size. Increase irrigation frequency.'
        elif r < 8:
            recommendation = 'Banana: Moisture deficit — critical irrigation needed. Maintain 70-80% soil moisture.'
        elif 24 <= t <= 32 and 65 <= h <= 85 and r >= 10:
            recommendation = 'Banana: Excellent conditions — optimal for planting and bunch development.'
        else:
            recommendation = 'Banana: Suitable — maintain regular irrigation and wind protection.'
    
    # Potato: Cool (10-20°C), moderate humidity (40-80%), moderate rainfall
    elif crop == 'Potato':
        if t > 25:
            recommendation = 'Potato: Too hot — tuberization impaired. Avoid planting; use heat-tolerant varieties if needed.'
        elif t < 8:
            recommendation = 'Potato: Too cold — slow growth. Wait for temperature above 10°C.'
        elif h > 85:
            recommendation = 'Potato: High humidity — late blight risk. Apply preventive fungicides and ensure airflow.'
        elif r > 15:
            recommendation = 'Potato: Excess moisture — delay planting; waterlogging causes tuber rot. Ensure raised beds.'
        elif 12 <= t <= 20 and 50 <= h <= 75 and 5 <= r <= 12:
            recommendation = 'Potato: Ideal conditions — perfect for planting with good tuber development expected.'
        else:
            recommendation = 'Potato: Moderate conditions — proceed with planting, ensure good drainage.'
    
    # Onion: Moderate (13-25°C), moderate humidity (40-70%), low rainfall
    elif crop == 'Onion':
        if t > 28:
            recommendation = 'Onion: Too hot — bolting risk. Avoid planting; use short-day varieties if needed.'
        elif t < 10:
            recommendation = 'Onion: Too cold — slow growth. Wait for temperature above 13°C.'
        elif h > 75:
            recommendation = 'Onion: High humidity — purple blotch and downy mildew risk. Ensure good airflow.'
        elif r > 10:
            recommendation = 'Onion: Excess moisture — delay planting; waterlogging causes bulb rot.'
        elif 15 <= t <= 22 and 45 <= h <= 65 and r < 8:
            recommendation = 'Onion: Excellent conditions — ideal for planting with good bulb formation expected.'
        else:
            recommendation = 'Onion: Suitable — proceed with planting, ensure well-drained soil.'
    
    # Tomato: Moderate (18-28°C), moderate humidity (50-80%), moderate rainfall
    elif crop == 'Tomato':
        if t > 32:
            recommendation = 'Tomato: Heat stress — flower drop and fruit cracking. Provide shade netting or increase irrigation.'
        elif t < 15:
            recommendation = 'Tomato: Cold stress — poor fruit set. Use greenhouse or delay planting.'
        elif h > 85:
            recommendation = 'Tomato: High humidity — early blight and bacterial spot risk. Use wider spacing and fungicides.'
        elif r > 15:
            recommendation = 'Tomato: Excess rain — delay planting; waterlogging causes root rot. Ensure raised beds.'
        elif 20 <= t <= 26 and 55 <= h <= 75 and 5 <= r <= 12:
            recommendation = 'Tomato: Optimal conditions — ideal for planting with good fruit quality expected.'
        else:
            recommendation = 'Tomato: Moderate conditions — proceed with planting, provide support and monitor for pests.'

    # Fallback if crop not recognized
    if recommendation is None:
        recommendation = f'{crop}: Analyze temperature ({t}°C), humidity ({h}%), and rainfall ({r}mm) against crop-specific requirements before proceeding.'

    # Specialized suggestions
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
    elif crop in ['Chickpea (Chana)', 'Mustard', 'Barley'] and 12 <= t <= 22 and r < 10:
        sowing_window = 'Favorable rabi sowing window.'
    elif crop in ['Sorghum (Jowar)', 'Pearl Millet (Bajra)'] and 22 <= t <= 32 and r < 15:
        sowing_window = 'Favorable kharif sowing window.'

    pest_disease_risks = []
    if h > 85:
        pest_disease_risks.append('Fungal diseases likely — ensure field airflow and monitor leaves.')
    if crop == 'Cotton' and h > 75:
        pest_disease_risks.append('Whiteflies/aphids risk — inspect underside of leaves.')
    if crop == 'Rice' and 25 <= t <= 32 and h > 80:
        pest_disease_risks.append('Blast/BLB risk — maintain proper spacing and drainage.')
    if crop == 'Wheat' and h > 70:
        pest_disease_risks.append('Rust and powdery mildew risk — apply preventive fungicides.')
    if crop == 'Tomato' and h > 80:
        pest_disease_risks.append('Early blight risk — use wider spacing and copper-based fungicides.')

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


