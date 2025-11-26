# AWS Deployment Guide for AgroCast

This guide provides step-by-step instructions for deploying the AgroCast application to Amazon Web Services (AWS) using multiple deployment methods.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Method 1: AWS Elastic Beanstalk (Easiest)](#method-1-aws-elastic-beanstalk-easiest)
3. [Method 2: AWS ECS with Fargate (Container-based)](#method-2-aws-ecs-with-fargate-container-based)
4. [Method 3: AWS EC2 with CodeDeploy (CI/CD)](#method-3-aws-ec2-with-codedeply-cicd)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- **AWS Account** with appropriate permissions
- **AWS CLI** installed and configured (`aws configure`)
- **OpenWeather API Key** (get one from [OpenWeatherMap](https://openweathermap.org/api))
- **Git** repository (if using CI/CD)
- **Docker** (for ECS deployment)

### Install AWS CLI

```bash
# macOS
brew install awscli

# Linux
pip install awscli

# Configure
aws configure
```

### Install EB CLI (for Elastic Beanstalk)

```bash
pip install awsebcli
```

---

## Method 1: AWS Elastic Beanstalk (Easiest)

Elastic Beanstalk is the simplest way to deploy a Flask application to AWS. It handles infrastructure provisioning, load balancing, and auto-scaling automatically.

### Step 1: Initialize Elastic Beanstalk

```bash
# Install EB CLI if not already installed
pip install awsebcli

# Initialize EB in your project directory
eb init -p python-3.8 agrocast-app --region us-east-1
```

When prompted:
- Select a region (e.g., `us-east-1`)
- Select/create an application name (e.g., `agrocast-app`)
- Confirm settings

### Step 2: Update Environment Configuration

Edit `.ebextensions/environment.config` and replace `YOUR_API_KEY_HERE` with your OpenWeather API key, or set it via EB CLI (recommended):

```bash
eb setenv OPENWEATHER_API_KEY="your_actual_api_key_here"
```

### Step 3: Create Environment

```bash
# Create a new environment (first time only)
eb create agrocast-env

# Or use existing environment
eb use agrocast-env
```

### Step 4: Deploy

```bash
# Deploy your application
eb deploy

# Open in browser
eb open
```

### Step 5: View Logs

```bash
# View recent logs
eb logs

# Stream logs in real-time
eb logs --stream
```

### Managing Your Deployment

```bash
# Check status
eb status

# View environment health
eb health

# SSH into EC2 instance
eb ssh

# Update environment variables
eb setenv OPENWEATHER_API_KEY="new_key"

# Terminate environment (when done)
eb terminate agrocast-env
```

### Using the Deployment Script

You can also use the provided deployment script:

```bash
cd aws-deployment
./deploy.sh
# Select option 1 for Elastic Beanstalk
```

---

## Method 2: AWS ECS with Fargate (Container-based)

ECS Fargate allows you to run containers without managing servers. This method uses Docker.

### Step 1: Create ECR Repository

```bash
# Set variables
REGION="us-east-1"
REPO_NAME="agrocast-app"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Create ECR repository
aws ecr create-repository \
    --repository-name $REPO_NAME \
    --region $REGION
```

### Step 2: Build and Push Docker Image

```bash
# Get login token and authenticate Docker
aws ecr get-login-password --region $REGION | \
    docker login --username AWS --password-stdin \
    $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Build Docker image
docker build -t agrocast-app .

# Tag image
docker tag agrocast-app:latest \
    $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest

# Push to ECR
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:latest
```

### Step 3: Create CloudWatch Log Group

```bash
aws logs create-log-group --log-group-name /ecs/agrocast-app --region $REGION
```

### Step 4: Create Task Definition

Update `aws-deployment/ecs-task-definition.json`:
- Replace `YOUR_ECR_REPOSITORY_URI` with your ECR URI
- Replace `YOUR_API_KEY_HERE` with your API key
- Adjust region in log configuration if needed

```bash
# Register task definition
aws ecs register-task-definition \
    --cli-input-json file://aws-deployment/ecs-task-definition.json \
    --region $REGION
```

### Step 5: Create ECS Cluster

```bash
aws ecs create-cluster --cluster-name agrocast-cluster --region $REGION
```

### Step 6: Create VPC and Networking (if needed)

If you don't have a VPC setup:

```bash
# Create VPC (or use existing)
# You'll need: VPC, Subnets, Security Group, Internet Gateway
# See AWS Console or use Terraform/CloudFormation
```

Update `aws-deployment/ecs-service-definition.json` with your:
- Subnet IDs
- Security Group ID
- Target Group ARN (if using ALB)

### Step 7: Create Service

```bash
aws ecs create-service \
    --cli-input-json file://aws-deployment/ecs-service-definition.json \
    --region $REGION
```

### Step 8: Access Your Application

```bash
# Get public IP of task
aws ecs list-tasks --cluster agrocast-cluster --region $REGION

# Get task details
aws ecs describe-tasks \
    --cluster agrocast-cluster \
    --tasks <task-arn> \
    --region $REGION
```

Or set up an Application Load Balancer (ALB) for better access.

### Using the Deployment Script

```bash
cd aws-deployment
./deploy.sh
# Select option 2 for ECS/Fargate
```

---

## Method 3: AWS EC2 with CodeDeploy (CI/CD)

This method sets up automated CI/CD pipeline using GitHub, CodePipeline, CodeBuild, and CodeDeploy.

### Step 1: Set Up EC2 Instance

1. Launch EC2 instance (Amazon Linux 2 or Ubuntu)
2. Security Group: Allow inbound on port 8080 (and SSH port 22)
3. Attach IAM role with CodeDeploy permissions

### Step 2: Install CodeDeploy Agent on EC2

**For Amazon Linux 2:**

```bash
sudo yum update -y
sudo yum install ruby -y
sudo yum install wget -y
cd /home/ec2-user
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent status
```

**For Ubuntu:**

```bash
sudo apt-get update
sudo apt-get install ruby wget -y
cd /home/ubuntu
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
chmod +x ./install
sudo ./install auto
sudo service codedeploy-agent status
```

### Step 3: Create S3 Bucket for Artifacts

```bash
aws s3 mb s3://agrocast-deployments-$(date +%s) --region us-east-1
```

### Step 4: Create CodeDeploy Application

```bash
aws deploy create-application \
    --application-name agrocast-app \
    --compute-platform Server \
    --region us-east-1
```

### Step 5: Create Deployment Group

```bash
# Tag your EC2 instance first
# Then create deployment group
aws deploy create-deployment-group \
    --application-name agrocast-app \
    --deployment-group-name agrocast-dg \
    --service-role-arn arn:aws:iam::ACCOUNT_ID:role/CodeDeployServiceRole \
    --ec2-tag-filters Key=Name,Value=agrocast-server,Type=KEY_AND_VALUE \
    --region us-east-1
```

### Step 6: Set Up CodeBuild Project

1. Go to AWS CodeBuild Console
2. Create new project:
   - Source: GitHub (connect repository)
   - Environment: Python 3.8
   - Buildspec: Use `buildspec.yml` from repository
   - Artifacts: S3 bucket created in Step 3

### Step 7: Set Up CodePipeline

1. Go to AWS CodePipeline Console
2. Create pipeline:
   - Source: GitHub (select repository and branch)
   - Build: CodeBuild project from Step 6
   - Deploy: CodeDeploy application from Step 4

### Step 8: Configure Environment Variables on EC2

Create `/etc/sysconfig/weather`:

```bash
sudo nano /etc/sysconfig/weather
```

Add:
```
OPENWEATHER_API_KEY=your_api_key_here
```

### Step 9: Test Deployment

Push a commit to trigger the pipeline, or manually deploy:

```bash
aws deploy create-deployment \
    --application-name agrocast-app \
    --deployment-group-name agrocast-dg \
    --s3-location bucket=YOUR_BUCKET,key=YOUR_KEY,bundleType=zip \
    --region us-east-1
```

### Using the Deployment Script

```bash
cd aws-deployment
./deploy.sh
# Select option 3 for EC2/CodeDeploy
```

---

## Environment Variables

All deployment methods require the `OPENWEATHER_API_KEY` environment variable.

### Setting in Elastic Beanstalk

```bash
eb setenv OPENWEATHER_API_KEY="your_key"
```

### Setting in ECS Task Definition

Edit `ecs-task-definition.json` environment section.

### Setting in EC2/CodeDeploy

Create `/etc/sysconfig/weather`:
```bash
OPENWEATHER_API_KEY=your_key
```

**⚠️ Security Note:** Never commit API keys to Git. Use environment variables or AWS Secrets Manager.

---

## Troubleshooting

### Elastic Beanstalk

**Issue: Application fails to start**
```bash
# Check logs
eb logs

# Common issues:
# - Missing environment variables
# - Port configuration issues
# - Python version mismatch
```

**Issue: 502 Bad Gateway**
- Check that the application is binding to `0.0.0.0:8080`
- Verify security group allows inbound on port 8080
- Check application health in EB console

### ECS/Fargate

**Issue: Task fails to start**
```bash
# Check CloudWatch logs
aws logs tail /ecs/agrocast-app --follow

# Common issues:
# - Incorrect ECR image URI
# - Missing environment variables
# - Insufficient CPU/memory
# - Security group blocking traffic
```

**Issue: Cannot pull image**
- Verify ECR repository permissions
- Check IAM role permissions
- Ensure image is tagged correctly

### EC2/CodeDeploy

**Issue: Deployment fails**
```bash
# Check CodeDeploy agent logs
sudo tail -f /var/log/aws/codedeploy-agent/codedeploy-agent.log

# Check application logs
sudo journalctl -u weather.service -f
```

**Issue: Service won't start**
```bash
# Check systemd service
sudo systemctl status weather.service
sudo systemctl restart weather.service

# Verify environment file
cat /etc/sysconfig/weather
```

---

## Cost Estimation

**Elastic Beanstalk:**
- EC2 instance: ~$10-50/month (t2.micro is free tier eligible)
- Data transfer: Pay per GB

**ECS Fargate:**
- Task: ~$15-30/month (0.25 vCPU, 0.5 GB RAM)
- Data transfer: Pay per GB
- ECR storage: ~$0.10/GB/month

**EC2 with CodeDeploy:**
- EC2 instance: ~$10-50/month
- CodePipeline: First 1000 executions free, then $1/pipeline/month
- CodeBuild: ~$0.005/minute
- CodeDeploy: Free for EC2 deployments

---

## Additional Resources

- [AWS Elastic Beanstalk Flask Documentation](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html)
- [ECS Fargate Getting Started](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-fargate.html)
- [AWS CodeDeploy User Guide](https://docs.aws.amazon.com/codedeploy/latest/userguide/)

---

## Next Steps

1. **Set up custom domain** using Route 53 and ALB
2. **Enable HTTPS** using AWS Certificate Manager
3. **Set up monitoring** with CloudWatch
4. **Configure auto-scaling** based on traffic
5. **Set up backups** and disaster recovery
6. **Use AWS Secrets Manager** for API keys (more secure)

---

For questions or issues, check the application logs and AWS CloudWatch logs.

