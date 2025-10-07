#!/usr/bin/env python3
"""
Test script to show exact DELETE URL construction
"""

import os
import asyncio
from dotenv import load_dotenv

# Add the current directory to path so we can import agent_builder_client
import sys
sys.path.insert(0, '.')

from agent_builder_client import AgentBuilderClient

async def test_delete_url():
    """Test and show the exact DELETE URL being constructed"""
    
    load_dotenv()
    
    kibana_url = os.getenv('KIBANA_URL', 'https://elasti-cart-b92fb1.kb.us-east-1.aws.elastic.cloud')
    api_key = os.getenv('KIBANA_API_KEY', 'test-key')
    
    print("🔧 DELETE URL Test")
    print("=" * 50)
    print(f"📍 Kibana URL: {kibana_url}")
    print(f"🔑 API Key (first 20): {api_key[:20]}...")
    print()
    
    # Test URL construction for each tool
    tool_names = [
        "search_grocery_items",
        "check_store_inventory", 
        "dietary_filter"
    ]
    
    for tool_name in tool_names:
        # Manually construct the URL like the delete_tool method does
        url = f"{kibana_url}/api/agent_builder/tools/{tool_name}"
        print(f"🗑️ DELETE URL for '{tool_name}':")
        print(f"   {url}")
        print()
    
    # Test with actual client
    print("🧪 Testing with AgentBuilderClient...")
    async with AgentBuilderClient(kibana_url, api_key) as client:
        print(f"✅ Client initialized")
        print(f"   kibana_url: {client.kibana_url}")
        print(f"   api_key: {client.api_key[:20]}...")
        
        # Show what the delete method would construct
        test_tool_id = "test_tool"
        expected_url = f"{client.kibana_url}/api/agent_builder/tools/{test_tool_id}"
        print(f"🔗 Expected DELETE URL: {expected_url}")

if __name__ == "__main__":
    asyncio.run(test_delete_url())
