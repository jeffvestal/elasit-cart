"""
Agent Builder API integration for creating grocery shopping agents and tools
"""

import asyncio
import json
import logging
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentBuilderClient:
    """Client for Elastic Agent Builder APIs"""
    
    def __init__(self, kibana_url: str, api_key: str):
        self.kibana_url = kibana_url.rstrip('/')
        self.api_key = api_key
        self.session = None
        self.headers = {
            'Authorization': f'ApiKey {api_key}',
            'Content-Type': 'application/json',
            'kbn-xsrf': 'true'
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def create_tool(self, tool_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new tool in Agent Builder"""
        url = f"{self.kibana_url}/api/agent_builder/tools"
        
        try:
            async with self.session.post(url, json=tool_definition) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Created tool: {tool_definition['id']}")
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create tool {tool_definition['id']}: {response.status} - {error_text}")
                    raise Exception(f"Tool creation failed: {response.status} - {error_text}")
                    
        except Exception as e:
            logger.error(f"Error creating tool: {e}")
            raise
            
    async def create_agent(self, agent_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new agent in Agent Builder"""
        url = f"{self.kibana_url}/api/agent_builder/agents"
        
        try:
            async with self.session.post(url, json=agent_definition) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Created agent: {agent_definition['id']}")
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to create agent {agent_definition['id']}: {response.status} - {error_text}")
                    raise Exception(f"Agent creation failed: {response.status} - {error_text}")
                    
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            raise
            
    async def converse_with_agent(self, agent_id: str, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """Have a conversation with an agent"""
        url = f"{self.kibana_url}/api/agent_builder/converse"
        
        payload = {
            "agent_id": agent_id,
            "message": message
        }
        
        if conversation_id:
            payload["conversation_id"] = conversation_id
            
        try:
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.debug(f"Agent {agent_id} conversation successful")
                    return result
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to converse with agent {agent_id}: {response.status} - {error_text}")
                    raise Exception(f"Conversation failed: {response.status} - {error_text}")
                    
        except Exception as e:
            logger.error(f"Error in conversation: {e}")
            raise
            
    async def delete_tool(self, tool_id: str) -> bool:
        """Delete a tool"""
        url = f"{self.kibana_url}/api/agent_builder/tools/{tool_id}"
        
        try:
            async with self.session.delete(url) as response:
                if response.status == 200:
                    logger.info(f"Deleted tool: {tool_id}")
                    return True
                else:
                    logger.warning(f"Failed to delete tool {tool_id}: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting tool {tool_id}: {e}")
            return False
            
    async def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent"""
        url = f"{self.kibana_url}/api/agent_builder/agents/{agent_id}"
        
        try:
            async with self.session.delete(url) as response:
                if response.status == 200:
                    logger.info(f"Deleted agent: {agent_id}")
                    return True
                else:
                    logger.warning(f"Failed to delete agent {agent_id}: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting agent {agent_id}: {e}")
            return False


class GroceryAgentBuilder:
    """Builder for grocery shopping agents and tools"""
    
    def __init__(self, agent_client: AgentBuilderClient, session_id: str):
        self.agent_client = agent_client
        self.session_id = session_id
        self.created_tools = []
        self.created_agents = []
        
    async def create_all_tools(self) -> List[Dict[str, Any]]:
        """Create all grocery shopping tools"""
        tools = [
            self._get_search_grocery_items_tool(),
            self._get_find_budget_items_tool(), 
            self._get_find_deals_tool(),
            self._get_check_nutrition_tool(),
            self._get_find_recipe_items_tool(),
            self._get_check_store_inventory_tool(),
            self._get_seasonal_recommendations_tool(),
            self._get_dietary_filter_tool()
        ]
        
        created_tools = []
        for tool in tools:
            try:
                result = await self.agent_client.create_tool(tool)
                created_tools.append(result)
                self.created_tools.append(tool['id'])
            except Exception as e:
                logger.error(f"Failed to create tool {tool['id']}: {e}")
                
        logger.info(f"Created {len(created_tools)} tools for session {self.session_id}")
        return created_tools
        
    async def create_all_agents(self) -> List[Dict[str, Any]]:
        """Create all grocery shopping agents"""
        agents = [
            self._get_budget_master_agent(),
            self._get_health_guru_agent(),
            self._get_gourmet_chef_agent(),
            self._get_speed_shopper_agent(),
            self._get_local_expert_agent()
        ]
        
        created_agents = []
        for agent in agents:
            try:
                result = await self.agent_client.create_agent(agent)
                created_agents.append(result)
                self.created_agents.append(agent['id'])
            except Exception as e:
                logger.error(f"Failed to create agent {agent['id']}: {e}")
                
        logger.info(f"Created {len(created_agents)} agents for session {self.session_id}")
        return created_agents
        
    async def cleanup_session(self):
        """Clean up all tools and agents created for this session"""
        logger.info(f"Cleaning up session {self.session_id}")
        
        # Delete agents first (they depend on tools)
        for agent_id in self.created_agents:
            await self.agent_client.delete_agent(agent_id)
            
        # Then delete tools
        for tool_id in self.created_tools:
            await self.agent_client.delete_tool(tool_id)
            
        logger.info(f"Session {self.session_id} cleanup complete")
        
    def _get_search_grocery_items_tool(self) -> Dict[str, Any]:
        """Core grocery search tool available to all agents"""
        return {
            "id": f"search_grocery_items_{self.session_id}",
            "description": "Search for grocery items by name, category, or description. Returns items with current prices and availability across stores.",
            "labels": ["retrieval", "grocery", "search"],
            "configuration": """
FROM grocery_items
| WHERE name LIKE CONCAT("*", ?search_term, "*") 
   OR category LIKE CONCAT("*", ?search_term, "*")
   OR description LIKE CONCAT("*", ?search_term, "*")
| EVAL item_key = CONCAT(item_id, "_", name)
| LOOKUP JOIN store_inventory ON item_id
| WHERE stock_status != "out_of_stock"
| EVAL final_price = CASE(on_sale, sale_price, current_price)
| STATS avg_price = AVG(final_price), 
        min_price = MIN(final_price),
        max_price = MAX(final_price),
        stores_available = COUNT_DISTINCT(store_id)
  BY item_id, name, brand, category, unit_size, organic, gluten_free, vegan
| WHERE stores_available > 0
| SORT avg_price ASC
| LIMIT 20
            """,
            "parameters": [
                {
                    "name": "search_term",
                    "description": "The search term for grocery items (name, category, or description)"
                }
            ]
        }
        
    def _get_find_budget_items_tool(self) -> Dict[str, Any]:
        """Tool for finding budget-friendly items"""
        return {
            "id": f"find_budget_items_{self.session_id}",
            "description": "Find the most budget-friendly items within a price range and category. Prioritizes discount stores and sale items.",
            "labels": ["budget", "deals", "savings"],
            "configuration": """
FROM grocery_items
| WHERE base_price <= ?max_price 
| EVAL category_filter = CASE(?category == "any", true, category == ?category)
| WHERE category_filter
| LOOKUP JOIN store_inventory ON item_id
| LOOKUP JOIN store_locations ON store_id  
| WHERE stock_status == "in_stock" AND chain_tier IN ("discount", "mid-range")
| EVAL final_price = CASE(on_sale, sale_price, current_price)
| EVAL savings = CASE(on_sale, current_price - sale_price, 0)
| STATS min_price = MIN(final_price),
        max_savings = MAX(savings),
        best_store = FIRST(store_id, final_price)
  BY item_id, name, brand, category, unit_size
| EVAL value_score = (100 - min_price) + (max_savings * 2)
| SORT value_score DESC
| LIMIT 15
            """,
            "parameters": [
                {
                    "name": "max_price", 
                    "description": "Maximum price per item in dollars"
                },
                {
                    "name": "category",
                    "description": "Product category to search in, or 'any' for all categories"
                }
            ]
        }
        
    def _get_find_deals_tool(self) -> Dict[str, Any]:
        """Tool for finding current deals and promotions"""
        return {
            "id": f"find_deals_{self.session_id}",
            "description": "Find current promotional offers, sales, and bundle deals across all stores.",
            "labels": ["promotions", "deals", "sales"],
            "configuration": """
FROM promotional_offers
| WHERE active == true 
  AND start_date <= NOW() 
  AND end_date >= NOW()
| EVAL promo_items = MV_EXPAND(item_ids)
| LOOKUP JOIN grocery_items ON promo_items AS item_id
| LOOKUP JOIN store_locations ON store_id
| EVAL discount_value = CASE(
    promo_type == "discount", discount_percent,
    promo_type == "bogo", 50,
    promo_type == "bulk_discount", discount_percent,
    0
  )
| WHERE discount_value > 0
| STATS promotion_count = COUNT(*),
        avg_discount = AVG(discount_value),
        items = MV_DEDUPE(COLLECT(name))
  BY promo_id, store_id, chain_name, promo_type, description, end_date
| SORT avg_discount DESC
| LIMIT 10
            """,
            "parameters": []
        }
        
    def _get_check_nutrition_tool(self) -> Dict[str, Any]:
        """Tool for checking nutritional information"""
        return {
            "id": f"check_nutrition_{self.session_id}",
            "description": "Get detailed nutritional information for grocery items, including calories, macros, and dietary classifications.",
            "labels": ["nutrition", "health", "dietary"],
            "configuration": """
FROM grocery_items
| WHERE name LIKE CONCAT("*", ?item_search, "*")
| LOOKUP JOIN nutrition_facts ON item_id
| EVAL dietary_flags = CONCAT(
    CASE(organic, "Organic ", ""),
    CASE(gluten_free, "Gluten-Free ", ""),
    CASE(vegan, "Vegan ", ""),
    CASE(dairy_free, "Dairy-Free ", "")
  )
| EVAL macro_summary = CONCAT(
    "Calories: ", COALESCE(calories, 0), 
    " | Fat: ", COALESCE(total_fat, 0), "g",
    " | Carbs: ", COALESCE(total_carbs, 0), "g", 
    " | Protein: ", COALESCE(protein, 0), "g"
  )
| KEEP item_id, name, brand, serving_size, macro_summary, dietary_flags, allergens
| LIMIT 10
            """,
            "parameters": [
                {
                    "name": "item_search",
                    "description": "Search term for the grocery item to get nutrition info"
                }
            ]
        }
        
    def _get_find_recipe_items_tool(self) -> Dict[str, Any]:
        """Tool for finding items that work well together in recipes"""
        return {
            "id": f"find_recipe_items_{self.session_id}",
            "description": "Find grocery items that work together for specific recipes or meal themes.",
            "labels": ["recipes", "meal-planning", "combinations"],
            "configuration": """
FROM recipe_combinations
| WHERE theme LIKE CONCAT("*", ?meal_theme, "*")
  OR recipe_name LIKE CONCAT("*", ?meal_theme, "*")
| EVAL all_items = MV_APPEND(COLLECT(primary_item_id), complementary_items)
| EVAL recipe_item = MV_EXPAND(all_items)
| LOOKUP JOIN grocery_items ON recipe_item AS item_id
| LOOKUP JOIN store_inventory ON item_id
| WHERE stock_status == "in_stock"
| EVAL final_price = CASE(on_sale, sale_price, current_price)
| STATS avg_price = AVG(final_price),
        available_stores = COUNT_DISTINCT(store_id),
        recipes_count = COUNT_DISTINCT(combo_id)
  BY item_id, name, category, unit_size
| WHERE available_stores > 0
| SORT recipes_count DESC, avg_price ASC
| LIMIT 12
            """,
            "parameters": [
                {
                    "name": "meal_theme",
                    "description": "The meal theme or cuisine type (e.g., 'italian', 'healthy', 'breakfast')"
                }
            ]
        }
        
    def _get_check_store_inventory_tool(self) -> Dict[str, Any]:
        """Tool for checking inventory at specific stores"""
        return {
            "id": f"check_store_inventory_{self.session_id}",
            "description": "Check current inventory levels and prices at specific stores or store chains.",
            "labels": ["inventory", "stores", "availability"],
            "configuration": """
FROM store_inventory
| LOOKUP JOIN store_locations ON store_id
| LOOKUP JOIN grocery_items ON item_id
| WHERE chain_tier LIKE CONCAT("*", ?store_tier, "*")
  OR chain_name LIKE CONCAT("*", ?store_tier, "*")
| WHERE stock_status != "out_of_stock"
| EVAL final_price = CASE(on_sale, sale_price, current_price)
| EVAL deal_indicator = CASE(on_sale, CONCAT("SALE: $", TO_STRING(final_price)), "")
| STATS items_available = COUNT(*),
        avg_price = AVG(final_price),
        deals_count = COUNT(CASE(on_sale, 1, null))
  BY store_id, chain_name, chain_tier, address.city
| SORT items_available DESC
| LIMIT 8
            """,
            "parameters": [
                {
                    "name": "store_tier",
                    "description": "Store tier or chain name (discount, premium, luxury, or specific chain name)"
                }
            ]
        }
        
    def _get_seasonal_recommendations_tool(self) -> Dict[str, Any]:
        """Tool for seasonal product recommendations"""
        return {
            "id": f"seasonal_recommendations_{self.session_id}",
            "description": "Get seasonal product recommendations with current availability and pricing.",
            "labels": ["seasonal", "fresh", "recommendations"],
            "configuration": """
FROM seasonal_availability
| WHERE season == ?current_season
  AND availability_score > 0.6
| LOOKUP JOIN grocery_items ON item_id
| LOOKUP JOIN store_inventory ON item_id
| WHERE stock_status == "in_stock"
| EVAL final_price = CASE(on_sale, sale_price, current_price)
| EVAL seasonal_price = final_price * price_multiplier
| EVAL seasonal_indicator = CASE(
    availability_score > 0.8, "PEAK SEASON",
    availability_score > 0.6, "IN SEASON",
    "LIMITED"
  )
| STATS avg_seasonal_price = AVG(seasonal_price),
        availability_rating = MAX(availability_score),
        stores_count = COUNT_DISTINCT(store_id)
  BY item_id, name, category, seasonal_indicator, description
| SORT availability_rating DESC, avg_seasonal_price ASC
| LIMIT 10
            """,
            "parameters": [
                {
                    "name": "current_season",
                    "description": "Current season (spring, summer, fall, winter)"
                }
            ]
        }
        
    def _get_dietary_filter_tool(self) -> Dict[str, Any]:
        """Tool for filtering by dietary restrictions"""
        return {
            "id": f"dietary_filter_{self.session_id}",
            "description": "Filter grocery items by dietary restrictions and preferences (vegan, gluten-free, organic, etc.).",
            "labels": ["dietary", "restrictions", "health"],
            "configuration": """
FROM grocery_items
| EVAL meets_organic = CASE(?organic_required, organic == true, true)
| EVAL meets_gluten_free = CASE(?gluten_free_required, gluten_free == true, true)  
| EVAL meets_vegan = CASE(?vegan_required, vegan == true, true)
| EVAL meets_dairy_free = CASE(?dairy_free_required, dairy_free == true, true)
| WHERE meets_organic AND meets_gluten_free AND meets_vegan AND meets_dairy_free
| LOOKUP JOIN store_inventory ON item_id
| WHERE stock_status == "in_stock"
| EVAL final_price = CASE(on_sale, sale_price, current_price)
| EVAL dietary_labels = CONCAT(
    CASE(organic, "🌱 Organic ", ""),
    CASE(gluten_free, "🚫 Gluten-Free ", ""),
    CASE(vegan, "🌿 Vegan ", ""),
    CASE(dairy_free, "🥛 Dairy-Free ", "")
  )
| STATS avg_price = AVG(final_price),
        stores_available = COUNT_DISTINCT(store_id)
  BY item_id, name, brand, category, dietary_labels
| SORT avg_price ASC
| LIMIT 15
            """,
            "parameters": [
                {
                    "name": "organic_required",
                    "description": "Require organic products (true/false)"
                },
                {
                    "name": "gluten_free_required", 
                    "description": "Require gluten-free products (true/false)"
                },
                {
                    "name": "vegan_required",
                    "description": "Require vegan products (true/false)"
                },
                {
                    "name": "dairy_free_required",
                    "description": "Require dairy-free products (true/false)"
                }
            ]
        }
        
    def _get_budget_master_agent(self) -> Dict[str, Any]:
        """Budget-focused shopping agent"""
        tools = [
            f"search_grocery_items_{self.session_id}",
            f"find_budget_items_{self.session_id}",
            f"find_deals_{self.session_id}",
            f"check_store_inventory_{self.session_id}"
        ]
        
        return {
            "id": f"budget_master_{self.session_id}",
            "name": "Budget Master",
            "description": "Your personal savings expert for grocery shopping. Specializes in finding the best deals, comparing prices across stores, and maximizing your shopping budget.",
            "instructions": """You are the Budget Master, a friendly and savvy grocery shopping expert who helps customers get the most value for their money. Your mission is to help players build a grocery cart that gets as close to $100 as possible without going over, while finding the best deals available.

**Your Personality:**
- Enthusiastic about savings and deals
- Practical and cost-conscious
- Always looking for ways to stretch a dollar
- Encouraging and supportive

**Your Expertise:**
- Finding the lowest prices across different stores
- Identifying sales, promotions, and special offers  
- Comparing unit prices and value propositions
- Recommending store brands and bulk options
- Spotting seasonal deals and clearance items

**Game Strategy:**
- Focus on maximizing total value while staying under $100
- Prioritize items on sale or with promotional offers
- Look for high-value items that fill multiple needs
- Consider quantity vs. price relationships
- Always check multiple stores for the best prices

**Communication Style:**
- Start responses with enthusiasm about savings opportunities
- Provide specific price comparisons when available
- Explain why certain choices offer better value
- Give practical shopping tips
- Celebrate good deals and smart choices

Remember: Your goal is to help the player win by getting closest to $100 without going over, while making their shopping budget work as hard as possible!""",
            "labels": ["budget", "savings", "deals"],
            "tools": tools
        }
        
    def _get_health_guru_agent(self) -> Dict[str, Any]:
        """Health and nutrition focused agent"""
        tools = [
            f"search_grocery_items_{self.session_id}",
            f"check_nutrition_{self.session_id}",
            f"dietary_filter_{self.session_id}",
            f"seasonal_recommendations_{self.session_id}"
        ]
        
        return {
            "id": f"health_guru_{self.session_id}",
            "name": "Health Guru",
            "description": "Your wellness-focused shopping companion. Specializes in nutritious choices, dietary restrictions, and healthy meal planning while staying within budget.",
            "instructions": """You are the Health Guru, a knowledgeable and encouraging nutrition expert who helps customers make healthy grocery choices. Your mission is to help players build a nutritious, well-balanced grocery cart that reaches $100 while supporting their health goals.

**Your Personality:**
- Passionate about health and wellness
- Knowledgeable about nutrition and dietary needs
- Encouraging without being preachy
- Practical about balancing health and budget

**Your Expertise:**
- Understanding nutritional value and ingredient quality
- Managing dietary restrictions (gluten-free, vegan, dairy-free, etc.)
- Identifying organic and natural options
- Seasonal produce recommendations
- Balanced meal planning and nutrient density
- Reading nutrition labels and ingredient lists

**Game Strategy:**
- Build a nutritionally balanced cart across food groups
- Prioritize fresh, whole foods when possible
- Find healthy options that offer good value
- Consider nutrient density per dollar spent
- Balance indulgences with nutritious choices

**Communication Style:**
- Lead with health benefits and nutritional value
- Explain why certain foods support wellness goals
- Offer alternatives for dietary restrictions
- Share interesting nutrition facts
- Encourage healthy choices while respecting preferences

Remember: Help the player win by reaching $100 with a cart that's not just budget-friendly, but also supports their health and wellness goals!""",
            "labels": ["health", "nutrition", "dietary"],
            "tools": tools
        }
        
    def _get_gourmet_chef_agent(self) -> Dict[str, Any]:
        """Culinary-focused shopping agent"""
        tools = [
            f"search_grocery_items_{self.session_id}",
            f"find_recipe_items_{self.session_id}",
            f"seasonal_recommendations_{self.session_id}",
            f"check_store_inventory_{self.session_id}"
        ]
        
        return {
            "id": f"gourmet_chef_{self.session_id}",
            "name": "Gourmet Chef",
            "description": "Your culinary adventure guide. Specializes in recipe combinations, premium ingredients, and creating memorable meals within your shopping budget.",
            "instructions": """You are the Gourmet Chef, a culinary enthusiast and experienced cook who helps customers create amazing meals through thoughtful ingredient selection. Your mission is to help players build a grocery cart that reaches $100 while creating possibilities for delicious, memorable meals.

**Your Personality:**
- Passionate about food and cooking
- Creative and inspiring
- Knowledgeable about flavors and techniques
- Appreciates quality ingredients

**Your Expertise:**
- Understanding flavor combinations and recipe harmony
- Identifying premium and specialty ingredients
- Seasonal cooking and ingredient availability
- Recipe development and meal planning
- Quality differences between brands and products
- Cooking techniques and ingredient preparation

**Game Strategy:**
- Build carts around cohesive meal themes or recipes
- Balance premium ingredients with budget-conscious choices
- Look for versatile ingredients that work in multiple dishes
- Consider seasonal specialties and peak-flavor items
- Create inspiring meal possibilities

**Communication Style:**
- Share culinary enthusiasm and inspiration
- Explain how ingredients work together in recipes
- Describe flavors, textures, and cooking possibilities
- Offer cooking tips and technique suggestions
- Paint appetizing pictures of potential meals

Remember: Help the player win by reaching $100 with ingredients that will create memorable, delicious meals that showcase the art of good cooking!""",
            "labels": ["gourmet", "recipes", "cooking"],
            "tools": tools
        }
        
    def _get_speed_shopper_agent(self) -> Dict[str, Any]:
        """Quick and efficient shopping agent"""
        tools = [
            f"search_grocery_items_{self.session_id}",
            f"find_budget_items_{self.session_id}",
            f"check_store_inventory_{self.session_id}"
        ]
        
        return {
            "id": f"speed_shopper_{self.session_id}",
            "name": "Speed Shopper",
            "description": "Your efficiency expert for quick, smart shopping decisions. Specializes in popular items, quick wins, and time-saving strategies.",
            "instructions": """You are the Speed Shopper, a fast-paced, efficient shopping expert who helps customers make quick, smart decisions. Your mission is to help players rapidly build a grocery cart that reaches $100 with popular, reliable choices.

**Your Personality:**
- Fast-paced and energetic
- Decisive and confident
- Focused on efficiency and results
- Practical and no-nonsense

**Your Expertise:**
- Identifying popular, crowd-pleasing items
- Making quick value assessments
- Finding reliable, tried-and-true products
- Streamlining shopping decisions
- Recognizing must-have staples and basics

**Game Strategy:**
- Make rapid progress toward the $100 target
- Choose popular items with broad appeal
- Focus on proven winners and customer favorites
- Avoid over-analyzing - go with solid choices
- Build momentum with quick, confident selections

**Communication Style:**
- Keep responses concise and action-oriented
- Provide clear, direct recommendations
- Use energetic, motivating language
- Focus on efficiency and speed
- Celebrate quick decision-making

Remember: Time is ticking! Help the player win by quickly reaching $100 with smart, popular choices that don't require lengthy deliberation!""",
            "labels": ["efficiency", "speed", "popular"],
            "tools": tools
        }
        
    def _get_local_expert_agent(self) -> Dict[str, Any]:
        """Las Vegas local shopping expert"""
        tools = [
            f"search_grocery_items_{self.session_id}",
            f"check_store_inventory_{self.session_id}",
            f"find_deals_{self.session_id}",
            f"seasonal_recommendations_{self.session_id}"
        ]
        
        return {
            "id": f"local_expert_{self.session_id}",
            "name": "Vegas Local Expert", 
            "description": "Your Las Vegas shopping insider. Knows the best stores, local specialties, and where to find the best deals across Sin City's grocery landscape.",
            "instructions": """You are the Vegas Local Expert, a Las Vegas native who knows the ins and outs of the city's grocery scene. Your mission is to help players build a grocery cart that reaches $100 while leveraging your insider knowledge of local stores, deals, and specialties.

**Your Personality:**
- Knowledgeable local with insider tips
- Friendly and welcoming to visitors
- Proud of Las Vegas and its unique character
- Helpful and resourceful

**Your Expertise:**
- Understanding the different Las Vegas store chains and their strengths
- Knowing which stores have the best deals and specialties
- Local preferences and regional favorites
- Store locations and accessibility
- Seasonal patterns specific to the Las Vegas market

**Game Strategy:**
- Leverage knowledge of which stores offer best value for different categories
- Recommend items that locals love and visitors should try
- Use store-specific advantages and specialties
- Consider the unique Las Vegas market and preferences
- Share insider tips about store promotions and patterns

**Store Chain Knowledge:**
- **Dice Mart**: Best for budget basics and everyday essentials
- **Jackpot Grocers**: Great family stores with good variety
- **All-In Foods**: Convenient locations with solid selections
- **Lucky Strike Market**: Premium fresh produce and organic options
- **High Roller Gourmet**: Luxury items and specialty ingredients

**Communication Style:**
- Share local knowledge and insider tips  
- Reference specific Las Vegas stores and their strengths
- Use welcoming, friendly local tone
- Mention what makes Vegas shopping unique
- Give practical advice about store locations and specialties

Remember: You're the local insider helping players win by reaching $100 while experiencing the best of Las Vegas grocery shopping!""",
            "labels": ["local", "vegas", "insider"],
            "tools": tools
        }


async def create_session_agents(kibana_url: str, api_key: str, session_id: str) -> GroceryAgentBuilder:
    """Create all agents and tools for a game session"""
    async with AgentBuilderClient(kibana_url, api_key) as client:
        builder = GroceryAgentBuilder(client, session_id)
        
        # Create tools first (agents depend on them)
        await builder.create_all_tools()
        
        # Then create agents
        await builder.create_all_agents()
        
        return builder
