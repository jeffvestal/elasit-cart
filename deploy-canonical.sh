#!/bin/bash
# Deploy canonical agent and tool definitions to any cluster

echo "🚀 Deploying Canonical Definitions..."
echo ""

# Check for required environment variables
if [ -z "$KIBANA_URL" ] || [ -z "$KIBANA_API_KEY" ]; then
    echo "❌ Missing required environment variables!"
    echo "Please set:"
    echo "  export KIBANA_URL='https://your-kibana.kb.cloud.es.io'"
    echo "  export KIBANA_API_KEY='your_kibana_api_key'"
    echo ""
    echo "Then run: ./deploy-canonical.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run deployment
python deploy_canonical_agents.py "$@"

