import json
from datetime import datetime

# Load the leadpool data
with open('src/data/leadpool.json', 'r') as f:
    leads = json.load(f)

# Current timestamp
now = datetime.now().isoformat() + "Z"

# Define updates based on screening
updates = {
    # GENUINE ITAD - promote to pipeline
    "org-564": {  # Bulk GSM
        "dataQuality": "verified",
        "stage": "qualified", 
        "score": 85,
        "isPipeline": True,
        "notes": ["GENUINE ITAD: Own facilities, proprietary data destruction software, 20+ years experience, NIST 800-88/DoD 5220.22M certified, Environment Agency registered. Multiple facilities, 20,000+ buyer network."],
        "services": ["ITAD", "Data Destruction", "Asset Recovery", "Secure Transportation", "Compliance Reporting"],
        "certifications": ["NIST 800-88", "DoD 5220.22M", "Environment Agency Registration"],
        "lastVerified": now
    },
    
    # NON-ITADS - reject
    "org-542": {  # Apogee Corporation  
        "dataQuality": "rejected",
        "stage": "rejected",
        "rejectReason": "IT Services Provider with basic buy-back program, not genuine ITAD with processing facilities",
        "lastVerified": now
    },
    "org-543": {  # Approved Technology
        "dataQuality": "rejected", 
        "stage": "rejected",
        "rejectReason": "Optical network connectivity distributor, not ITAD",
        "lastVerified": now
    },
    "org-548": {  # Alvi Traders UK
        "dataQuality": "rejected",
        "stage": "rejected", 
        "rejectReason": "Wholesale trader/exporter, no ITAD processing facilities",
        "lastVerified": now
    },
    "org-572": {  # Centrex Computing Services
        "dataQuality": "rejected",
        "stage": "rejected",
        "rejectReason": "IT maintenance/support provider, not ITAD",
        "lastVerified": now
    },
    "org-603": {  # Excotek
        "dataQuality": "rejected",
        "stage": "rejected",
        "rejectReason": "IT solutions/procurement provider, not ITAD",
        "lastVerified": now
    },
    "org-567": {  # Buyer Area
        "dataQuality": "rejected",
        "stage": "rejected",
        "rejectReason": "Retail refurbished laptop reseller, not genuine ITAD",
        "lastVerified": now
    },
    
    # DEAD WEBSITES - reject
    "org-547": {  # ALM Trading
        "dataQuality": "rejected",
        "stage": "rejected", 
        "rejectReason": "Website down/non-functional",
        "lastVerified": now
    },
    "org-566": {  # IT Reuse Buy Back IT
        "dataQuality": "rejected",
        "stage": "rejected",
        "rejectReason": "Website returns 404 error", 
        "lastVerified": now
    },
    "org-575": {  # Channel-C
        "dataQuality": "rejected",
        "stage": "rejected",
        "rejectReason": "Website down/non-functional",
        "lastVerified": now
    },
    "org-604": {  # Exporttech Distribution
        "dataQuality": "rejected", 
        "stage": "rejected",
        "rejectReason": "Website down/non-functional",
        "lastVerified": now
    },
    "org-563": {  # BNM Services
        "dataQuality": "rejected",
        "stage": "rejected",
        "rejectReason": "Website down/non-functional",
        "lastVerified": now
    },
    
    # POTENTIAL ITADS - needs further review
    "org-588": {  # Comtek Network Systems
        "dataQuality": "needs_review",
        "notes": ["Telecoms equipment repair/refurb specialist with multiple facilities. Does asset recovery and recycling but focused on network equipment rather than traditional ITAD. Needs further assessment for ITAD classification."],
        "lastVerified": now
    },
    "org-594": {  # Discovery Computer Services
        "dataQuality": "needs_review", 
        "notes": ["Operating since 1992, mentions IT recycling and buying equipment. Basic website doesn't clearly show ITAD facilities or certifications. Needs further verification."],
        "lastVerified": now
    },
    "org-546": {  # Air Space Technology
        "dataQuality": "needs_review",
        "notes": ["Apple product refurbishment and resale. Basic website doesn't clearly indicate proper ITAD facilities or data destruction capabilities. Needs further verification."],
        "lastVerified": now
    }
}

# Apply updates
for i, lead in enumerate(leads):
    if lead["id"] in updates:
        update_data = updates[lead["id"]]
        for key, value in update_data.items():
            leads[i][key] = value
        leads[i]["updatedAt"] = now

# Save updated data
with open('src/data/leadpool.json', 'w') as f:
    json.dump(leads, f, indent=2)

print(f"Updated {len(updates)} leads")
print("Breakdown:")
print("- 1 promoted to verified/pipeline (Bulk GSM)")
print("- 6 rejected (non-ITAD)")
print("- 5 rejected (dead websites)")  
print("- 3 marked for further review")
