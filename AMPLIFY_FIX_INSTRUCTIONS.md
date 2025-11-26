# Fix for Amplify Build Error - Step by Step

## The Problem

AWS Amplify is trying to run `npm install` because it thinks your project is a Node.js app, but it's actually a Python Flask application.

## Solution Steps

### Step 1: Ensure `amplify.yml` is committed to Git

The `amplify.yml` file I created must be:
- ✅ In the root directory of your repository
- ✅ Committed to Git
- ✅ Pushed to GitHub

**Check if it's committed:**
```bash
git status
```

**If not committed, commit it:**
```bash
git add amplify.yml
git commit -m "Add amplify.yml to fix Python build configuration"
git push
```

### Step 2: Configure Amplify Console to Use the File

1. Go to **AWS Amplify Console**
2. Select your app (agrocast-app)
3. Go to **App settings** → **Build settings**
4. Click **Edit**
5. Make sure it says **"Use a buildspec or amplify.yml file"**
6. Verify it shows: `amplify.yml` or `amplify.yml (detected)`
7. If it doesn't, select **"amplify.yml"** from the dropdown
8. Click **Save**

### Step 3: Re-run the Build

After pushing the file and configuring Amplify:

1. Go to your Amplify app
2. Click **Redeploy this version** or push a new commit
3. The build should now use `amplify.yml` instead of trying `npm install`

---

## Alternative: Quick Test

If you want to verify the file works immediately:

1. **Commit and push `amplify.yml`:**
   ```bash
   git add amplify.yml
   git commit -m "Fix: Add amplify.yml for Python build"
   git push
   ```

2. **In Amplify Console:**
   - The build should automatically trigger
   - Check the build logs - you should see "Skipping npm install" instead of the npm error

---

## Why This Happens

AWS Amplify has default build behaviors:
- If no `amplify.yml` is found → tries to auto-detect project type
- If it sees common frontend files → assumes Node.js and runs `npm install`
- Your Python project has no `package.json`, so `npm install` fails

By adding `amplify.yml`, you explicitly tell Amplify:
- "This is NOT a Node.js project"
- "Skip npm install"
- "Install Python dependencies instead"

---

## Still Getting Errors?

If the error persists after committing and pushing `amplify.yml`:

1. **Verify file location:**
   ```bash
   # Should show amplify.yml in root
   ls -la | grep amplify
   ```

2. **Check Amplify Console settings:**
   - Build settings must point to `amplify.yml`
   - Not using "Override build settings" that ignores the file

3. **Clear build cache:**
   - In Amplify Console → App settings → Build settings
   - Click "Clear cache" before next build

4. **Verify file format:**
   - File must be valid YAML
   - No syntax errors
   - Starts with `version: 1`

---

## Important Note

⚠️ **Even after fixing the build, Amplify Hosting cannot run Flask servers!**

Amplify Hosting is for:
- ✅ Static websites
- ✅ Serverless functions (Lambda)

Amplify Hosting is NOT for:
- ❌ Traditional web servers (Flask, Django, Express)
- ❌ Long-running processes

**For your Flask app, use AWS Elastic Beanstalk:**
```bash
pip install awsebcli
eb init -p python-3.8 agrocast-app
eb setenv OPENWEATHER_API_KEY="your_key"
eb create agrocast-env
eb deploy
```

See `AWS_QUICK_START.md` for full instructions.

