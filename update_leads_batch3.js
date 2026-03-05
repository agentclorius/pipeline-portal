import fs from 'fs';

// Read the lead pool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

// Define batch 3 updates
const updates = [
  // QUALIFICATIONS
  {
    id: "org-622", // Global Computer Specialists
    action: "qualify",
    stage: "qualified",
    score: 80,
    isPipeline: true,
    dataQuality: "verified",
    notes: ["QUALIFIED: GCS Recycling - Circular IT Solutions, transforms redundant IT equipment, global redistribution network"],
    services: ["Circular IT Solutions", "IT Asset Processing", "Global Redistribution"]
  },
  {
    id: "org-630", // Greenfuture IT Solutions
    action: "qualify",
    stage: "qualified",
    score: 85,
    isPipeline: true,
    dataQuality: "verified",
    notes: ["QUALIFIED: GreenFuture IT - 20+ years experience, IT disposal with secure data destruction, buyback services, circular economy focus"],
    services: ["IT Disposal", "Secure Data Destruction", "Asset Buyback", "IT Remarketing"]
  },
  {
    id: "org-628", // Green Eagle Limited
    action: "qualify",
    stage: "qualified",
    score: 75,
    isPipeline: true,
    dataQuality: "verified",
    notes: ["QUALIFIED: Green Eagle - electrical waste management, repair & reuse focus, social enterprise, environmental responsibility"],
    services: ["Electrical Waste Management", "Repair & Reuse", "Environmental Disposal"]
  },
  
  // REJECTIONS
  {
    id: "org-636", // Imagine Technology
    action: "reject",
    reason: "IT hardware reseller/broker, not ITAD",
    notes: ["REJECTED: Imagine Technology - refurbished IT hardware supplier/broker, no disposal services"]
  },
  {
    id: "org-581", // Circle Stock
    action: "reject",
    reason: "IT hardware distributor, not ITAD", 
    notes: ["REJECTED: Circle Stock - IT hardware distribution business, not ITAD processing"]
  },
  {
    id: "org-584", // COMEA Computer
    action: "reject",
    reason: "Computer broker/trading, not ITAD",
    notes: ["REJECTED: COMEA Computer - computer broker/trading company, not ITAD processing"]
  },
  {
    id: "org-585", // Complete Care Consultancy
    action: "reject",
    reason: "Consultancy business, not ITAD", 
    notes: ["REJECTED: Complete Care Consultancy - business consultancy, not ITAD processing"]
  },
  {
    id: "org-587", // Computer factory uk
    action: "reject",
    reason: "Computer retailer/broker, not ITAD",
    notes: ["REJECTED: Computer Factory UK - computer retail/broker, not ITAD processing"]
  },
  {
    id: "org-598", // eJobber
    action: "reject",
    reason: "IT broker/trading platform, not ITAD",
    notes: ["REJECTED: eJobber - IT broker/trading platform, not ITAD processing"]
  },
  {
    id: "org-618", // Gaia Packaging Solutions  
    action: "reject",
    reason: "Packaging solutions, not ITAD",
    notes: ["REJECTED: Gaia Packaging Solutions - packaging/product development, not IT disposal"]
  },
  {
    id: "org-631", // GTechIT
    action: "reject", 
    reason: "IT broker, not ITAD",
    notes: ["REJECTED: GTechIT - IT broker, not ITAD processing"]
  },
  {
    id: "org-634", // HGK Solutions
    action: "reject",
    reason: "IT broker, not ITAD", 
    notes: ["REJECTED: HGK Solutions - IT broker, not ITAD processing"]
  },
  {
    id: "org-614", // Gadget Centre (UK)
    action: "reject",
    reason: "No website, unverifiable",
    notes: ["REJECTED: Gadget Centre UK - no website, unverifiable business model"]
  },
  {
    id: "org-623", // Global Computers
    action: "reject",
    reason: "No website, unverifiable", 
    notes: ["REJECTED: Global Computers - no website, unverifiable business model"]
  },
  {
    id: "org-629", // Green it recycling uk
    action: "reject",
    reason: "No website, unverifiable",
    notes: ["REJECTED: Green IT Recycling UK - no website, unverifiable business model"]
  },
  {
    id: "org-633", // Hazell Computers  
    action: "reject",
    reason: "No website, unverifiable",
    notes: ["REJECTED: Hazell Computers - no website, unverifiable business model"]
  },
  {
    id: "org-635", // Hewlett Packard Enterprise
    action: "reject",
    reason: "OEM manufacturer, not ITAD processor",
    notes: ["REJECTED: Hewlett Packard Enterprise - OEM manufacturer, not third-party ITAD processor"]
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
console.log(`\nSuccessfully updated ${updated} leads (3 qualified, ${updated-3} rejected)`);