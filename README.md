# LLM Agent with AWS Bedrock
A production-ready conversational AI agent built on AWS serverless infrastructure, featuring persistent memory, intelligent responses, and scalable architecture.

# Features
🤖 Intelligent Conversations: Powered by Amazon Bedrock's Claude model

💾 Persistent Memory: Stores conversation history in DynamoDB

🚀 Serverless Architecture: Auto-scaling with AWS Lambda and API Gateway

🔒 Secure: IAM role-based permissions and secure API endpoints

🌐 REST API: Easy integration with web/mobile applications

📊 Monitoring: Built-in CloudWatch logging and metrics

# Requirements
1. AWS Account with appropriate permissions

2. AWS CLI configured with credentials

3. AWS SAM CLI installed

4. Access to Amazon Bedrock (Claude model)

5. Python 3.8+

# AWS SAM Deployment

```

mkdir llm-agent-sam
cd llm-agent-sam
# Clone the git repo
# Build the application
sam build

# Deploy the configuration
sam deploy \
  --stack-name llm-agent-stack \
  --s3-bucket sam-deploy-1764459000-f28996da \
  --region us-east-1 \
  --capabilities CAPABILITY_IAM
```


