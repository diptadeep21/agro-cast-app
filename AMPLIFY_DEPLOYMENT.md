# AWS Amplify Deployment Guide

## ⚠️ Important Note About Amplify

**AWS Amplify Hosting is designed for static websites and serverless functions**, not traditional Flask backends that run continuously. For a Flask application like AgroCast, you have two options:

1. **Use Elastic Beanstalk** (Recommended - see `AWS_QUICK_START.md`)
2. **Convert to serverless functions** (Complex - requires refactoring)

However, if you need to use Amplify, see the solution below.

---

## Quick Fix for Amplify Build Error

The error you're seeing is because Amplify is trying to run `npm install` but your project is Python-based. 

### Solution: Create `amplify.yml`

I've created an `amplify.yml` file that tells Amplify to:
- Install Python dependencies
- Skip Node.js build steps

**However, Amplify still won't run your Flask app as a continuous server.** You'll need to either:

### Option A: Use Elastic Beanstalk Instead (Recommended)

This is the easiest and most appropriate solution for Flask apps:

```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init -p python-3.8 agrocast-app --region us-east-1
eb setenv OPENWEATHER_API_KEY="your_api_key"
eb create agrocast-env
eb deploy
```

See `AWS_QUICK_START.md` for detailed instructions.

### Option B: Configure Amplify with Custom Build

If you must use Amplify, you can configure it to deploy to a different service (like ECS or Elastic Beanstalk) through a custom build script.

1. **Update `amplify.yml`** - Already created for you
2. **In AWS Amplify Console:**
   - Go to your app settings
   - Under "Build settings", select "Use a buildspec or amplify.yml file"
   - The `amplify.yml` file should be detected automatically
3. **Configure deployment target:**
   - You'll need to add deployment commands that push to Elastic Beanstalk or ECS
   - This is more complex than using EB directly

### Option C: Convert to Serverless (Advanced)

Convert your Flask routes to AWS Lambda functions. This requires significant refactoring:
- Each route becomes a separate Lambda function
- Use API Gateway for routing
- Requires rewriting the app structure

---

## Why the Error Occurred

The error message shows:
```
npm error enoent Could not read package.json
```

This happened because:
1. AWS Amplify defaults to building Node.js/JavaScript applications
2. It looks for `package.json` and runs `npm install`
3. Your project is Python-based and has no `package.json`
4. Amplify needs `amplify.yml` to know it's a Python project

---

## Next Steps

**Recommended:** Switch to Elastic Beanstalk for the easiest Flask deployment:
```bash
cd /path/to/your/project
pip install awsebcli
eb init -p python-3.8 agrocast-app
eb create agrocast-env
```

Or see the full guide in `AWS_DEPLOYMENT_GUIDE.md`.

---

## If You Must Use Amplify

The `amplify.yml` file I created will fix the build error, but you'll still need to:
1. Configure a backend service (ECS, EB, or Lambda)
2. Set up proper routing
3. Configure environment variables in Amplify Console

This is significantly more complex than using Elastic Beanstalk directly.

