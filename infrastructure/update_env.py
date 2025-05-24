#!/usr/bin/env python3
"""
Script to update .env file with Pulumi output values
"""
import os
import subprocess
import json
from dotenv import load_dotenv, set_key
import sys

# Load current .env file
load_dotenv()

# Check if we're in the right directory
if not os.path.exists("../pyproject.toml"):
    print("Error: This script should be run from the 'infrastructure' directory")
    sys.exit(1)

# Get Pulumi stack name from command line or use default
stack_name = sys.argv[1] if len(sys.argv) > 1 else "dev"

try:
    # Run pulumi stack output command to get values
    result = subprocess.run(
        ["pulumi", "stack", "output", "--json", "--stack", stack_name],
        capture_output=True,
        text=True,
        check=True
    )
    
    # Parse JSON output
    outputs = json.loads(result.stdout)
    
    # Update .env file with values
    env_file = "../.env"
    
    # Update S3 bucket name
    if "bucket_name" in outputs:
        set_key(env_file, "S3_BUCKET_NAME", outputs["bucket_name"])
        print(f"Updated S3_BUCKET_NAME to {outputs['bucket_name']}")
    
    # Update CloudFront domain
    if "cdn_domain" in outputs:
        set_key(env_file, "CLOUDFRONT_DOMAIN", outputs["cdn_domain"])
        print(f"Updated CLOUDFRONT_DOMAIN to {outputs['cdn_domain']}")
        
    print(f"Successfully updated {env_file} with Pulumi output values")
    
except subprocess.CalledProcessError as e:
    print(f"Error running Pulumi command: {e}")
    print(f"Output: {e.stderr}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit(1)
