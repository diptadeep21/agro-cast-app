#!/bin/bash

# AWS Deployment Script for AgroCast
# This script helps deploy the application to AWS using different methods

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}AgroCast AWS Deployment Script${NC}"
echo "=================================="
echo ""
echo "Select deployment method:"
echo "1) Elastic Beanstalk"
echo "2) ECS/Fargate"
echo "3) EC2 with CodeDeploy"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
  1)
    echo -e "${YELLOW}Deploying to Elastic Beanstalk...${NC}"
    
    # Check if EB CLI is installed
    if ! command -v eb &> /dev/null; then
        echo -e "${RED}EB CLI not found. Install it with: pip install awsebcli${NC}"
        exit 1
    fi
    
    # Initialize EB if not already done
    if [ ! -f ".elasticbeanstalk/config.yml" ]; then
        echo "Initializing Elastic Beanstalk..."
        eb init -p python-3.8 agrocast-app --region us-east-1
    fi
    
    # Create environment if it doesn't exist
    echo "Creating/updating environment..."
    eb create agrocast-env || eb use agrocast-env
    
    # Set environment variables
    read -p "Enter your OpenWeather API key: " api_key
    eb setenv OPENWEATHER_API_KEY="$api_key"
    
    # Deploy
    eb deploy
    
    echo -e "${GREEN}Deployment complete!${NC}"
    eb open
    ;;
    
  2)
    echo -e "${YELLOW}Deploying to ECS/Fargate...${NC}"
    
    # Check if AWS CLI is installed
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}AWS CLI not found. Please install it first.${NC}"
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker info &> /dev/null; then
        echo -e "${RED}Docker is not running. Please start Docker.${NC}"
        exit 1
    fi
    
    read -p "Enter AWS region (default: us-east-1): " region
    region=${region:-us-east-1}
    
    read -p "Enter ECR repository name (default: agrocast-app): " repo_name
    repo_name=${repo_name:-agrocast-app}
    
    read -p "Enter your OpenWeather API key: " api_key
    
    account_id=$(aws sts get-caller-identity --query Account --output text)
    ecr_uri="${account_id}.dkr.ecr.${region}.amazonaws.com/${repo_name}"
    
    echo "Building Docker image..."
    docker build -t agrocast-app .
    
    echo "Logging into ECR..."
    aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $ecr_uri
    
    echo "Creating ECR repository if it doesn't exist..."
    aws ecr describe-repositories --repository-names $repo_name --region $region 2>/dev/null || \
    aws ecr create-repository --repository-name $repo_name --region $region
    
    echo "Tagging and pushing image..."
    docker tag agrocast-app:latest ${ecr_uri}:latest
    docker push ${ecr_uri}:latest
    
    echo -e "${GREEN}Image pushed to ECR successfully!${NC}"
    echo "Next steps:"
    echo "1. Update ecs-task-definition.json with your ECR URI: ${ecr_uri}"
    echo "2. Update environment variable in task definition with your API key"
    echo "3. Register the task definition: aws ecs register-task-definition --cli-input-json file://aws-deployment/ecs-task-definition.json"
    echo "4. Create/update the service: aws ecs create-service --cli-input-json file://aws-deployment/ecs-service-definition.json"
    ;;
    
  3)
    echo -e "${YELLOW}Deploying to EC2 with CodeDeploy...${NC}"
    echo "See AWS_DEPLOYMENT_GUIDE.md for detailed instructions on setting up EC2 with CodeDeploy."
    echo ""
    echo "Quick steps:"
    echo "1. Set up EC2 instance with CodeDeploy agent"
    echo "2. Configure CodePipeline with GitHub source"
    echo "3. Set up CodeBuild project"
    echo "4. Configure CodeDeploy application"
    ;;
    
  *)
    echo -e "${RED}Invalid choice${NC}"
    exit 1
    ;;
esac

