#!/usr/bin/env python3
"""
Script to delete and recreate grocery indices with LOOKUP mode for ES|QL LOOKUP JOIN support
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add the lib directory to the path
lib_path = Path(__file__).parent / "lib"
sys.path.insert(0, str(lib_path))

from elasticsearch_client import ElasticsearchClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def recreate_indices_with_lookup_mode():
    """Delete existing indices and recreate with lookup mode"""
    
    # Get environment variables
    es_url = os.getenv('ES_URL')
    api_key = os.getenv('ES_API_KEY')
    
    if not es_url or not api_key:
        print("❌ Missing environment variables!")
        print("   Set ES_URL and ES_API_KEY before running this script")
        print("   Example:")
        print("     export ES_URL='https://your-cluster.es.cloud.es.io:443'")
        print("     export ES_API_KEY='your-api-key'")
        return False
    
    print("🗂️  Recreating Elasticsearch indices with LOOKUP mode...")
    print(f"   Elasticsearch URL: {es_url}")
    print(f"   API Key: {api_key[:10]}...")
    print()
    
    try:
        # Initialize client
        client = ElasticsearchClient(es_url, api_key)
        await client.connect()
        
        # Get all index names
        mappings = client._get_index_mappings()
        index_names = list(mappings.keys())
        
        print(f"📋 Indices to recreate: {', '.join(index_names)}")
        print()
        
        # Delete existing indices
        print("🗑️  Deleting existing indices...")
        for index_name in index_names:
            try:
                if await client.client.indices.exists(index=index_name):
                    await client.client.indices.delete(index=index_name)
                    print(f"   ✅ Deleted: {index_name}")
                else:
                    print(f"   ⏭️  Not found: {index_name}")
            except Exception as e:
                print(f"   ⚠️  Error deleting {index_name}: {e}")
        
        print()
        
        # Recreate indices with LOOKUP mode
        print("🏗️  Creating indices with LOOKUP mode...")
        await client.create_indices()
        print("   ✅ All indices created with lookup mode!")
        
        print()
        print("🎉 SUCCESS! All indices recreated with LOOKUP mode.")
        print()
        print("📝 Next steps:")
        print("   1. Re-upload your grocery data:")
        print("      cd grocery-data-generator")
        print("      python control.py --action load-only")
        print()
        print("   2. Test Agent Builder tools with LOOKUP JOIN:")
        print("      cd ../agent-builder-service") 
        print("      python test_corrected_tools.py")
        
        await client.close()
        return True
        
    except Exception as e:
        logger.error(f"Failed to recreate indices: {e}")
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Elasti-Cart Index Recreation for LOOKUP JOIN Support")
    print("=" * 60)
    print()
    
    success = asyncio.run(recreate_indices_with_lookup_mode())
    
    if success:
        print("✅ Index recreation completed successfully!")
        sys.exit(0)
    else:
        print("❌ Index recreation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
