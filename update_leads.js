import fs from 'fs';

// Read the lead pool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

// Define rejections for this session
const rejections = [
  {
    id: "org-569", 
    reason: "Printer repair/refurbishment only, not ITAD",
    notes: ["REJECTED: CDS Printer Solutions - printer repair and refurbishment company, not ITAD processing"]
  },
  {
    id: "org-570",
    reason: "Consumer electronics retailer, not ITAD", 
    notes: ["REJECTED: Celebrium Technologies - gaming PC and electronics e-commerce store, not ITAD"]
  },
  {
    id: "org-595",
    reason: "Website down/non-functional",
    notes: ["REJECTED: Dragon Computer Remarketing - website domain for sale, business inactive"]
  },
  {
    id: "org-610", 
    reason: "Website down/non-functional",
    notes: ["REJECTED: Flogit2us.com - website non-functional/inaccessible"]
  },
  {
    id: "org-615",
    reason: "Website down/non-functional", 
    notes: ["REJECTED: Gentronics Solutions - website misconfigured/non-functional"]
  },
  {
    id: "org-619",
    reason: "Technology distributor, not ITAD",
    notes: ["REJECTED: Genuine Solutions - smart technology distributor, no ITAD processing"]
  },
  {
    id: "org-590",
    reason: "Consumer electronics reseller, not ITAD",
    notes: ["REJECTED: Crown Workspace (ITresale) - refurbished electronics B2C reseller, not ITAD"]
  }
];

let updated = 0;

// Update leads
for (let lead of leadpool) {
  const rejection = rejections.find(r => r.id === lead.id);
  if (rejection) {
    lead.stage = "rejected";
    lead.dataQuality = "rejected"; 
    lead.isPipeline = false;
    lead.notes = rejection.notes;
    lead.rejectReason = rejection.reason;
    lead.lastVerified = new Date().toISOString();
    lead.updatedAt = new Date().toISOString();
    updated++;
    console.log(`Updated ${lead.id}: ${lead.name} - ${rejection.reason}`);
  }
}

// Write back
fs.writeFileSync('src/data/leadpool.json', JSON.stringify(leadpool, null, 2));
console.log(`\nSuccessfully updated ${updated} leads with rejections`);