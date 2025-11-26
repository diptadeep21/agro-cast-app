# API Configuration Guide

## Problem: 404 Error on `/api/weather`

The frontend is trying to call Netlify Functions (`/.netlify/functions/weather/`), but you're deploying to AWS Amplify, which doesn't support Netlify Functions.

## Solution: Deploy Flask Backend Separately

Since AWS Amplify only serves static files, you need to deploy your Flask backend separately.

### Option 1: Deploy Flask Backend to Elastic Beanstalk (Recommended)

1. **Deploy Flask backend:**
   ```bash
   pip install awsebcli
   eb init -p python-3.8 agrocast-backend --region us-east-1
   eb setenv OPENWEATHER_API_KEY="your_api_key"
   eb create agrocast-backend-env
   eb deploy
   ```

2. **Get your backend URL:**
   ```bash
   eb status
   # Note the CNAME/URL (e.g., agrocast-backend-env.us-east-1.elasticbeanstalk.com)
   ```

3. **Configure Amplify to use backend URL:**
   - Go to AWS Amplify Console
   - Select your app
   - Go to **App settings** → **Environment variables**
   - Add: `API_URL` = `https://your-backend-url.elasticbeanstalk.com`
   - Save and redeploy

### Option 2: Deploy Flask Backend to ECS/Fargate

Follow the instructions in `AWS_DEPLOYMENT_GUIDE.md` for ECS deployment.

### Option 3: Use Same Domain (CORS Setup Required)

If you want frontend and backend on the same domain:
1. Deploy Flask backend to Elastic Beanstalk
2. Configure CloudFront/CDN to route:
   - `/api/*` → Flask backend
   - `/*` → Amplify static files

---

## API Endpoints

Your Flask backend now has these endpoints:

- `GET /api/weather?city=London` - Get weather data
- `GET /agriculture/recommendation?crop=Rice&temperature=25&humidity=70&rainfall=10` - Get agriculture recommendations
- `GET /agriculture/crop-recommendations?city=London` - Get recommended crops

---

## Testing Locally

1. **Start Flask backend:**
   ```bash
   export OPENWEATHER_API_KEY="your_key"
   python app.py
   # Backend runs on http://localhost:8080
   ```

2. **Test API endpoint:**
   ```bash
   curl "http://localhost:8080/api/weather?city=London"
   ```

3. **Update frontend locally (for testing):**
   - Edit `public/result.html`
   - Change `API_BASE` to: `const API_BASE = 'http://localhost:8080';`
   - Open `public/result.html` in browser

---

## Quick Fix for Current Error

The 404 error happens because:
1. Frontend calls `/.netlify/functions/weather/` 
2. Amplify doesn't have this endpoint
3. Flask backend isn't deployed yet

**Immediate fix:** Deploy Flask backend to Elastic Beanstalk and configure `API_URL` in Amplify.

