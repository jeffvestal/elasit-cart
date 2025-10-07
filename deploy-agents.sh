#!/bin/bash
# Deploy updated agents to Kibana Agent Builder
echo "🚀 Deploying updated agents..."

# Check for required environment variables
if [ -z "$KIBANA_URL" ] || [ -z "$KIBANA_API_KEY" ]; then
    echo "❌ Missing required environment variables!"
    echo "Please set:"
    echo "  export KIBANA_URL='https://your-kibana.kb.cloud.es.io'"
    echo "  export KIBANA_API_KEY='your_kibana_api_key'"
    echo ""
    echo "Then run: ./deploy-agents.sh"
    exit 1
fi

source venv/bin/activate
python deploy_updated_agents.py
