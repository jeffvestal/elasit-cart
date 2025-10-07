#!/usr/bin/env python3
"""
Grocery Data Generator Control Script
Follows the pattern from synthetic-financial-data
"""

import argparse
import asyncio
import sys
from pathlib import Path
import importlib.util

# Add lib directory to path
lib_path = Path(__file__).parent / "lib"
sys.path.insert(0, str(lib_path))

from elasticsearch_client import ElasticsearchClient
from data_generators import GroceryDataGenerator
from llm_client import LLMClient

class GroceryDataControl:
    def __init__(self):
        self.es_client = None
        self.llm_client = None
        self.data_generator = None
        
    async def initialize_clients(self, es_url=None, es_api_key=None, llm_provider="bedrock", llm_model=None, skip_es=False, **llm_kwargs):
        """Initialize Elasticsearch and LLM clients"""
        if not skip_es and es_url and es_api_key:
            self.es_client = ElasticsearchClient(es_url, es_api_key)
            await self.es_client.connect()
        elif not skip_es:
            print("⚠️  No Elasticsearch connection - some features will be limited to file generation only")
        
        self.llm_client = LLMClient(provider=llm_provider, model=llm_model, **llm_kwargs)
        await self.llm_client.initialize()
        
        self.data_generator = GroceryDataGenerator(self.es_client, self.llm_client)
        
    async def interactive_menu(self):
        """Interactive menu for data generation options"""
        while True:
            print("\n" + "="*60)
            print("🛒 GROCERY DATA GENERATOR")
            print("="*60)
            print("1. 📊 Generate All Data (Full Dataset)")
            print("2. 🏪 Generate Store Data Only")  
            print("3. 🥑 Generate Grocery Items Only")
            print("4. 📦 Generate Inventory Data Only")
            print("5. 💰 Update Prices & Promotions")
            print("6. 📈 Load Data to Elasticsearch")
            print("7. 🗑️  Delete All Indices")
            print("8. 📋 View Current Configuration")
            print("9. ⚙️  Configure Dataset Sizes")
            print("0. 🚪 Exit")
            print("-"*60)
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                await self.generate_all_data()
            elif choice == "2":
                await self.generate_store_data()
            elif choice == "3":
                await self.generate_grocery_items()
            elif choice == "4":
                await self.generate_inventory_data()
            elif choice == "5":
                await self.update_dynamic_data()
            elif choice == "6":
                await self.load_data_to_elasticsearch()
            elif choice == "7":
                await self.delete_all_indices()
            elif choice == "8":
                self.show_configuration()
            elif choice == "9":
                self.configure_dataset_sizes()
            elif choice == "0":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                
    async def generate_all_data(self):
        """Generate complete dataset"""
        print("🚀 Generating complete grocery dataset...")
        
        print("🏪 Generating store locations...")
        await self.data_generator.generate_stores()
        
        print("🥑 Generating grocery items...")
        await self.data_generator.generate_grocery_items()
        
        print("📦 Generating inventory data...")
        await self.data_generator.generate_inventory()
        
        print("🍂 Generating seasonal data...")
        await self.data_generator.generate_seasonal_data()
        
        print("💰 Generating promotional offers...")
        await self.data_generator.generate_promotions()
        
        print("🥗 Generating dietary/nutrition data...")
        await self.data_generator.generate_nutrition_data()
        
        print("👨‍🍳 Generating recipe combinations...")
        await self.data_generator.generate_recipe_data()
        
        print("✅ Complete dataset generated!")
        
    async def generate_store_data(self):
        """Generate only store location data"""
        print("🏪 Generating store locations...")
        await self.data_generator.generate_stores()
        print("✅ Store data generated!")
        
    async def generate_grocery_items(self):
        """Generate only grocery items"""
        print("🥑 Generating grocery items...")
        await self.data_generator.generate_grocery_items()
        print("✅ Grocery items generated!")
        
    async def generate_inventory_data(self):
        """Generate inventory levels for all stores"""
        print("📦 Generating inventory data...")
        await self.data_generator.generate_inventory()
        print("✅ Inventory data generated!")
        
    async def update_dynamic_data(self):
        """Update prices, inventory, and promotions"""
        print("💰 Updating dynamic data (prices, inventory, promotions)...")
        await self.data_generator.update_dynamic_data()
        print("✅ Dynamic data updated!")
        
    async def load_data_to_elasticsearch(self):
        """Load generated data files to Elasticsearch"""
        print("📈 Loading data to Elasticsearch...")
        await self.data_generator.load_to_elasticsearch()
        print("✅ Data loaded to Elasticsearch!")
        
    async def delete_all_indices(self):
        """Delete all grocery-related indices"""
        confirm = input("⚠️  Are you sure you want to delete ALL indices? (yes/no): ")
        if confirm.lower() == 'yes':
            await self.es_client.delete_all_grocery_indices()
            print("🗑️  All indices deleted!")
        else:
            print("❌ Operation cancelled.")
            
    def show_configuration(self):
        """Display current configuration"""
        config = self.data_generator.get_configuration() if self.data_generator else {}
        print("\n📋 CURRENT CONFIGURATION")
        print("-"*40)
        print(f"Grocery Items: {config.get('grocery_items', 50000):,}")
        print(f"Store Count: {config.get('store_count', 20)}")
        print(f"Inventory per Store: {config.get('inventory_per_store', 15000):,}")
        print(f"Store Chains: {config.get('store_chains', 5)}")
        print(f"Target City: {config.get('city', 'Las Vegas')}")
        print(f"Seasonal Items: {config.get('seasonal_items', True)}")
        print(f"Promotional Offers: {config.get('promotions', True)}")
        
    def configure_dataset_sizes(self):
        """Configure dataset generation parameters"""
        print("\n⚙️  CONFIGURE DATASET SIZES")
        print("-"*40)
        
        # Get current config or defaults
        config = self.data_generator.get_configuration() if self.data_generator else {
            'grocery_items': 50000,
            'store_count': 20,
            'inventory_per_store': 15000,
            'store_chains': 5,
            'city': 'Las Vegas'
        }
        
        try:
            items = int(input(f"Grocery Items [{config['grocery_items']:,}]: ") or config['grocery_items'])
            stores = int(input(f"Store Count [{config['store_count']}]: ") or config['store_count'])
            inventory = int(input(f"Inventory per Store [{config['inventory_per_store']:,}]: ") or config['inventory_per_store'])
            chains = int(input(f"Store Chains [{config['store_chains']}]: ") or config['store_chains'])
            city = input(f"Target City [{config['city']}]: ") or config['city']
            
            new_config = {
                'grocery_items': items,
                'store_count': stores,
                'inventory_per_store': inventory,
                'store_chains': chains,
                'city': city,
                'seasonal_items': True,
                'promotions': True
            }
            
            if self.data_generator:
                self.data_generator.update_configuration(new_config)
                print("✅ Configuration updated!")
            else:
                print("⚠️  Configuration will be applied when generator is initialized.")
                
        except ValueError:
            print("❌ Invalid input. Configuration unchanged.")

async def main():
    parser = argparse.ArgumentParser(
        description="Grocery Data Generator",
        epilog="""
LLM Credential Setup:
  AWS Bedrock (recommended):
    export AWS_ACCESS_KEY_ID=your_access_key
    export AWS_SECRET_ACCESS_KEY=your_secret_key  
    export AWS_DEFAULT_REGION=us-west-2
    
  OpenAI:
    export OPENAI_API_KEY=your_api_key
    
  Azure OpenAI:
    export AZURE_OPENAI_ENDPOINT=your_endpoint
    export AZURE_OPENAI_API_KEY=your_api_key

Examples:
  Interactive mode:
    python control.py --es-url https://your-cluster.es.io:443 --es-api-key YOUR_KEY
    # OR using environment variables:
    export ELASTICSEARCH_URL=https://your-cluster.es.io:443
    export ELASTICSEARCH_API_KEY=YOUR_KEY
    python control.py
    
  Generate all data and load to ES:
    python control.py --action generate-and-load
    
  Generate data only (save to files):
    python control.py --action generate-only
    
  Load existing files to ES:
    python control.py --action load-only
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Required arguments (but made optional for generate-only mode)
    parser.add_argument("--es-url", help="Elasticsearch URL (required for load/interactive modes, or set ELASTICSEARCH_URL env var)")
    parser.add_argument("--es-api-key", help="Elasticsearch API Key (required for load/interactive modes, or set ELASTICSEARCH_API_KEY env var)")
    
    # Action selection (new!)
    parser.add_argument("--action", choices=["generate-and-load", "generate-only", "load-only", "update-dynamic", "interactive"], 
                       default="interactive", help="Action to perform")
    
    # LLM configuration
    parser.add_argument("--llm-provider", default="bedrock", choices=["bedrock", "openai", "azure"], 
                       help="LLM provider to use (default: bedrock)")
    parser.add_argument("--llm-model", help="Specific model to use (optional)")
    parser.add_argument("--aws-region", default="us-west-2", help="AWS region for Bedrock (default: us-west-2)")
    
    # LLM credentials (optional, can use env vars)
    parser.add_argument("--openai-api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--azure-endpoint", help="Azure OpenAI endpoint (or set AZURE_OPENAI_ENDPOINT env var)")
    parser.add_argument("--azure-api-key", help="Azure OpenAI API key (or set AZURE_OPENAI_API_KEY env var)")
    
    # Data configuration
    parser.add_argument("--items", type=int, default=50000, help="Number of grocery items to generate (default: 50000)")
    parser.add_argument("--stores", type=int, default=20, help="Number of stores to generate (default: 20)")
    parser.add_argument("--inventory-per-store", type=int, default=15000, help="Inventory items per store (default: 15000)")
    parser.add_argument("--city", default="Las Vegas", help="Target city for stores (default: Las Vegas)")
    
    # Legacy flags for backward compatibility
    parser.add_argument("--generate-all", action="store_true", help="[DEPRECATED] Use --action generate-and-load")
    parser.add_argument("--update-dynamic", action="store_true", help="[DEPRECATED] Use --action update-dynamic")
    parser.add_argument("--load-to-es", action="store_true", help="[DEPRECATED] Use --action load-only")
    
    args = parser.parse_args()
    
    # Add environment variable fallbacks for ES credentials
    import os
    if not args.es_url:
        args.es_url = os.getenv('ELASTICSEARCH_URL') or os.getenv('ES_URL')
    if not args.es_api_key:
        args.es_api_key = os.getenv('ELASTICSEARCH_API_KEY') or os.getenv('ES_API_KEY')
    
    # Check if ES credentials are required for the selected action
    es_required_actions = ["generate-and-load", "load-only", "update-dynamic", "interactive"]
    if args.action in es_required_actions and (not args.es_url or not args.es_api_key):
        print(f"❌ Elasticsearch URL and API key are required for --action {args.action}")
        print("💡 For generate-only mode, ES credentials are not needed!")
        sys.exit(1)
    
    skip_es = args.action == "generate-only"
    
    control = GroceryDataControl()
    
    # Handle legacy flags
    if args.generate_all:
        print("⚠️  --generate-all is deprecated. Use --action generate-and-load")
        args.action = "generate-and-load"
    elif args.update_dynamic:
        print("⚠️  --update-dynamic is deprecated. Use --action update-dynamic")
        args.action = "update-dynamic"  
    elif args.load_to_es:
        print("⚠️  --load-to-es is deprecated. Use --action load-only")
        args.action = "load-only"
    
    # Prepare LLM kwargs
    llm_kwargs = {'region': args.aws_region}
    
    if args.llm_provider == "openai":
        import os
        api_key = args.openai_api_key or os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ OpenAI API key required. Set OPENAI_API_KEY environment variable or use --openai-api-key")
            sys.exit(1)
        llm_kwargs['api_key'] = api_key
        
    elif args.llm_provider == "azure":
        import os
        endpoint = args.azure_endpoint or os.getenv('AZURE_OPENAI_ENDPOINT')
        api_key = args.azure_api_key or os.getenv('AZURE_OPENAI_API_KEY')
        if not endpoint or not api_key:
            print("❌ Azure endpoint and API key required. Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables")
            sys.exit(1)
        llm_kwargs.update({'endpoint': endpoint, 'api_key': api_key})
    
    try:
        print(f"🔧 Initializing {args.llm_provider} LLM client...")
        await control.initialize_clients(
            args.es_url, 
            args.es_api_key, 
            args.llm_provider,
            llm_model=args.llm_model,
            skip_es=skip_es,
            **llm_kwargs
        )
        
        # Apply data configuration
        if hasattr(control, 'data_generator') and control.data_generator:
            config = {
                'grocery_items': args.items,
                'store_count': args.stores,
                'inventory_per_store': args.inventory_per_store,
                'city': args.city,
                'store_chains': 5,
                'seasonal_items': True,
                'promotions': True
            }
            control.data_generator.update_configuration(config)
        
        print(f"✅ Initialized! Action: {args.action}")
        
        # Execute the requested action
        if args.action == "generate-and-load":
            await control.generate_all_data()
            await control.load_data_to_elasticsearch()
        elif args.action == "generate-only":
            await control.generate_all_data()
            print("📁 Data generated and saved to files. Use --action load-only to load to Elasticsearch.")
        elif args.action == "load-only":
            await control.load_data_to_elasticsearch()
        elif args.action == "update-dynamic":
            await control.update_dynamic_data()
            await control.load_data_to_elasticsearch()
        elif args.action == "interactive":
            await control.interactive_menu()
            
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled by user.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        if control.es_client:
            await control.es_client.close()

if __name__ == "__main__":
    asyncio.run(main())
