#!/usr/bin/env python3
"""
Direct test within our grocery-data-generator environment
Using your exact working pattern
"""
import asyncio
import sys
import os
from pathlib import Path

# Add lib directory to path
lib_path = Path(__file__).parent / "lib"
sys.path.insert(0, str(lib_path))

from llm_client import LLMClient

async def test_your_exact_pattern():
    print("🧪 Testing your exact working pattern...")
    
    # Use your exact working ARN
    model_id = "arn:aws:bedrock:us-east-1:461485115270:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0"
    
    print(f"Model ID: {model_id}")
    print()
    
    try:
        # Initialize our LLM client
        llm_client = LLMClient(provider="bedrock", model=model_id, region="us-east-1")
        await llm_client.initialize()
        
        print("✅ LLM client initialized successfully")
        
        # Test a simple generation
        response = await llm_client.generate_text(
            "Generate a JSON object with 2 grocery items including name and price.", 
            max_tokens=200
        )
        
        print("✅ SUCCESS!")
        print("Response:")
        print(response)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        
        # Let's also test the direct boto3 pattern like your script
        print("🔄 Testing direct boto3 pattern (like your working script)...")
        
        import boto3
        import json
        
        try:
            bedrock = boto3.client(
                service_name='bedrock-runtime',
                region_name='us-east-1'
            )
            
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 200,
                "messages": [
                    {
                        "role": "user",
                        "content": "Generate a JSON object with 2 grocery items including name and price."
                    }
                ]
            })
            
            response = bedrock.invoke_model(
                modelId=model_id,
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            print("✅ Direct boto3 pattern works!")
            print("Response:")
            print(response_body['content'][0]['text'])
            
        except Exception as e2:
            print(f"❌ Direct boto3 also failed: {e2}")

if __name__ == "__main__":
    asyncio.run(test_your_exact_pattern())
