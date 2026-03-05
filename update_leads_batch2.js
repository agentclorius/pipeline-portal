import fs from 'fs';

// Read the lead pool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

// Define rejections and qualifications for batch 2
const updates = [
  // QUALIFICATIONS
  {
    id: "org-611", // FLP Solutions
    action: "qualify",
    stage: "qualified",
    score: 75,
    isPipeline: true,
    dataQuality: "verified",
    notes: ["QUALIFIED: FLP Solutions - 24+ years IT recycling & disposal services, ISO 9001/14001/27001 certified"],
    services: ["IT Recycling", "IT Disposal", "Environmental Compliance"]
  },
  
  // REJECTIONS
  {
    id: "org-571", // CENTREX PRINT SERVICES
    action: "reject",
    reason: "Print services only, not ITAD",
    notes: ["REJECTED: CENTREX PRINT SERVICES - print services company, no website, not ITAD processing"]
  },
  {
    id: "org-593", // Deane Computer Solutions  
    action: "reject",
    reason: "Website down/non-functional",
    notes: ["REJECTED: Deane Computer Solutions - website non-functional/inaccessible"]
  },
  {
    id: "org-600", // Euro Options
    action: "reject", 
    reason: "IT hardware distributor, not ITAD",
    notes: ["REJECTED: Euro Options - IT hardware distributor to resellers, £12M inventory, not ITAD processing"]
  },
  {
    id: "org-612", // Fox in the Box
    action: "reject",
    reason: "Refurbished equipment reseller, not ITAD", 
    notes: ["REJECTED: Fox in the Box - refurbished workstation/server reseller to end users, not ITAD processing"]
  },
  {
    id: "org-578", // Circle Mobile
    action: "reject",
    reason: "Mobile device broker, not ITAD",
    notes: ["REJECTED: Circle Mobile - mobile device broker/trading, not ITAD processing"]
  }
];

let updated = 0;

// Update leads
for (let lead of leadpool) {
  const update = updates.find(u => u.id === lead.id);
  if (update) {
    if (update.action === "qualify") {
      lead.stage = update.stage;
      lead.score = update.score;
      lead.isPipeline = update.isPipeline;
      lead.dataQuality = update.dataQuality;
      lead.notes = update.notes;
      lead.services = update.services || [];
    } else if (update.action === "reject") {
      lead.stage = "rejected";
      lead.dataQuality = "rejected";
      lead.isPipeline = false;
      lead.notes = update.notes;
      lead.rejectReason = update.reason;
    }
    
    lead.lastVerified = new Date().toISOString();
    lead.updatedAt = new Date().toISOString();
    updated++;
    console.log(`Updated ${lead.id}: ${lead.name} - ${update.action} - ${update.reason || 'qualified'}`);
  }
}

// Write back
fs.writeFileSync('src/data/leadpool.json', JSON.stringify(leadpool, null, 2));
console.log(`\nSuccessfully updated ${updated} leads (1 qualified, ${updated-1} rejected)`);