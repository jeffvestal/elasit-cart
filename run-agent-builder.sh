#!/bin/bash
# Run Agent Builder client using unified venv
source venv/bin/activate
cd agent-builder-service
python agent_builder_client.py "$@"
