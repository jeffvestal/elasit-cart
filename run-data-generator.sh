#!/bin/bash
# Run grocery data generator using unified venv
source venv/bin/activate
cd grocery-data-generator
python control.py "$@"
