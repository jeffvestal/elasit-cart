#!/usr/bin/env python3
"""
Quick script to check Bedrock model access
"""
import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError

def check_bedrock_access():
    print("🔍 Checking Bedrock Access...")
    print("=" * 50)
    
    try:
        # Create both clients
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        print(f"✅ AWS Credentials: OK")
        print(f"✅ Region: us-east-1")
        print()
        
        # List foundation models
        print("📋 Available Foundation Models:")
        response = bedrock.list_foundation_models()
        
        claude_models = []
        for model in response['modelSummaries']:
            if 'claude' in model['modelId'].lower():
                claude_models.append(model)
                print(f"  ✅ {model['modelId']}")
                print(f"     Status: {model.get('modelLifecycle', {}).get('status', 'Unknown')}")
                print()
        
        if not claude_models:
            print("❌ No Claude models found. You may need to request access.")
            print()
            
        # Test a simple model call with a common model
        print("🧪 Testing Model Access...")
        test_models = [
            "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "anthropic.claude-3-5-sonnet-20240620-v1:0", 
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-sonnet-4-5-20250929-v1:0"  # Your model
        ]
        
        for model_id in test_models:
            try:
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 10,
                    "messages": [{"role": "user", "content": "Hello"}]
                }
                
                response = bedrock_runtime.invoke_model(
                    modelId=model_id,
                    body=json.dumps(body),
                    contentType="application/json"
                )
                print(f"  ✅ {model_id} - ACCESSIBLE")
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'AccessDeniedException':
                    print(f"  ❌ {model_id} - NO ACCESS")
                elif error_code == 'ValidationException':
                    print(f"  ⚠️  {model_id} - INVALID MODEL ID")
                else:
                    print(f"  ❓ {model_id} - ERROR: {error_code}")
        
    except NoCredentialsError:
        print("❌ AWS Credentials not found!")
        print("   Check your ~/.aws/credentials file")
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"❌ AWS Error: {error_code}")
        print(f"   {e.response['Error']['Message']}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    check_bedrock_access()
