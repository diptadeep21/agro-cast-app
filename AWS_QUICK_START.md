# AWS Deployment Quick Start

## 🚀 Fastest Deployment: Elastic Beanstalk (5 minutes)

### Prerequisites
- AWS CLI configured (`aws configure`)
- EB CLI installed (`pip install awsebcli`)
- OpenWeather API key

### Steps

1. **Install EB CLI** (if not installed):
   ```bash
   pip install awsebcli
   ```

2. **Initialize Elastic Beanstalk**:
   ```bash
   eb init -p python-3.8 agrocast-app --region us-east-1
   ```

3. **Set API Key**:
   ```bash
   eb setenv OPENWEATHER_API_KEY="your_api_key_here"
   ```

4. **Create and Deploy**:
   ```bash
   eb create agrocast-env
   # OR if environment exists:
   eb use agrocast-env
   eb deploy
   ```

5. **Open in Browser**:
   ```bash
   eb open
   ```

That's it! Your app is live. 🎉

---

## 🐳 Docker Deployment: ECS Fargate

### Quick Steps

1. **Build and Push to ECR**:
   ```bash
   cd aws-deployment
   ./deploy.sh
   # Select option 2
   ```

2. **Or manually**:
   ```bash
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin \
     $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com

   # Build and push
   docker build -t agrocast-app .
   # ... (see AWS_DEPLOYMENT_GUIDE.md for full instructions)
   ```

---

## 📚 Full Documentation

See `AWS_DEPLOYMENT_GUIDE.md` for detailed instructions for all deployment methods.

---

## ⚠️ Important Notes

1. **API Key**: Never commit your API key to Git. Use environment variables.
2. **Costs**: Elastic Beanstalk t2.micro is free tier eligible for 12 months.
3. **Security**: Update security groups to only allow necessary ports.

---

## 🆘 Troubleshooting

**App won't start?**
```bash
eb logs  # Check logs for Elastic Beanstalk
```

**Need help?**
- Check `AWS_DEPLOYMENT_GUIDE.md` troubleshooting section
- Review AWS CloudWatch logs
- Verify environment variables are set correctly

