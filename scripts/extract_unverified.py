#!/usr/bin/env python3
"""
Extract 150 unverified leads for enrichment processing
"""

import json

def extract_unverified_leads():
    # Load leadpool
    with open('src/data/leadpool.json', 'r', encoding='utf-8') as f:
        leads = json.load(f)
    
    # Find unverified leads
    unverified = [lead for lead in leads if lead.get('dataQuality') == 'unverified']
    
    print(f"Total unverified leads: {len(unverified)}")
    
    # Take first 150
    batch = unverified[:150]
    
    print(f"Extracted {len(batch)} leads for processing")
    
    # Save to separate file for processing
    with open('scripts/unverified_batch.json', 'w', encoding='utf-8') as f:
        json.dump(batch, f, indent=2, ensure_ascii=False)
    
    return batch

if __name__ == "__main__":
    extract_unverified_leads()