#!/usr/bin/env python3

import json
from datetime import datetime

def update_leadpool():
    # Load current data
    with open('src/data/leadpool.json', 'r') as f:
        data = json.load(f)
    
    # Define updates for batch 3
    updates = {
        "org-674": {  # LA Recycling
            "dataQuality": "verified",
            "stage": "qualified", 
            "score": 78,
            "isPipeline": True,
            "notes": ["LA Recycling - Comprehensive ITAD services: IT asset disposal, certified data erasure (100% irrecoverable), asset tracking, data destruction certificates, material recycling."],
            "services": ["ITAD", "Data Destruction", "Asset Tracking", "Recycling", "Certified Data Erasure"],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-670": {  # Kudos Remarketing
            "dataQuality": "verified",
            "stage": "qualified", 
            "score": 76,
            "isPipeline": True,
            "notes": ["Kudos Remarketing - IT asset recovery, recycling, certified data destruction. WEEE compliant, onsite disk shredding, value recovery focus."],
            "services": ["ITAD", "IT Asset Recovery", "Certified Data Destruction", "WEEE Recycling", "Disk Shredding"],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-668": {  # KEW COMPUTERS
            "dataQuality": "verified",
            "stage": "qualified", 
            "score": 65,
            "isPipeline": True,
            "notes": ["KEW COMPUTERS - Computer recycling and disposal services. Understands legal structures for IT equipment disposal."],
            "services": ["Computer Recycling", "IT Disposal"],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-664": {  # Jarvis Tech
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: IT wholesaler/reseller only, not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-679": {  # Make Change International
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: No verifiable online presence or ITAD services found."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-675": {  # Level3Computer
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: No website provided, unverifiable."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-676": {  # LikedItems UK Ltd.
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: No website provided, unverifiable."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-659": {  # ITCSALES.CO.UK
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: No website provided, unverifiable."],
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
    
    print("Leadpool batch 3 updated successfully")

if __name__ == "__main__":
    update_leadpool()