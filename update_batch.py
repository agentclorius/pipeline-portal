#!/usr/bin/env python3
import json
from datetime import datetime

def update_leadpool():
    """Update specific leads based on manual screening"""
    
    # Load data
    with open('/tmp/pipeline-portal/src/data/leadpool.json', 'r') as f:
        leads = json.load(f)
    
    # Define updates based on screening
    updates = {
        'Inventus Group': {
            'dataQuality': 'verified',
            'stage': 'qualified',
            'score': 85,
            'notes': ['Auto-screened 2026-03-09: Clear ITAD focus - used IT equipment sales/disposal, data removal services. Website: https://inventusgroup.com/']
        },
        'Anrema Tech': {
            'dataQuality': 'rejected', 
            'notes': ['Auto-screened 2026-03-09: Domain hijacked with inappropriate content. No longer legitimate business.']
        },
        'Bloomtree Technologies': {
            'dataQuality': 'verified',
            'stage': 'qualified', 
            'score': 88,
            'notes': ['Auto-screened 2026-03-09: Global IT asset solutions specialist - technology resale/disposal, secure data erasure. Website: https://bloomtreegroup.com/']
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
            
            if 'stage' in update_data:
                lead['stage'] = update_data['stage']
            if 'score' in update_data:
                lead['score'] = update_data['score']
                
            # Update notes
            if 'notes' not in lead:
                lead['notes'] = []
            lead['notes'].extend(update_data['notes'])
            
            updated_count += 1
            print(f"✅ Updated: {lead['name']} -> {update_data['dataQuality']}")
    
    # Save updated data
    with open('/tmp/pipeline-portal/src/data/leadpool.json', 'w') as f:
        json.dump(leads, f, indent=2)
    
    print(f"\n📊 Updated {updated_count} leads")
    return updated_count

if __name__ == "__main__":
    update_leadpool()