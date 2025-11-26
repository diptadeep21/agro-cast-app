# Deploying AgroCast to Netlify

## Prerequisites
- Netlify account (free tier is fine)
- OpenWeatherMap API key
- Git repository (GitHub, GitLab, or Bitbucket)

## Step 1: Set Environment Variable in Netlify

1. Go to your Netlify dashboard
2. Select your site (or create a new one)
3. Go to **Site settings** → **Environment variables**
4. Click **Add a variable**
5. Add:
   - **Key**: `OPENWEATHER_API_KEY`
   - **Value**: `9387b2f6efd6cbe56ff540d2322852f3` (or your API key)
6. Click **Save**

## Step 2: Connect Repository

1. In Netlify dashboard, click **Add new site** → **Import an existing project**
2. Connect your Git provider (GitHub, GitLab, or Bitbucket)
3. Select your repository
4. Netlify will auto-detect the settings from `netlify.toml`

## Step 3: Configure Build Settings

Netlify should automatically detect:
- **Publish directory**: `public`
- **Functions directory**: `netlify/functions`
- **Build command**: (none needed - static site)

If not, manually set:
- **Base directory**: (leave empty)
- **Build command**: `echo 'No build needed'`
- **Publish directory**: `public`

## Step 4: Deploy

1. Click **Deploy site**
2. Wait for deployment to complete
3. Your site will be live at `https://your-site-name.netlify.app`

## Step 5: Test Your Deployment

1. Visit your deployed site
2. Enter a city name (e.g., "London", "Mumbai")
3. Verify that:
   - Weather data loads correctly
   - Agriculture recommendations work
   - Crop recommendations appear

## Troubleshooting

### Functions Not Working
- Check that `OPENWEATHER_API_KEY` is set in environment variables
- Check Netlify function logs in the dashboard
- Verify function paths in browser console (should be `/.netlify/functions/...`)

### 404 Errors
- Ensure `netlify.toml` has the redirect rule: `from = "/*" to = "/index.html"`
- Check that `public/index.html` exists

### CORS Errors
- Functions should have `Access-Control-Allow-Origin: *` header (already included)

## Project Structure

```
weather-app/
├── netlify.toml              # Netlify configuration
├── public/                   # Static files (published)
│   ├── index.html           # Home page
│   └── result.html          # Results page
├── netlify/
│   └── functions/           # Serverless functions
│       ├── weather.py
│       ├── forecast.py
│       ├── agriculture-recommendation.py
│       ├── crop-recommendations.py
│       └── requirements.txt
└── .gitignore
```

## Functions

- `/.netlify/functions/weather` - Get current weather for a city
- `/.netlify/functions/forecast` - Get weather forecast
- `/.netlify/functions/agriculture-recommendation` - Get crop-specific recommendations
- `/.netlify/functions/crop-recommendations` - Get recommended crops for a city

## Notes

- The project uses Netlify Serverless Functions (Python) for backend API
- Frontend is static HTML/JavaScript
- All API calls are made from the frontend to Netlify functions
- Environment variables are securely stored in Netlify dashboard


