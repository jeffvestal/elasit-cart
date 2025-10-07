#!/usr/bin/env python3
"""
Simple working grocery data generator using your exact Bedrock pattern
"""
import boto3
import json
import os
from pathlib import Path

# Your working model ID
MODEL_ID = "arn:aws:bedrock:us-east-1:461485115270:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0"

def generate_grocery_items(count=5):
    """Generate grocery items using your working Bedrock pattern"""
    
    # Initialize Bedrock client exactly like your working script  
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1'
    )
    
    prompt = f"""Generate {count} realistic grocery items in JSON format. 
    Each item should have: name, brand, category, price, description.
    Return only valid JSON array, no markdown or extra text.
    
    Example format:
    [
      {{"name": "Organic Bananas", "brand": "Fresh Farm", "category": "Produce", "price": 2.99, "description": "Fresh organic bananas"}},
      {{"name": "Whole Milk", "brand": "Dairy Best", "category": "Dairy", "price": 3.49, "description": "Fresh whole milk"}}
    ]"""
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })
    
    print(f"🤖 Generating {count} grocery items with Claude Sonnet 4.5...")
    print(f"🔧 Model: {MODEL_ID}")
    print()
    
    try:
        # Invoke the model using your exact working pattern
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=body
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        result_text = response_body['content'][0]['text']
        
        print("✅ SUCCESS! Generated items:")
        print(result_text)
        
        # Save to file
        output_dir = Path("generated_data")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "grocery_items_simple.json"
        with open(output_file, 'w') as f:
            f.write(result_text)
            
        print(f"\n📁 Saved to: {output_file}")
        
        return result_text
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    # Default to 5 items, or use command line argument
    count = 5
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            print("Usage: python simple_grocery_generator.py [number_of_items]")
            sys.exit(1)
    
    generate_grocery_items(count)
