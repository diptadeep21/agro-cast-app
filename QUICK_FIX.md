# Quick Fix for Amplify Deployment Error

## The Problem

Your deployed site shows:
```
⚠️ Failed to fetch weather data: Unexpected token '<', "<!DOCTYPE "... is not valid JSON
/.netlify/functions/weather/?city=pune:1 Failed to load resource: 404
```

**Root Cause:** AWS Amplify only serves static files. It cannot run Flask backend or Netlify Functions. The frontend is trying to call an API that doesn't exist.

## Solution: Deploy Flask Backend Separately

You need to deploy your Flask backend to a service that can run Python, then point your frontend to it.

### Step 1: Deploy Flask Backend to Elastic Beanstalk (5 minutes)

```bash
# Install EB CLI
pip install awsebcli

# Initialize Elastic Beanstalk
cd /path/to/your/project
eb init -p python-3.8 agrocast-backend --region us-east-1

# Set your API key
eb setenv OPENWEATHER_API_KEY="your_openweather_api_key_here"

# Create and deploy
eb create agrocast-backend-env
eb deploy
```

### Step 2: Get Your Backend URL

```bash
eb status
```

Copy the CNAME URL (e.g., `agrocast-backend-env.us-east-1.elasticbeanstalk.com`)

### Step 3: Configure Amplify to Use Backend

1. Go to **AWS Amplify Console**
2. Select your app
3. Go to **App settings** → **Environment variables**
4. Click **Manage variables**
5. Add new variable:
   - **Key:** `API_URL`
   - **Value:** `https://your-backend-url.elasticbeanstalk.com` (use the URL from Step 2)
6. Click **Save**
7. Go to **App settings** → **Build settings**
8. Click **Edit**
9. Under **Environment variables**, make sure `API_URL` is listed
10. Click **Save**

### Step 4: Update Build Script to Inject API_URL

Update `amplify.yml` to inject the API_URL into your HTML:

```yaml
version: 1

frontend:
  env:
    variables:
      NODE_ENV: production
  phases:
    preBuild:
      commands:
        - echo "PreBuild phase - checking for submodules"
        - |
          if [ -f .gitmodules ]; then
            echo "Found .gitmodules, updating submodules..."
            git submodule update --init --recursive || echo "Submodule update failed, continuing..."
          else
            echo "No .gitmodules found, skipping submodule update"
          fi
    build:
      commands:
        - npm install
        - |
          # Inject API_URL into HTML files if set
          if [ -n "$API_URL" ]; then
            echo "Injecting API_URL: $API_URL"
            find public -name "*.html" -type f -exec sed -i.bak "s|<meta name=\"api-url\" content=\"\">|<meta name=\"api-url\" content=\"$API_URL\">|g" {} \;
            find public -name "*.bak" -delete
          fi
        - npm run build
  artifacts:
    baseDirectory: build
    files:
      - "**/*"
  cache:
    paths: []
```

### Step 5: Commit and Push

```bash
git add .
git commit -m "Fix: Configure frontend to use Flask backend API"
git push
```

Amplify will automatically rebuild with the new configuration.

### Step 6: Verify

1. Wait for Amplify build to complete
2. Visit your Amplify site
3. Enter a city name
4. It should now call your Flask backend API successfully!

---

## Alternative: Quick Test with Direct API Call

If you want to test immediately without deploying backend, you can temporarily modify `public/result.html` to call OpenWeather API directly (NOT recommended for production - exposes API key):

```javascript
// TEMPORARY FIX - Remove after deploying backend
const API_KEY = 'your_api_key_here'; // ⚠️ This exposes your key!
const weatherUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`;
```

**⚠️ Warning:** Never commit API keys to Git! This is only for testing.

---

## Why This Happens

- **AWS Amplify** = Static file hosting only (HTML, CSS, JS)
- **Flask Backend** = Needs a server to run Python
- **Solution** = Deploy Flask separately (Elastic Beanstalk/ECS) and connect frontend to it

---

## Need Help?

See `API_SETUP.md` for detailed instructions or `AWS_QUICK_START.md` for full deployment guide.

