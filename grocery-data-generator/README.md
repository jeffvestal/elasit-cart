# Grocery Data Generator

A comprehensive data generator for creating realistic grocery store data for demos and testing. This tool generates synthetic but realistic data for grocery items, store locations, inventory, pricing, promotions, and more.

## Features

- 🛒 **Grocery Items**: Generate 50,000+ unique items with realistic names, brands, categories, and pricing
- 🏪 **Store Locations**: Create stores with fun Vegas-themed chain names and realistic addresses
- 📦 **Inventory Management**: Per-store inventory with dynamic pricing and stock levels
- 🍂 **Seasonal Data**: Seasonal availability and pricing variations for produce
- 💰 **Promotions**: Realistic sales, bundles, and promotional offers
- 🥗 **Nutrition Facts**: Complete nutrition labels for food items
- 👨‍🍳 **Recipe Combinations**: Recipe suggestions with ingredient combinations
- 🔄 **Dynamic Updates**: Configurable price and inventory fluctuations

## Installation

```bash
cd grocery-data-generator
pip install -r requirements.txt
```

## Configuration

Set up your credentials:

```bash
# For AWS Bedrock (recommended)
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-west-2

# For OpenAI (alternative)
export OPENAI_API_KEY=your_openai_key

# For Azure OpenAI (alternative)
export AZURE_OPENAI_ENDPOINT=your_endpoint
export AZURE_OPENAI_API_KEY=your_key
```

## Usage

### Interactive Mode

```bash
python control.py --es-url https://your-cluster.es.cloud.es.io:443 --es-api-key your_api_key
```

This will show an interactive menu with options to:
- Generate complete datasets
- Generate specific data types
- Update dynamic data (prices, inventory)
- Load data to Elasticsearch
- Configure dataset sizes

### Command Line Mode

```bash
# Generate all data and load to Elasticsearch
python control.py --es-url URL --es-api-key KEY --generate-all

# Update only dynamic data (prices, inventory)
python control.py --es-url URL --es-api-key KEY --update-dynamic

# Load pre-generated data to Elasticsearch
python control.py --es-url URL --es-api-key KEY --load-to-es
```

### Configuration Options

Default settings:
- **Grocery Items**: 50,000 unique items
- **Stores**: 20 stores across 5 chains
- **Inventory per Store**: 15,000 items
- **Location**: Las Vegas, Nevada

These can be customized through the interactive menu or by modifying the configuration.

## Data Structure

### Generated Indices

- `grocery_items` - Product catalog with names, brands, categories, pricing
- `store_locations` - Store addresses, hours, specialties
- `store_inventory` - Per-store stock levels and pricing
- `seasonal_availability` - Seasonal variations for produce
- `promotional_offers` - Sales, bundles, discounts
- `nutrition_facts` - Nutrition labels for food items
- `recipe_combinations` - Recipe suggestions and ingredient pairings

### Vegas Store Chains

- **Dice Mart** (Discount) - Budget-friendly everyday essentials
- **Jackpot Grocers** (Mid-range) - General family-friendly groceries
- **All-In Foods** (Mid-range) - Convenient general groceries
- **Lucky Strike Market** (Premium) - Organic, fresh, local focus
- **High Roller Gourmet** (Luxury) - Gourmet, imported, premium items

## Output Files

Generated data is saved to `generated_data/` directory:
- `grocery_items.json`
- `store_locations.json`
- `store_inventory.json`
- `seasonal_availability.json`
- `promotional_offers.json`
- `nutrition_facts.json`
- `recipe_combinations.json`

These files can be reloaded into Elasticsearch clusters without regenerating the data.

## LLM Providers

### AWS Bedrock (Recommended)
Uses Claude 3.5 Sonnet for high-quality data generation.

### OpenAI
Supports GPT-4 and other OpenAI models.

### Azure OpenAI
Supports Azure-hosted OpenAI models.

## Development

The generator follows a modular architecture:
- `control.py` - Main control script and interactive menu
- `lib/elasticsearch_client.py` - Elasticsearch operations
- `lib/llm_client.py` - Multi-provider LLM integration
- `lib/data_generators.py` - Core data generation logic

## Examples

### Generate Sample Data
```bash
# Quick test run with smaller dataset
python control.py --es-url URL --es-api-key KEY
# Select option 9 to configure smaller sizes for testing
# Then select option 1 to generate all data
```

### Update Prices Daily
```bash
# Set up cron job to update prices and inventory
0 6 * * * cd /path/to/grocery-data-generator && python control.py --es-url URL --es-api-key KEY --update-dynamic
```

## License

Apache 2.0 License - See LICENSE file for details.
