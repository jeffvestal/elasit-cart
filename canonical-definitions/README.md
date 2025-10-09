# Canonical Agent Builder Definitions

This directory contains the canonical, production-ready definitions for all Elasti-Cart Agent Builder tools and agents. These definitions are used for consistent, reproducible deployments across any Elasticsearch cluster.

## Files

- **`tools.json`** - All 8 grocery shopping tools with correct ES|QL queries
- **`agents.json`** - All 5 shopping agent personalities with their configurations

## Tools

1. **search_grocery_items** - Core search tool for finding items by name, category, or description
2. **find_budget_items** - Find items in optimal price ranges ($15-25) for building $100 carts
3. **find_deals** - Current promotional offers and sales
4. **check_nutrition** - Detailed nutritional information
5. **find_recipe_items** - Items that work together for recipes
6. **check_store_inventory** - Real-time inventory levels (FIXED: searches by name OR item_id)
7. **seasonal_recommendations** - Seasonal product recommendations
8. **dietary_filter** - Filter by dietary restrictions (vegan, gluten-free, etc.)

## Agents

1. **budget_master** - Savings expert, finds best deals
2. **health_guru** - Wellness-focused, nutrition emphasis
3. **gourmet_chef** - Culinary expert, recipe combinations
4. **speed_shopper** - Efficiency expert, popular items
5. **local_expert** - Las Vegas insider, local specialties

## Deployment

### Quick Deploy

```bash
# Set your target cluster
export KIBANA_URL=https://your-cluster.kb.cloud.es.io
export KIBANA_API_KEY=your_api_key

# Deploy (will fail if tools/agents already exist)
./deploy-canonical.sh

# Or force redeploy (deletes existing first)
./deploy-canonical.sh --delete-existing
```

### Manual Deploy

```bash
source venv/bin/activate
python deploy_canonical_agents.py
```

## Schema Format

### Tools

```json
{
  "id": "tool_name",
  "type": "esql",
  "description": "What the tool does",
  "tags": ["tag1", "tag2"],
  "configuration": {
    "query": "FROM index | ...",
    "params": {
      "param_name": {
        "type": "keyword|double|boolean",
        "description": "Parameter description"
      }
    }
  },
  "readonly": false
}
```

### Agents

```json
{
  "id": "agent_name",
  "type": "chat",
  "name": "Agent Display Name",
  "description": "What the agent does",
  "labels": ["label1", "label2"],
  "configuration": {
    "instructions": "Agent personality and behavior...",
    "tools": [
      {
        "tool_ids": ["tool1", "tool2", "..."]
      }
    ]
  },
  "readonly": false
}
```

## Key Fixes Applied

### check_store_inventory Tool
- **Problem**: Query was `WHERE item_id: ?item_query` which only matched item IDs
- **Solution**: Changed to `WHERE name: ?item_query OR item_id: ?item_query`
- **Result**: Tool now searches by product name (like "tilapia") OR item ID

This fix allows agents to search for products by their common names instead of requiring exact item IDs, making the tool much more useful.

## Updating Canonical Definitions

To update these definitions after making changes in the UI or via API:

```bash
# Export current production definitions
export KIBANA_URL=https://your-cluster.kb.cloud.es.io
export KIBANA_API_KEY=your_api_key

# Download current state
curl -s "${KIBANA_URL}/api/agent_builder/tools" \
  -H "Authorization: ApiKey ${KIBANA_API_KEY}" \
  -H "kbn-xsrf: true" | \
  jq '[.results[] | select(.readonly == false)]' > canonical-definitions/tools.json

curl -s "${KIBANA_URL}/api/agent_builder/agents" \
  -H "Authorization: ApiKey ${KIBANA_API_KEY}" \
  -H "kbn-xsrf: true" | \
  jq '[.results[] | select(.readonly == false)]' > canonical-definitions/agents.json

# Commit the changes
git add canonical-definitions/
git commit -m "Update canonical agent definitions"
```

## Testing Deployments

After deployment, test that tools work correctly:

```bash
# Test the fixed check_store_inventory tool
curl -s "http://localhost:3000/api/agent-chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "check inventory for tilapia", "agentId": "speed_shopper", "streaming": false}' | \
  jq '.steps[] | select(.type == "tool_call" and (.tool_id | contains("check_store_inventory")))'
```

## Data Requirements

These tools expect the following Elasticsearch indices with grocery data:

- `grocery_items` - Items with prices, categories, nutrition
- `store_inventory` - Stock levels per store  
- `store_locations` - Store details and specialties
- `seasonal_availability` - Seasonal item data
- `promotional_offers` - Sales and deals
- `nutrition_facts` - Detailed nutrition info
- `recipe_combinations` - Recipe suggestions

Generate this data using:

```bash
./run-data-generator.sh --action generate-and-load
```

