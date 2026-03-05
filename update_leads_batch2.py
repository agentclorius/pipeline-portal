#!/usr/bin/env python3

import json
from datetime import datetime

def update_leadpool():
    # Load current data
    with open('src/data/leadpool.json', 'r') as f:
        data = json.load(f)
    
    # Define updates for batch 2
    updates = {
        "org-641": {  # Inkhouse
            "dataQuality": "verified",
            "stage": "qualified", 
            "score": 68,
            "isPipeline": True,
            "notes": ["Inkhouse - 20+ years, refurbished IT hardware provision. End of life IT services include data sanitization and asset remarketing. Mixed IT services provider."],
            "services": ["IT Hardware", "Data Sanitization", "End of Life IT"],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-645": {  # Interforce
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Security guard company, not ITAD."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-649": {  # Inventory Source Limited
            "dataQuality": "rejected",
            "stage": "rejected", 
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Equipment reseller with basic data wiping. No comprehensive ITAD facilities."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-652": {  # IT CONNECTS LONDON
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False, 
            "notes": ["REJECTED: Website under construction, cannot verify ITAD capabilities."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-653": {  # IT Links
            "dataQuality": "rejected", 
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Dead website (404), unverifiable."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-654": {  # IT Parts and Spares
            "dataQuality": "rejected", 
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Website inaccessible, cannot verify ITAD capabilities."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-663": {  # ITRegeneration
            "dataQuality": "rejected", 
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Electronics surplus/used parts reseller, not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        }
    }
    
    # Apply updates
    for item in data:
        if item["id"] in updates:
            update_data = updates[item["id"]]
            for key, value in update_data.items():
                item[key] = value
            print(f"Updated {item['id']}: {item['name']} -> {item['dataQuality']}")
    
    # Save updated data
    with open('src/data/leadpool.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Leadpool batch 2 updated successfully")

if __name__ == "__main__":
    update_leadpool()