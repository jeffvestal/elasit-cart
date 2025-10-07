#!/usr/bin/env python3
"""
Deploy updated agents with better price range logic
"""

import asyncio
import os
import sys
sys.path.append('/Users/jeffvestal/repos/elasti-cart/agent-builder-service')

from agent_builder_client import GroceryAgentBuilder, AgentBuilderClient

async def redeploy_agents():
    print('🚀 Starting agent redeployment...')
    
    # Get environment variables
    kibana_url = os.getenv('KIBANA_URL')
    api_key = os.getenv('KIBANA_API_KEY')
    
    if not kibana_url or not api_key:
        print('❌ Missing KIBANA_URL or KIBANA_API_KEY environment variables')
        print('Please set these environment variables before running:')
        print('export KIBANA_URL="your_kibana_url"')
        print('export KIBANA_API_KEY="your_api_key"')
        return
    
    print(f'📡 Connecting to: {kibana_url}')
    
    try:
        # Create the client and use it as an async context manager
        async with AgentBuilderClient(kibana_url, api_key) as client:
            # Use a new session ID to avoid conflicts
            builder = GroceryAgentBuilder(
                agent_client=client,
                session_id='game_agents_v3'
            )
            
            print('🔧 Creating updated tools with better price logic...')
            tools = await builder.create_all_tools()
            print(f'✅ Created {len(tools)} tools')
            
            print('🤖 Creating updated agents with price range instructions...')
            agents = await builder.create_all_agents()
            print(f'✅ Created {len(agents)} agents')
            
            print('🎉 Redeployment complete!')
            
            # List the agent IDs for reference
            print('\n📋 Available agents:')
            for agent in agents:
                agent_id = agent.get('id', 'unknown')
                agent_name = agent.get('name', 'unknown')
                print(f'  - {agent_id}: {agent_name}')
                
            print('\n💡 The frontend will now get items in the $15-25 range instead of $0.60!')
            print('💡 Test with: "I need 5 items that cost around $20 each"')
            
    except Exception as e:
        print(f'❌ Error during deployment: {e}')
        import traceback
        traceback.print_exc()
        
    finally:
        print('✅ Agents deployment finished!')

if __name__ == '__main__':
    # Run the redeployment
    asyncio.run(redeploy_agents())
