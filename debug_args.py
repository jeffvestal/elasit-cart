#!/usr/bin/env python3
"""
Debug script to see what model IDs we're actually receiving
"""
import sys

print("🔍 Command line arguments:")
for i, arg in enumerate(sys.argv):
    print(f"  {i}: '{arg}'")

print()

# Look for --llm-model argument
if '--llm-model' in sys.argv:
    index = sys.argv.index('--llm-model')
    if index + 1 < len(sys.argv):
        model_id = sys.argv[index + 1]
        print(f"🎯 Model ID found: '{model_id}'")
        print(f"🎯 Length: {len(model_id)}")
        print(f"🎯 Type: {type(model_id)}")
        
        # Check if it contains the ARN parts
        if 'arn:aws:bedrock' in model_id:
            print("✅ Contains ARN prefix")
        else:
            print("❌ Missing ARN prefix")
            
        if 'inference-profile' in model_id:
            print("✅ Contains inference-profile")
        else:
            print("❌ Missing inference-profile")
            
        if '461485115270' in model_id:
            print("✅ Contains account ID")
        else:
            print("❌ Missing account ID")
    else:
        print("❌ --llm-model found but no value after it")
else:
    print("❌ --llm-model not found in arguments")
