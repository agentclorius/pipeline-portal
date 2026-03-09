#!/usr/bin/env python3
import json
from datetime import datetime

def update_leadpool_batch2():
    """Update leads from second screening batch"""
    
    # Load data
    with open('/tmp/pipeline-portal/src/data/leadpool.json', 'r') as f:
        leads = json.load(f)
    
    # Define updates for batch 2
    updates = {
        'Emporium Partners': {
            'dataQuality': 'rejected',
            'notes': ['Auto-screened 2026-03-09: Electronic components supply chain/procurement services - not ITAD focused. Website: https://emporiumpartners.com/']
        },
        'Itectra': {
            'dataQuality': 'rejected', 
            'notes': ['Auto-screened 2026-03-09: Network infrastructure and optical infrastructure provider - not ITAD services. Website: https://itectra.com/']
        },
        'Minu': {
            'dataQuality': 'rejected',
            'notes': ['Auto-screened 2026-03-09: IT distributor for end-of-life products (sourcing/distribution) - no disposal services. Website: https://www.minu.dk/']
        },
        'Rebound Electronics': {
            'dataQuality': 'rejected',
            'notes': ['Auto-screened 2026-03-09: Electronic components distributor and supply chain services - not IT asset disposal. Website: https://reboundeu.com/']
        }
    }
    
    updated_count = 0
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    for lead in leads:
        if lead['name'] in updates:
            update_data = updates[lead['name']]
            
            # Apply updates
            lead['dataQuality'] = update_data['dataQuality']
            lead['lastVerified'] = timestamp
            lead['updatedAt'] = timestamp
                
            # Update notes
            if 'notes' not in lead:
                lead['notes'] = []
            lead['notes'].extend(update_data['notes'])
            
            updated_count += 1
            print(f"✅ Updated: {lead['name']} -> {update_data['dataQuality']}")
    
    # Save updated data
    with open('/tmp/pipeline-portal/src/data/leadpool.json', 'w') as f:
        json.dump(leads, f, indent=2)
    
    print(f"\n📊 Updated {updated_count} leads from batch 2")
    return updated_count

if __name__ == "__main__":
    update_leadpool_batch2()