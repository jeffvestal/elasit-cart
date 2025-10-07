#!/usr/bin/env python3
"""
Test script to show complete HTTP DELETE request details
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv

async def test_delete_request():
    """Test and show the complete HTTP DELETE request details"""
    
    load_dotenv()
    
    kibana_url = os.getenv('KIBANA_URL', 'https://elasti-cart-b92fb1.kb.us-east-1.aws.elastic.cloud')
    api_key = os.getenv('KIBANA_API_KEY', 'test-key')
    
    print("🔧 Complete HTTP DELETE Request Details")
    print("=" * 60)
    print(f"📍 Kibana URL: {kibana_url}")
    print(f"🔑 API Key (first 20): {api_key[:20]}...")
    print()
    
    # Test tool
    tool_id = "dietary_filter"
    url = f"{kibana_url}/api/agent_builder/tools/{tool_id}"
    
    headers = {
        "Authorization": f"ApiKey {api_key}",
        "Content-Type": "application/json",
        "kbn-xsrf": "reporting"
    }
    
    print("📤 HTTP DELETE Request:")
    print(f"   Method: DELETE")
    print(f"   URL: {url}")
    print(f"   Headers:")
    for key, value in headers.items():
        if key == "Authorization":
            print(f"     {key}: ApiKey {api_key[:20]}...")
        else:
            print(f"     {key}: {value}")
    print()
    
    # Test the actual request (but don't fail on auth errors)
    print("🧪 Testing actual HTTP request...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                print(f"📥 Response Status: {response.status}")
                print(f"📥 Response Reason: {response.reason}")
                print(f"📥 Response Headers:")
                for key, value in response.headers.items():
                    print(f"     {key}: {value}")
                
                response_text = await response.text()
                print(f"📄 Response Body: {response_text[:200]}...")
                
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_delete_request())
