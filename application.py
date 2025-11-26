"""
WSGI entry point for AWS Elastic Beanstalk
This file is required by Elastic Beanstalk to deploy Flask applications
"""
from app import app as application

if __name__ == "__main__":
    application.run()

