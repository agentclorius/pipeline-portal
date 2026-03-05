import fs from 'fs';

// Read the lead pool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

// Define batch 4 updates - focusing on completing 50 leads total
const updates = [
  // HIGH-QUALITY QUALIFICATIONS
  {
    id: "org-642", // Innovent Recycling
    action: "qualify",
    stage: "qualified", 
    score: 90,
    isPipeline: true,
    dataQuality: "verified",
    notes: ["QUALIFIED: Innovent Recycling - Top tier ITAD: ISO 27001, HMG IS5, 0% landfill, 10,000+ UK businesses, WEEE compliant"],
    services: ["IT Recycling", "Secure Data Destruction", "Asset Reporting", "Zero Landfill Policy"]
  },
  {
    id: "org-640", // Ingram Micro Lifecycle
    action: "qualify",
    stage: "qualified",
    score: 85,
    isPipeline: true, 
    dataQuality: "verified",
    notes: ["QUALIFIED: Ingram Micro Lifecycle - Major global ITAD provider, circular economy focus, enterprise-scale operations"],
    services: ["Circular Economy Solutions", "IT Asset Disposition", "Technology Lifecycle Management"]
  },
  
  // REJECTIONS - Brokers and wrong business models
  {
    id: "org-583", // Com Cubed
    action: "reject",
    reason: "IT support services, not ITAD",
    notes: ["REJECTED: Com Cubed - IT support company, not ITAD processing"]
  },
  {
    id: "org-589", // CONTINENTEL
    action: "reject", 
    reason: "IT services company, not ITAD",
    notes: ["REJECTED: CONTINENTEL - IT services company, not ITAD processing"]
  },
  {
    id: "org-592", // Datek Solutions
    action: "reject",
    reason: "IT broker, not ITAD processor",
    notes: ["REJECTED: Datek Solutions - IT broker/trader, not ITAD processing"]
  },
  {
    id: "org-596", // EBM Office Centre
    action: "reject",
    reason: "Office equipment provider, not ITAD",
    notes: ["REJECTED: EBM Office Centre - office equipment provider, not ITAD processing"]
  },
  {
    id: "org-597", // Ecom Management (UK)
    action: "reject",
    reason: "E-commerce management, not ITAD",
    notes: ["REJECTED: Ecom Management UK - e-commerce management services, not ITAD processing"]
  },
  {
    id: "org-602", // Everything IT
    action: "reject",
    reason: "IT services provider, not ITAD",
    notes: ["REJECTED: Everything IT - general IT services, not ITAD processing"]
  },
  {
    id: "org-605", // Fala
    action: "reject",
    reason: "IT services company, not ITAD",
    notes: ["REJECTED: Fala - IT services company, not ITAD processing"]
  },
  {
    id: "org-607", // First Click Solutions
    action: "reject",
    reason: "IT support services, not ITAD", 
    notes: ["REJECTED: First Click Solutions - IT support services, not ITAD processing"]
  },
  {
    id: "org-608", // Fixio
    action: "reject",
    reason: "Computer repair services, not ITAD",
    notes: ["REJECTED: Fixio - computer/device repair services, not ITAD processing"]
  },
  {
    id: "org-620", // Ghekko
    action: "reject", 
    reason: "IT services provider, not ITAD",
    notes: ["REJECTED: Ghekko - IT services provider, not ITAD processing"]
  },
  {
    id: "org-626", // GoSpec
    action: "reject",
    reason: "IT broker, not ITAD processor",
    notes: ["REJECTED: GoSpec - IT broker, not ITAD processing"]
  },
  {
    id: "org-627", // GraphicSolutions
    action: "reject",
    reason: "Graphics/printing solutions, not ITAD",
    notes: ["REJECTED: GraphicSolutions - graphics/printing solutions, not IT disposal"]
  },
  {
    id: "org-632", // Hamilton Rentals
    action: "reject",
    reason: "Technology rental company, not ITAD",
    notes: ["REJECTED: Hamilton Rentals - technology rental/leasing, not ITAD processing"]
  },
  {
    id: "org-637", // iNet Group
    action: "reject",
    reason: "IT services provider, not ITAD",
    notes: ["REJECTED: iNet Group - IT services provider, not ITAD processing"]
  },
  {
    id: "org-647", // Inturn Industries
    action: "reject",
    reason: "IT broker/auction house, not ITAD",
    notes: ["REJECTED: Inturn Industries - IT broker/auction house, not ITAD processing"]
  },
  {
    id: "org-650", // Iris Conex
    action: "reject",
    reason: "IT broker, not ITAD processor", 
    notes: ["REJECTED: Iris Conex - IT broker, not ITAD processing"]
  },

  // Unverifiable (no websites)
  {
    id: "org-639", // INFORSIGHT
    action: "reject",
    reason: "No website, unverifiable",
    notes: ["REJECTED: INFORSIGHT - no website, unverifiable business model"]
  },
  {
    id: "org-644", // Intelligent Pixel Technology  
    action: "reject",
    reason: "No website, unverifiable",
    notes: ["REJECTED: Intelligent Pixel Technology - no website, unverifiable business model"]
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
console.log(`\nSuccessfully updated ${updated} leads (2 qualified, ${updated-2} rejected)`);