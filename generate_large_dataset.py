#!/usr/bin/env python3
"""
Quick large dataset generator without LLM dependency
Generates realistic grocery data for testing the agents
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# Realistic grocery data templates
GROCERY_CATEGORIES = {
    "Fresh Produce": {
        "subcategories": ["Fruits", "Vegetables", "Herbs", "Organic"],
        "items": [
            ("Organic Bananas", "Dole", 1.99, "lb"),
            ("Hass Avocados", "Nature's Pride", 2.49, "each"),
            ("Baby Spinach", "Earthbound Farm", 4.99, "5 oz"),
            ("Roma Tomatoes", "Fresh Select", 2.99, "lb"),
            ("Red Bell Peppers", "Premium", 3.99, "lb"),
            ("Broccoli Crowns", "Green Giant", 2.49, "each"),
            ("Organic Carrots", "Cal-Organic", 1.99, "2 lb bag"),
            ("Strawberries", "Driscoll's", 4.99, "16 oz"),
            ("Gala Apples", "Washington", 2.99, "3 lb bag"),
            ("Green Onions", "Fresh", 1.49, "bunch")
        ]
    },
    "Meat & Seafood": {
        "subcategories": ["Beef", "Poultry", "Pork", "Seafood"],
        "items": [
            ("Ground Beef 80/20", "Premium", 6.99, "lb"),
            ("Chicken Breast", "Foster Farms", 8.99, "lb"),
            ("Salmon Fillets", "Fresh Atlantic", 12.99, "lb"),
            ("Ground Turkey", "Jennie-O", 5.99, "lb"),
            ("Pork Chops", "Smithfield", 7.99, "lb"),
            ("Shrimp", "Wild Caught", 15.99, "lb"),
            ("Ribeye Steak", "Choice Grade", 18.99, "lb"),
            ("Chicken Thighs", "Foster Farms", 4.99, "lb"),
            ("Ground Pork", "Premium", 5.49, "lb"),
            ("Tilapia Fillets", "Fresh", 8.99, "lb")
        ]
    },
    "Dairy & Eggs": {
        "subcategories": ["Milk", "Cheese", "Eggs", "Yogurt"],
        "items": [
            ("Whole Milk", "Horizon Organic", 4.99, "64 oz"),
            ("Large Eggs", "Farm Fresh", 3.99, "dozen"),
            ("Cheddar Cheese", "Tillamook", 5.49, "8 oz"),
            ("Greek Yogurt", "Chobani", 1.99, "5.3 oz"),
            ("Butter", "Land O'Lakes", 4.49, "16 oz"),
            ("Cream Cheese", "Philadelphia", 2.99, "8 oz"),
            ("Mozzarella Cheese", "Kraft", 4.99, "16 oz"),
            ("Almond Milk", "Silk", 3.99, "64 oz"),
            ("Cottage Cheese", "Daisy", 3.49, "16 oz"),
            ("Heavy Cream", "Organic Valley", 3.99, "16 oz")
        ]
    },
    "Pantry Staples": {
        "subcategories": ["Pasta", "Rice", "Canned Goods", "Condiments"],
        "items": [
            ("Spaghetti", "Barilla", 1.99, "16 oz"),
            ("White Rice", "Minute", 2.99, "2 lb"),
            ("Olive Oil", "Bertolli", 7.99, "25.3 oz"),
            ("Tomato Sauce", "Hunt's", 1.49, "15 oz"),
            ("Black Beans", "Bush's", 1.99, "15 oz"),
            ("Peanut Butter", "Jif", 4.99, "40 oz"),
            ("Honey", "Nature Nate's", 6.99, "32 oz"),
            ("Quinoa", "Ancient Harvest", 7.99, "16 oz"),
            ("Coconut Oil", "Spectrum", 8.99, "14 oz"),
            ("Balsamic Vinegar", "Pompeian", 3.99, "16 oz")
        ]
    },
    "Bakery": {
        "subcategories": ["Bread", "Pastries", "Bagels", "Rolls"],
        "items": [
            ("Whole Wheat Bread", "Dave's Killer", 4.99, "27 oz"),
            ("Sourdough Bread", "Boudin", 3.99, "24 oz"),
            ("Bagels", "Thomas'", 3.49, "6 pack"),
            ("Croissants", "La Brea", 4.99, "4 pack"),
            ("Dinner Rolls", "King's Hawaiian", 3.99, "12 pack"),
            ("English Muffins", "Thomas'", 2.99, "6 pack"),
            ("Tortillas", "Mission", 2.99, "10 count"),
            ("Pita Bread", "Joseph's", 2.49, "6 pack"),
            ("Hamburger Buns", "Wonder", 2.49, "8 pack"),
            ("Muffins", "Costco", 5.99, "12 pack")
        ]
    }
}

LAS_VEGAS_STORES = [
    ("Smith's Food & Drug", "Kroger", "Premium", "4350 E Tropicana Ave", "89121", 36.1002, -115.0892),
    ("Albertsons", "Albertsons", "Premium", "2885 E Desert Inn Rd", "89169", 36.1291, -115.1089),
    ("Walmart Supercenter", "Walmart", "Discount", "4505 W Charleston Blvd", "89102", 36.1580, -115.2087),
    ("Whole Foods Market", "Amazon", "Premium", "8855 W Charleston Blvd", "89117", 36.1580, -115.2950),
    ("Vons", "Albertsons", "Premium", "9120 W Sahara Ave", "89117", 36.1447, -115.2989),
    ("Smith's Food & Drug", "Kroger", "Premium", "2211 N Rainbow Blvd", "89108", 36.1845, -115.2428),
    ("WinCo Foods", "WinCo", "Discount", "7231 Arroyo Crossing Pkwy", "89113", 36.0394, -115.1654),
    ("Fresh Market", "Independent", "Premium", "9620 S Eastern Ave", "89123", 36.0394, -115.1183),
    ("Lee's Sandwiches", "Lee's", "Discount", "2620 S Decatur Blvd", "89102", 36.1291, -115.2087),
    ("Sprouts Farmers Market", "Sprouts", "Premium", "7530 W Lake Mead Blvd", "89128", 36.2108, -115.2654),
    ("Target", "Target", "Mid-tier", "8725 W Charleston Blvd", "89117", 36.1580, -115.2850),
    ("Costco Wholesale", "Costco", "Warehouse", "801 S Pavilion Center Dr", "89144", 36.1447, -115.2989),
    ("Sam's Club", "Walmart", "Warehouse", "4815 Boulder Hwy", "89121", 36.1002, -115.0654),
    ("Trader Joe's", "Trader Joe's", "Premium", "2716 N Green Valley Pkwy", "89014", 36.1845, -115.0321),
    ("Food 4 Less", "Kroger", "Discount", "4855 Boulder Hwy", "89121", 36.1002, -115.0587),
    ("Ranch Market", "Independent", "Mid-tier", "2901 Las Vegas Blvd S", "89109", 36.1291, -115.1654),
    ("International Marketplace", "Independent", "Premium", "5000 Spring Mountain Rd", "89146", 36.1291, -115.2321),
    ("99 Ranch Market", "99 Ranch", "Premium", "4275 Spring Mountain Rd", "89102", 36.1291, -115.1987),
    ("Cardenas Markets", "Cardenas", "Mid-tier", "2710 N Las Vegas Blvd", "89030", 36.2108, -115.1654),
    ("Mariana's Supermarket", "Independent", "Mid-tier", "3045 N Las Vegas Blvd", "89030", 36.2200, -115.1654)
]

def generate_stores():
    """Generate store location data"""
    stores = []
    
    for i, (name, chain, tier, address, zip_code, lat, lon) in enumerate(LAS_VEGAS_STORES):
        store = {
            "store_id": f"STORE_{i+1:03d}",
            "store_name": name,
            "chain_name": chain,
            "chain_tier": tier,
            "address": {
                "street": address,
                "city": "Las Vegas",
                "state": "NV", 
                "zip_code": zip_code,
                "coordinates": {
                    "lat": lat + random.uniform(-0.01, 0.01),
                    "lon": lon + random.uniform(-0.01, 0.01)
                }
            },
            "phone": f"702-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "hours": {
                "monday": "6:00 AM - 11:00 PM",
                "tuesday": "6:00 AM - 11:00 PM", 
                "wednesday": "6:00 AM - 11:00 PM",
                "thursday": "6:00 AM - 11:00 PM",
                "friday": "6:00 AM - 12:00 AM",
                "saturday": "6:00 AM - 12:00 AM",
                "sunday": "7:00 AM - 10:00 PM"
            },
            "specialties": random.sample([
                "Fresh produce", "Organic foods", "International cuisine",
                "Bulk items", "Prepared foods", "Bakery", "Pharmacy",
                "Floral", "Seafood counter", "Meat department"
            ], k=random.randint(2, 4))
        }
        stores.append(store)
    
    return stores

def generate_grocery_items(count=10000):
    """Generate grocery items"""
    items = []
    item_counter = 1
    
    # Generate items from each category
    items_per_category = count // len(GROCERY_CATEGORIES)
    
    for category, data in GROCERY_CATEGORIES.items():
        subcategories = data["subcategories"]
        base_items = data["items"]
        
        for i in range(items_per_category):
            base_item = random.choice(base_items)
            subcategory = random.choice(subcategories)
            
            # Add some variation to names and prices
            name_variations = ["", "Premium", "Organic", "Fresh", "Select", "Choice"]
            name_prefix = random.choice(name_variations)
            final_name = f"{name_prefix} {base_item[0]}".strip()
            
            price_variation = random.uniform(0.8, 1.3)
            final_price = round(base_item[2] * price_variation, 2)
            
            item = {
                "item_id": f"ITEM_{item_counter:06d}",
                "name": final_name,
                "brand": base_item[1],
                "category": category,
                "sub_category": subcategory,
                "description": f"High-quality {final_name.lower()} from {base_item[1]}",
                "base_price": final_price,
                "unit_size": base_item[3],
                "unit_type": "package",
                "barcode": f"{random.randint(100000000000, 999999999999)}",
                "organic": "Organic" in final_name,
                "gluten_free": random.choice([True, False]),
                "vegan": category == "Fresh Produce" or random.choice([True, False]),
                "vegetarian": category != "Meat & Seafood" or random.choice([True, False]),
                "dairy_free": category not in ["Dairy & Eggs"] or random.choice([True, False]),
                "nut_free": random.choice([True, False]),
                "tags": [category.lower().replace(" & ", "_").replace(" ", "_"), subcategory.lower()],
                "created_date": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
            }
            items.append(item)
            item_counter += 1
    
    return items

def generate_store_inventory(stores, items, items_per_store=1000):
    """Generate store inventory"""
    inventory = []
    inventory_counter = 1
    
    for store in stores:
        store_id = store["store_id"]
        
        # Each store gets a random selection of items
        store_items = random.sample(items, min(items_per_store, len(items)))
        
        for item in store_items:
            # Price variations by store tier
            base_price = item["base_price"]
            tier = store["chain_tier"]
            
            if tier == "Premium":
                price_multiplier = random.uniform(1.1, 1.3)
            elif tier == "Discount":
                price_multiplier = random.uniform(0.7, 0.9)
            elif tier == "Warehouse":
                price_multiplier = random.uniform(0.6, 0.8)
            else:  # Mid-tier
                price_multiplier = random.uniform(0.9, 1.1)
            
            current_price = round(base_price * price_multiplier, 2)
            
            # Random sales
            on_sale = random.choice([True, False]) if random.random() < 0.3 else False
            sale_price = round(current_price * random.uniform(0.7, 0.9), 2) if on_sale else None
            
            inventory_item = {
                "inventory_id": f"INV_{inventory_counter:08d}",
                "store_id": store_id,
                "item_id": item["item_id"],
                "current_price": current_price,
                "on_sale": on_sale,
                "sale_price": sale_price,
                "sale_end_date": (datetime.now() + timedelta(days=random.randint(1, 14))).isoformat() if on_sale else None,
                "stock_level": random.randint(5, 100),
                "stock_status": random.choice(["in_stock", "low_stock"]),
                "seasonal_availability": random.choice([True, False]),
                "last_restocked": (datetime.now() - timedelta(days=random.randint(1, 7))).isoformat(),
                "last_updated": datetime.now().isoformat(),
                "price_last_updated": datetime.now().isoformat()
            }
            inventory.append(inventory_item)
            inventory_counter += 1
    
    return inventory

def generate_promotional_offers(items, stores):
    """Generate promotional offers for items"""
    offers = []
    offer_counter = 1
    
    # Select random items for promotions (about 20% of items)
    promo_items = random.sample(items, min(len(items) // 5, 5000))
    
    for item in promo_items:
        # Random stores for this promotion
        promo_stores = random.sample(stores, random.randint(1, 5))
        
        for store in promo_stores:
            offer = {
                "offer_id": f"PROMO_{offer_counter:06d}",
                "item_id": item["item_id"],
                "store_id": store["store_id"],
                "offer_type": random.choice(["percentage_discount", "fixed_discount", "buy_one_get_one", "bulk_discount"]),
                "discount_percent": random.randint(10, 50) if random.choice([True, False]) else None,
                "fixed_discount": round(random.uniform(0.50, 3.00), 2) if random.choice([True, False]) else None,
                "min_quantity": random.randint(1, 3) if random.choice([True, False]) else 1,
                "description": f"Special offer on {item['name']}",
                "start_date": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                "end_date": (datetime.now() + timedelta(days=random.randint(7, 60))).isoformat(),
                "conditions": f"Valid at {store['store_name']} only",
                "active": random.choice([True, True, True, False])  # 75% active
            }
            offers.append(offer)
            offer_counter += 1
    
    return offers

def generate_seasonal_availability(items):
    """Generate seasonal availability data"""
    seasonal_data = []
    
    # Select items that would be seasonal (mainly produce)
    seasonal_items = [item for item in items if item["category"] == "Fresh Produce"]
    seasonal_items = random.sample(seasonal_items, min(len(seasonal_items), 1000))
    
    seasons = ["spring", "summer", "fall", "winter"]
    
    for item in seasonal_items:
        season = random.choice(seasons)
        seasonal = {
            "item_id": item["item_id"],
            "season": season,
            "availability_score": round(random.uniform(0.3, 1.0), 2),
            "price_multiplier": round(random.uniform(0.8, 1.5), 2),
            "peak_months": random.sample(["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 
                                       k=random.randint(2, 4)),
            "description": f"{item['name']} seasonal availability for {season}"
        }
        seasonal_data.append(seasonal)
    
    return seasonal_data

def generate_recipe_combinations(items):
    """Generate recipe combinations using actual item IDs"""
    recipes = []
    recipe_counter = 1
    
    # Recipe templates with ingredient categories
    recipe_templates = [
        {
            "name": "Classic Spaghetti Marinara",
            "categories": ["Pantry Staples", "Fresh Produce", "Dairy & Eggs"],
            "difficulty": "easy",
            "cook_time": 30,
            "servings": 4
        },
        {
            "name": "Grilled Chicken Salad", 
            "categories": ["Meat & Seafood", "Fresh Produce", "Pantry Staples"],
            "difficulty": "medium",
            "cook_time": 25,
            "servings": 2
        },
        {
            "name": "Beef Stir Fry",
            "categories": ["Meat & Seafood", "Fresh Produce", "Pantry Staples"],
            "difficulty": "medium", 
            "cook_time": 20,
            "servings": 4
        },
        {
            "name": "Breakfast Sandwich",
            "categories": ["Dairy & Eggs", "Bakery", "Meat & Seafood"],
            "difficulty": "easy",
            "cook_time": 10,
            "servings": 1
        },
        {
            "name": "Vegetable Soup",
            "categories": ["Fresh Produce", "Pantry Staples"],
            "difficulty": "easy",
            "cook_time": 45,
            "servings": 6
        }
    ]
    
    # Generate multiple recipes from templates
    for _ in range(2000):  # Generate 2000 recipe combinations
        template = random.choice(recipe_templates)
        
        # Find items from required categories
        recipe_items = []
        for category in template["categories"]:
            category_items = [item for item in items if item["category"] == category]
            if category_items:
                recipe_items.extend(random.sample(category_items, min(2, len(category_items))))
        
        if len(recipe_items) >= 3:  # Need at least 3 ingredients
            primary_item = recipe_items[0]
            
            recipe = {
                "recipe_id": f"RECIPE_{recipe_counter:06d}",
                "recipe_name": template["name"],
                "primary_item_id": primary_item["item_id"],
                "ingredient_ids": [item["item_id"] for item in recipe_items[:6]],  # Max 6 ingredients
                "difficulty": template["difficulty"],
                "prep_time": random.randint(5, 30),
                "cook_time": template["cook_time"] + random.randint(-10, 10),
                "total_time": template["cook_time"] + random.randint(5, 40),
                "servings": template["servings"],
                "cuisine_type": random.choice(["American", "Italian", "Mexican", "Asian", "Mediterranean"]),
                "meal_type": random.choice(["breakfast", "lunch", "dinner", "snack"]),
                "description": f"Delicious {template['name'].lower()} made with fresh ingredients",
                "instructions": f"Prepare {template['name'].lower()} using the listed ingredients",
                "tags": [template["difficulty"], template["name"].lower().replace(" ", "_")]
            }
            recipes.append(recipe)
            recipe_counter += 1
    
    return recipes

def generate_nutrition_facts(items):
    nutrition_data = []
    
    for item in items:
        # Skip non-food items
        if item["category"] in ["Fresh Produce", "Meat & Seafood", "Dairy & Eggs", "Pantry Staples", "Bakery"]:
            nutrition = {
                "item_id": item["item_id"],
                "serving_size": "1 serving",
                "calories": random.randint(50, 500),
                "total_fat": round(random.uniform(0, 25), 1),
                "saturated_fat": round(random.uniform(0, 10), 1),
                "cholesterol": random.randint(0, 100),
                "sodium": random.randint(0, 1000),
                "total_carbs": round(random.uniform(0, 50), 1),
                "dietary_fiber": round(random.uniform(0, 15), 1),
                "total_sugars": round(random.uniform(0, 30), 1),
                "protein": round(random.uniform(0, 30), 1),
                "ingredients": f"Main ingredients for {item['name'].lower()}",
                "allergens": random.sample(["milk", "eggs", "fish", "shellfish", "tree nuts", "peanuts", "wheat", "soybeans"], k=random.randint(0, 3)),
                "organic": item["organic"],
                "gluten_free": item["gluten_free"],
                "vegan": item["vegan"],
                "vegetarian": item["vegetarian"],
                "dairy_free": item["dairy_free"],
                "nut_free": item["nut_free"]
            }
            nutrition_data.append(nutrition)
    
    return nutrition_data

def main():
    """Generate complete dataset"""
    output_dir = Path("grocery-data-generator/generated_data")
    output_dir.mkdir(exist_ok=True)
    
    print("🏪 Generating Las Vegas stores...")
    stores = generate_stores()
    print(f"Generated {len(stores)} stores")
    
    print("🥑 Generating grocery items...")
    items = generate_grocery_items(10000)  # 10k items
    print(f"Generated {len(items)} items")
    
    print("📦 Generating store inventory...")
    inventory = generate_store_inventory(stores, items, 1500)  # 1.5k items per store
    print(f"Generated {len(inventory)} inventory records")
    
    print("🥗 Generating nutrition facts...")
    nutrition = generate_nutrition_facts(items)
    print(f"Generated {len(nutrition)} nutrition records")
    
    print("🎯 Generating promotional offers...")
    promotions = generate_promotional_offers(items, stores)
    print(f"Generated {len(promotions)} promotional offers")
    
    print("🍂 Generating seasonal availability...")
    seasonal = generate_seasonal_availability(items)
    print(f"Generated {len(seasonal)} seasonal records")
    
    print("👨‍🍳 Generating recipe combinations...")
    recipes = generate_recipe_combinations(items) 
    print(f"Generated {len(recipes)} recipe combinations")
    
    # Save all data
    datasets = {
        "store_locations.json": stores,
        "grocery_items.json": items,
        "store_inventory.json": inventory,
        "nutrition_facts.json": nutrition,
        "promotional_offers.json": promotions,
        "seasonal_availability.json": seasonal,
        "recipe_combinations.json": recipes
    }
    
    for filename, data in datasets.items():
        filepath = output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Saved {len(data)} records to {filepath}")
    
    print("\n✅ Dataset generation complete!")
    print(f"📊 Total records: {sum(len(data) for data in datasets.values())}")

if __name__ == "__main__":
    main()
