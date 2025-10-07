#!/usr/bin/env python3
"""
Simple script to redeploy agents with updated tools
"""

import asyncio
import os
import sys

# Add the agent-builder-service to the path
sys.path.append('/Users/jeffvestal/repos/elasti-cart/agent-builder-service')

from agent_builder_client import AgentBuilderClient, GroceryAgentBuilder

async def redeploy_agents():
    """Redeploy agents with updated tool configurations"""
    
    # Check environment variables
    kibana_url = os.getenv('KIBANA_URL')
    kibana_api_key = os.getenv('KIBANA_API_KEY')
    
    if not kibana_url or not kibana_api_key:
        print("Error: KIBANA_URL and KIBANA_API_KEY environment variables must be set")
        return False
    
    print(f"Connecting to Kibana at: {kibana_url}")
    
    try:
        # Create client and builder
        async with AgentBuilderClient(kibana_url, kibana_api_key) as client:
            session_id = "elasti_cart_redeploy"
            builder = GroceryAgentBuilder(client, session_id)
            
            print("Deploying updated agents...")
            
            # First create all tools
            print("Creating tools...")
            tools_result = await builder.create_all_tools()
            print(f"✅ Created {len(tools_result)} tools")
            
            # Then create all agents  
            print("Creating agents...")
            agents_result = await builder.create_all_agents()
            print(f"✅ Created {len(agents_result)} agents")
            
            print("Agent deployment completed!")
            return True
            
    except Exception as e:
        print(f"Error during deployment: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(redeploy_agents())
    sys.exit(0 if success else 1)
