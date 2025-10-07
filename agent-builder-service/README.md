# Agent Builder Service

This service manages the creation and lifecycle of Elastic Agent Builder agents and tools for the Elasti-Cart game.

## Setup

1. **Install dependencies:**
   ```bash
   cd agent-builder-service
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Create a `.env` file with your Kibana connection details:
   ```bash
   KIBANA_URL=https://your-cluster.es.cloud.es.io:9243
   KIBANA_API_KEY=your-api-key-here
   ```

   To create a Kibana API key:
   1. Go to Kibana > Stack Management > API Keys
   2. Click "Create API Key"
   3. Give it a name like "elasti-cart-agent-builder"
   4. Copy the encoded key

## Testing

**Test connection:**
```bash
python test_connection.py
```

**Interactive test menu:**
```bash
python agent_builder_client.py
```

## Components

### 🤖 **5 Specialized Agents:**
1. **Budget Master** - Cost-focused shopping, finds best deals
2. **Health Guru** - Nutrition and dietary focused
3. **Gourmet Chef** - Culinary excellence, premium ingredients
4. **Speed Shopper** - Quick and efficient shopping
5. **Local Expert** - Las Vegas shopping specialist

### 🛠️ **8 Specialized Tools:**
1. **Search Grocery Items** - Core search with ES|QL
2. **Find Budget Items** - Price-focused queries
3. **Find Deals** - Promotional offers and sales
4. **Check Nutrition** - Dietary information and ingredients
5. **Find Recipe Items** - Recipe-based shopping lists
6. **Check Store Inventory** - Real-time stock levels
7. **Seasonal Recommendations** - Seasonal items and availability
8. **Dietary Filter** - Filter by dietary restrictions

## Usage in Game

```python
from agent_builder_client import create_session_agents

# Create all agents for a game session
builder = await create_session_agents(
    kibana_url="https://your-cluster.es.cloud.es.io:9243",
    api_key="your-api-key",
    session_id="player-123"
)

# Agents are now available for the player to choose from
# Each agent has different personalities and tool access

# Clean up when session ends
await builder.cleanup_session()
```

## Architecture

- **AgentBuilderClient**: Low-level API client for Kibana Agent Builder
- **GroceryAgentBuilder**: High-level builder for game-specific agents
- **Session Management**: Creates isolated agents per game session
- **ES|QL Integration**: All tools use Elasticsearch Query Language for data access

## Data Requirements

The agents expect these Elasticsearch indices with grocery data:
- `grocery_items` - Items with prices, categories, nutrition
- `store_inventory` - Stock levels per store
- `store_locations` - Store details and specialties  
- `seasonal_availability` - Seasonal item data
- `promotional_offers` - Sales and deals
- `nutrition_facts` - Detailed nutrition info
- `recipe_combinations` - Recipe suggestions

## Agent Personalities

Each agent has a unique personality and specialized tools:

- **Budget Master**: "Your penny-pinching champion!" - Focuses on value and savings
- **Health Guru**: "Your wellness warrior!" - Emphasizes nutrition and health
- **Gourmet Chef**: "Your culinary maestro!" - Seeks premium quality ingredients
- **Speed Shopper**: "Your efficiency expert!" - Optimizes for quick shopping
- **Local Expert**: "Your Vegas insider!" - Knows Las Vegas stores and specialties

## Next Steps

1. **Deploy to Instruqt**: Integrate with per-user Elasticsearch clusters
2. **Game Integration**: Connect with the game UI for agent selection
3. **Observability**: Add metrics and logging for agent performance
4. **Scaling**: Handle concurrent game sessions and agent management
