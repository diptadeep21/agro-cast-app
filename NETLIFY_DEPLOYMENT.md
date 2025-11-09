# Netlify Deployment Guide

## Important Note
**Netlify does not support Flask apps directly.** Netlify is designed for:
- Static websites
- Serverless functions (AWS Lambda)

Your Flask app needs to be converted to use Netlify Functions or deployed to a different platform.

## Option 1: Deploy to a Flask-Compatible Platform (Recommended)

### Recommended Platforms:
1. **Render** (https://render.com) - Free tier available
2. **Railway** (https://railway.app) - Free tier available  
3. **Fly.io** (https://fly.io) - Free tier available
4. **Heroku** (https://heroku.com) - Paid only now

### For Render:
1. Create account at render.com
2. Connect your GitHub repository
3. Create a new "Web Service"
4. Set environment variable: `OPENWEATHER_API_KEY=9387b2f6efd6cbe56ff540d2322852f3`
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`

## Option 2: Convert to Netlify Functions (Advanced)

This requires converting your Flask app to serverless functions. This is a significant rewrite.

## Setting Environment Variables in Netlify

If you proceed with Netlify Functions, set environment variables in Netlify Dashboard:

1. Go to your site in Netlify Dashboard
2. Go to **Site settings** → **Environment variables**
3. Add:
   - **Key**: `OPENWEATHER_API_KEY`
   - **Value**: `9387b2f6efd6cbe56ff540d2322852f3`

**Do NOT commit the .env file to git** - it contains sensitive API keys!

## Quick Answer for Netlify's .env Prompt

If Netlify is asking for .env file contents, paste:
```
OPENWEATHER_API_KEY=9387b2f6efd6cbe56ff540d2322852f3
```

But remember: This won't work for a Flask app without conversion to serverless functions.

