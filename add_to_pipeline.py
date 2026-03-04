import json
from datetime import datetime

# Load pipeline and leadpool data
with open('src/data/pipeline.json', 'r') as f:
    pipeline = json.load(f)

with open('src/data/leadpool.json', 'r') as f:
    leadpool = json.load(f)

# Find Bulk GSM in leadpool
bulk_gsm = None
for lead in leadpool:
    if lead["id"] == "org-564":
        bulk_gsm = lead
        break

if bulk_gsm:
    # Add to pipeline if not already there
    pipeline_ids = [org["id"] for org in pipeline]
    if bulk_gsm["id"] not in pipeline_ids:
        pipeline.append(bulk_gsm)
        
        # Save updated pipeline
        with open('src/data/pipeline.json', 'w') as f:
            json.dump(pipeline, f, indent=2)
        
        print(f"Added {bulk_gsm['name']} to pipeline.json")
    else:
        print(f"{bulk_gsm['name']} already in pipeline")
else:
    print("Bulk GSM not found in leadpool")

print(f"Pipeline now has {len(pipeline)} organizations")
