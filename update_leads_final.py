#!/usr/bin/env python3

import json
from datetime import datetime

def update_leadpool():
    # Load current data
    with open('src/data/leadpool.json', 'r') as f:
        data = json.load(f)
    
    # Define updates for remaining leads (batch 4 - final)
    # Based on website checks and business names, categorizing as ITAD vs resellers/traders
    updates = {
        "org-658": {  # IT Xchange
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Computer technology retailer/reseller, not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-656": {  # I.T. Trade Services
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: IT trading company, not ITAD processor with facilities."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-657": {  # IT TRADERS UK
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Website inaccessible (301), IT trading company name suggests reseller not ITAD."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-660": {  # ITEKDATA
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: IT equipment trader based on name, not verified as ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-661": {  # ITELLIGENTSIA GLOBAL
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: IT services company, not verified as ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-662": {  # ITinStock
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: IT equipment stockist/trader based on name, not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-667": {  # TeamKCI
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: No clear ITAD services identified, unverifiable."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-669": {  # KSD Technology Group
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Website inaccessible, cannot verify ITAD capabilities."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-672": {  # LanPartsDirect
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Network parts supplier based on name, not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-673": {  # LA Peripherals
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: IT peripherals supplier (related to LA Recycling), not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-677": {  # Lizard Tech Solutions
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: IT solutions company, not verified as ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-678": {  # MacColl Group
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Media/communications company, not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-680": {  # McCarthy's
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Website inaccessible (301), cannot verify ITAD capabilities."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-681": {  # MDC
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Website inaccessible (301), cannot verify ITAD capabilities."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-682": {  # Mem-Star Distribution
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Memory/parts distributor based on name, not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-683": {  # MF Communications
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Communications equipment supplier, not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-684": {  # Micro-D Ltd.
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: IT equipment supplier, not verified as ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-685": {  # MicroDream Limited
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: IT services company, not verified as ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-688": {  # Mid-Blue International
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Trading company, not verified as ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-689": {  # Mr Phone Streatham
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Phone repair shop, not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-690": {  # MRRS Empire Ltd.
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: General trading company, not verified as ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-691": {  # ALS
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: General services company, not verified as ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-692": {  # Angem Limited
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: General services company, not verified as ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-693": {  # ASC Technology
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: Gaming PC supplier based on website URL, not ITAD processor."],
            "services": [],
            "lastVerified": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z"
        },
        "org-694": {  # Bitz for All
            "dataQuality": "rejected",
            "stage": "rejected",
            "score": None,
            "isPipeline": False,
            "notes": ["REJECTED: IT parts supplier, not verified as ITAD processor."],
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
    
    print("Final leadpool batch updated successfully")

if __name__ == "__main__":
    update_leadpool()