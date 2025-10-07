#!/bin/bash

# Elasti-Cart Index Recreation Workflow
# This script recreates all indices with LOOKUP mode for ES|QL LOOKUP JOIN support

echo "🚀 Elasti-Cart Index Recreation for LOOKUP JOIN Support"
echo "============================================================"
echo

# Check if we're in the right directory
if [ ! -f "control.py" ]; then
    echo "❌ Please run this script from the grocery-data-generator directory"
    exit 1
fi

echo "📋 This script will:"
echo "   1. Delete all existing grocery indices"
echo "   2. Recreate them with 'index.mode: lookup' setting"
echo "   3. Reload your grocery data"
echo

read -p "⚠️  This will DELETE all existing data. Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted by user"
    exit 1
fi

echo

# Set Elasticsearch connection (you may need to update these)
export ES_URL="${ES_URL:-https://your-cluster.es.cloud.es.io:443}"
export ES_API_KEY="${ES_API_KEY:-your-api-key}"

# Check if environment variables are set
if [ "$ES_URL" = "https://your-cluster.es.cloud.es.io:443" ] || [ "$ES_API_KEY" = "your-api-key" ]; then
    echo "❌ Please set your Elasticsearch connection details:"
    echo "   export ES_URL='https://your-cluster.es.cloud.es.io:443'"
    echo "   export ES_API_KEY='your-api-key'"
    echo
    echo "   Then run this script again."
    exit 1
fi

echo "🔗 Using Elasticsearch:"
echo "   URL: $ES_URL"
echo "   API Key: ${ES_API_KEY:0:10}..."
echo

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Activated virtual environment"
else
    echo "❌ Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Step 1: Recreate indices
echo
echo "🗂️  Step 1: Recreating indices with LOOKUP mode..."
python recreate_indices.py
if [ $? -ne 0 ]; then
    echo "❌ Failed to recreate indices"
    exit 1
fi

# Step 2: Reload data
echo
echo "📊 Step 2: Reloading grocery data..."
python control.py --action load-only
if [ $? -ne 0 ]; then
    echo "❌ Failed to reload data"
    exit 1
fi

echo
echo "🎉 SUCCESS! Indices recreated with LOOKUP mode and data reloaded!"
echo
echo "🧪 Next: Test your Agent Builder tools with LOOKUP JOIN support:"
echo "   cd ../agent-builder-service"
echo "   source venv/bin/activate"  
echo "   export KIBANA_URL=https://elasti-cart-b92fb1.kb.us-east-1.aws.elastic.cloud"
echo "   export KIBANA_API_KEY=a1c0RXNwa0I3MDZPSlQ3UTl5em86NlBkak5QZnhXNHFQSnpPVzRrS3hNUQ=="
echo "   python -c 'import asyncio; from agent_builder_client import create_demo_session; asyncio.run(create_demo_session())'"
