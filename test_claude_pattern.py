#!/usr/bin/env python3
"""
Test Claude's exact pattern from the playground
"""
import boto3
import json

# Initialize Bedrock client exactly as Claude suggested
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

# Model ID from Claude's response (using your account ID)
model_id = "arn:aws:bedrock:us-east-1:461485115270:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0"

# Prepare the request exactly as Claude suggested
prompt = "Generate a JSON list with 2 grocery items including name and price."

body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
})

print("🧪 Testing Claude's exact pattern...")
print(f"Model ID: {model_id}")
print(f"Region: us-east-1")
print()

try:
    # Invoke the model exactly as Claude suggested
    response = bedrock.invoke_model(
        modelId=model_id,
        body=body
    )

    # Parse response
    response_body = json.loads(response['body'].read())
    print("✅ SUCCESS!")
    print("Response:")
    print(response_body['content'][0]['text'])
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()
    print("🔍 Let's try without the account ID in the ARN:")
    
    # Try the simpler ARN format
    simple_model_id = "arn:aws:bedrock:us-east-1::inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0"
    print(f"Trying: {simple_model_id}")
    
    try:
        response = bedrock.invoke_model(
            modelId=simple_model_id,
            body=body
        )
        response_body = json.loads(response['body'].read())
        print("✅ SUCCESS with simplified ARN!")
        print("Response:")
        print(response_body['content'][0]['text'])
        
    except Exception as e2:
        print(f"❌ Also failed: {e2}")
        print()
        print("🔍 Let's try just the inference profile ID:")
        
        # Try just the inference profile ID
        profile_id = "global.anthropic.claude-sonnet-4-5-20250929-v1:0"
        print(f"Trying: {profile_id}")
        
        try:
            response = bedrock.invoke_model(
                modelId=profile_id,
                body=body
            )
            response_body = json.loads(response['body'].read())
            print("✅ SUCCESS with profile ID!")
            print("Response:")
            print(response_body['content'][0]['text'])
            
        except Exception as e3:
            print(f"❌ All attempts failed: {e3}")
