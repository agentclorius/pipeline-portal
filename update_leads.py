#!/usr/bin/env python3

import json
from datetime import datetime

def update_leadpool():
    # Load current data
    with open('src/data/leadpool.json', 'r') as f:
        data = json.load(f)
    
    # Define updates
    updates = {
        "org-554": {  # AYOO SERVICES
            "dataQuality": "verified",
            "stage": "qualified", 
            "score": 74,
            "isPipeline": True,
            "notes": ["AYOO Services - Remanufacturing laptops with own facility. ITAD services: secure data erasure (NIST/DoD/GDPR), asset tracking, certified destruction, chain of custody."],
            "services": ["ITAD", "Data Erasure", "Remanufacturing", "IT Recycling"],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-588": {  # Comtek Network Systems
            "dataQuality": "verified",
            "stage": "qualified",
            "score": 70, 
            "isPipeline": True,
            "notes": ["Comtek Network Systems - Telecom/network equipment repair, refurb, and recycling. Component-level repairs, circular economy focus. Multi-vendor support."],
            "services": ["Network Equipment Repair", "Refurbishment", "Component Recovery", "Recycling"],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-546": {  # Air space technology
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Apple device reseller/refurbisher only. Not ITAD processor with own facilities."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-549": {  # APPLEBITE2NDBITE
            "dataQuality": "rejected",
            "stage": "rejected", 
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Apple device retailer only. No ITAD processing facilities."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-594": {  # DISCOVERY COMPUTER SERVICES
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False, 
            "notes": ["REJECTED: IT equipment buyback service only. No ITAD processing or data destruction facilities."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-638": {  # INFOCUS ID
            "dataQuality": "rejected", 
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: ID card printer supplier only. Not ITAD."],
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
    
    print("Leadpool updated successfully")

if __name__ == "__main__":
    update_leadpool()