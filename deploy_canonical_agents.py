#!/usr/bin/env python3
"""
Deploy canonical agent and tool definitions to any Elasticsearch cluster.
This ensures consistent, reproducible deployments across environments.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add agent-builder-service to path
sys.path.insert(0, str(Path(__file__).parent / 'agent-builder-service'))

from agent_builder_client import AgentBuilderClient

async def deploy_canonical_definitions(delete_existing=False):
    """Deploy tools and agents from canonical definitions."""
    
    print('🚀 Deploying Canonical Agent Builder Definitions')
    print('=' * 60)
    
    # Get environment variables
    kibana_url = os.getenv('KIBANA_URL')
    api_key = os.getenv('KIBANA_API_KEY')
    
    if not kibana_url or not api_key:
        print('❌ Missing KIBANA_URL or KIBANA_API_KEY environment variables')
        print('Please set these environment variables before running:')
        print('export KIBANA_URL="your_kibana_url"')
        print('export KIBANA_API_KEY="your_api_key"')
        return False
    
    print(f'📡 Target: {kibana_url}')
    print()
    
    # Load canonical definitions
    canonical_dir = Path(__file__).parent / 'canonical-definitions'
    tools_file = canonical_dir / 'tools.json'
    agents_file = canonical_dir / 'agents.json'
    
    if not tools_file.exists() or not agents_file.exists():
        print(f'❌ Canonical definitions not found in {canonical_dir}')
        return False
    
    with open(tools_file) as f:
        canonical_tools = json.load(f)
    
    with open(agents_file) as f:
        canonical_agents = json.load(f)
    
    print(f'📋 Loaded {len(canonical_tools)} tool definitions')
    print(f'📋 Loaded {len(canonical_agents)} agent definitions')
    print()
    
    async with AgentBuilderClient(kibana_url, api_key) as client:
        
        # Delete existing tools if requested
        if delete_existing:
            print('🗑️  Deleting existing tools and agents...')
            for tool in canonical_tools:
                try:
                    await client.delete_tool(tool['id'])
                    print(f'  ✅ Deleted tool: {tool["id"]}')
                except Exception as e:
                    print(f'  ℹ️  Could not delete {tool["id"]}: {str(e)[:50]}')
            
            for agent in canonical_agents:
                try:
                    await client.delete_agent(agent['id'])
                    print(f'  ✅ Deleted agent: {agent["id"]}')
                except Exception as e:
                    print(f'  ℹ️  Could not delete {agent["id"]}: {str(e)[:50]}')
            print()
        
        # Deploy tools
        print('🔧 Deploying Tools...')
        print('-' * 60)
        deployed_tools = []
        failed_tools = []
        
        for tool in canonical_tools:
            tool_id = tool['id']
            try:
                # Remove fields that shouldn't be in create request
                tool_def = {k: v for k, v in tool.items() if k not in ['created_at', 'updated_at', 'readonly']}
                
                result = await client.create_tool(tool_def)
                deployed_tools.append(tool_id)
                print(f'  ✅ {tool_id}')
            except Exception as e:
                failed_tools.append((tool_id, str(e)))
                print(f'  ❌ {tool_id}: {str(e)[:80]}')
        
        print()
        print(f'✅ Successfully deployed {len(deployed_tools)}/{len(canonical_tools)} tools')
        if failed_tools:
            print(f'❌ Failed to deploy {len(failed_tools)} tools')
        print()
        
        # Deploy agents
        print('🤖 Deploying Agents...')
        print('-' * 60)
        deployed_agents = []
        failed_agents = []
        
        for agent in canonical_agents:
            agent_id = agent['id']
            try:
                # Remove fields that shouldn't be in create request
                # Note: 'type' is returned in GET but shouldn't be in POST
                agent_def = {k: v for k, v in agent.items() if k not in ['created_at', 'updated_at', 'readonly', 'type']}
                
                result = await client.create_agent(agent_def)
                deployed_agents.append(agent_id)
                print(f'  ✅ {agent_id}')
            except Exception as e:
                failed_agents.append((agent_id, str(e)))
                print(f'  ❌ {agent_id}: {str(e)[:80]}')
        
        print()
        print(f'✅ Successfully deployed {len(deployed_agents)}/{len(canonical_agents)} agents')
        if failed_agents:
            print(f'❌ Failed to deploy {len(failed_agents)} agents')
        print()
        
        # Summary
        print('=' * 60)
        print('📊 Deployment Summary')
        print('=' * 60)
        print(f'Tools:  {len(deployed_tools)}/{len(canonical_tools)} deployed')
        print(f'Agents: {len(deployed_agents)}/{len(canonical_agents)} deployed')
        
        if failed_tools:
            print('\n❌ Failed Tools:')
            for tool_id, error in failed_tools:
                print(f'  - {tool_id}: {error[:100]}')
        
        if failed_agents:
            print('\n❌ Failed Agents:')
            for agent_id, error in failed_agents:
                print(f'  - {agent_id}: {error[:100]}')
        
        success = len(failed_tools) == 0 and len(failed_agents) == 0
        
        if success:
            print('\n🎉 All definitions deployed successfully!')
        else:
            print('\n⚠️  Some definitions failed to deploy')
        
        return success

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Deploy canonical agent and tool definitions'
    )
    parser.add_argument(
        '--delete-existing',
        action='store_true',
        help='Delete existing tools and agents before deploying'
    )
    
    args = parser.parse_args()
    
    success = asyncio.run(deploy_canonical_definitions(
        delete_existing=args.delete_existing
    ))
    
    sys.exit(0 if success else 1)

