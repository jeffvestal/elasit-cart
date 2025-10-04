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
        
    async def initialize_clients(self, es_url, es_api_key, llm_provider="bedrock"):
        """Initialize Elasticsearch and LLM clients"""
        self.es_client = ElasticsearchClient(es_url, es_api_key)
        await self.es_client.connect()
        
        self.llm_client = LLMClient(provider=llm_provider)
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
    parser = argparse.ArgumentParser(description="Grocery Data Generator")
    parser.add_argument("--es-url", required=True, help="Elasticsearch URL")
    parser.add_argument("--es-api-key", required=True, help="Elasticsearch API Key")
    parser.add_argument("--llm-provider", default="bedrock", choices=["bedrock", "openai", "azure"], 
                       help="LLM provider to use")
    parser.add_argument("--generate-all", action="store_true", help="Generate all data and exit")
    parser.add_argument("--update-dynamic", action="store_true", help="Update only dynamic data")
    parser.add_argument("--load-to-es", action="store_true", help="Load generated files to Elasticsearch")
    
    args = parser.parse_args()
    
    control = GroceryDataControl()
    
    try:
        await control.initialize_clients(args.es_url, args.es_api_key, args.llm_provider)
        
        if args.generate_all:
            await control.generate_all_data()
        elif args.update_dynamic:
            await control.update_dynamic_data()
        elif args.load_to_es:
            await control.load_data_to_elasticsearch()
        else:
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
