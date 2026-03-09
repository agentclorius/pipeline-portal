#!/usr/bin/env python3
import json
import sys

def filter_unverified_leads(file_path, limit=150):
    """Filter for unverified leads from leadpool"""
    with open(file_path, 'r') as f:
        leads = json.load(f)
    
    unverified = []
    for lead in leads:
        if lead.get('dataQuality') != 'verified':
            unverified.append(lead)
        if len(unverified) >= limit:
            break
    
    return unverified

if __name__ == "__main__":
    leads = filter_unverified_leads('/tmp/pipeline-portal/src/data/leadpool.json')
    print(f"Found {len(leads)} unverified leads")
    
    for i, lead in enumerate(leads):
        print(f"\n{i+1}. {lead['name']}")
        print(f"   Website: {lead.get('website', 'NO WEBSITE')}")
        print(f"   Location: {lead.get('address', 'No address')}, {lead.get('country', 'No country')}")
        print(f"   Data Quality: {lead.get('dataQuality', 'unknown')}")
        print(f"   ID: {lead['id']}")
        
        if i >= 10:  # Show first 10 for preview
            print(f"\n... and {len(leads) - 10} more leads to process")
            break