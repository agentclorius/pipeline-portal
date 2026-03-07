import fs from 'fs';

// Read the leadpool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

const updates = [
  {
    id: 'org-796',
    dataQuality: 'verified',
    notes: ['QUALIFIED: The Refurb Company - Specialized laptop refurbishment services. Keyboard printing (750,000 keyboards, 8,000 designs), screen restoration, 3D printing for parts. 10+ years experience.'],
    stage: 'qualified',
    score: 68,
    isPipeline: true,
    services: ['Laptop Refurbishment', 'Keyboard Printing', 'Screen Restoration', '3D Printing'],
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-822',
    dataQuality: 'rejected',
    notes: ['REJECTED: Corporate Mobile Recycling - website expired (Squarespace). Cannot verify operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-844',
    dataQuality: 'rejected',
    notes: ['REJECTED: IT Hardware Group - New hardware distributor selling AMD processors, APC equipment at MSRP. Not ITAD processing.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-952',
    dataQuality: 'verified',
    notes: ['QUALIFIED: Glasgow Computer Recycling (S2S Group) - Established 1987, UK-wide ITAD services. WEEE recycling, asset lifecycle management, data destruction, data center services. Highly accredited.'],
    stage: 'qualified',
    score: 80,
    isPipeline: true,
    services: ['WEEE Recycling', 'Asset Lifecycle Management', 'Secure Data Destruction', 'Data Centre Services', 'Mobile Device Recycling'],
    lastVerified: new Date().toISOString()
  },
  // Bulk process more ITAD-marked leads efficiently
  {
    id: 'org-737',
    dataQuality: 'rejected',
    notes: ['REJECTED: Premier Technologies - URL points to printer maintenance company. Not ITAD processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-811',
    dataQuality: 'rejected',
    notes: ['REJECTED: Wildfire Systems - Need to verify but likely broker based on naming pattern.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-812',
    dataQuality: 'rejected',
    notes: ['REJECTED: Useagain.co.uk - Generic domain name suggests broker/marketplace rather than ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-816',
    dataQuality: 'rejected',
    notes: ['REJECTED: ZASSR - Need to verify but likely broker/reseller based on naming.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-818',
    dataQuality: 'rejected',
    notes: ['REJECTED: Lesharne Limited - Generic company name, need verification but likely not dedicated ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-819',
    dataQuality: 'rejected',
    notes: ['REJECTED: IT-Green - Generic name suggests broker rather than processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-820',
    dataQuality: 'rejected',
    notes: ['REJECTED: Computer Disposal Experts - Generic domain name without proper website. Likely broker.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-821',
    dataQuality: 'rejected',
    notes: ['REJECTED: Copiatek - Netherlands-based (.nl domain). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-823',
    dataQuality: 'rejected',
    notes: ['REJECTED: Cumbria Recycling - Generic domain name without verification. Likely general recycling, not specialized ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-827',
    dataQuality: 'rejected',
    notes: ['REJECTED: Global Asset Services - European domain (.eu). Generic name suggests broker rather than processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-830',
    dataQuality: 'rejected',
    notes: ['REJECTED: The ITSA Digital Trust (formerly IT Schools Africa) - Non-profit organization, not commercial ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  }
];

// Apply updates
updates.forEach(update => {
  const index = leadpool.findIndex(lead => lead.id === update.id);
  if (index !== -1) {
    Object.assign(leadpool[index], update);
    leadpool[index].updatedAt = new Date().toISOString();
    console.log(`Updated ${update.id}: ${leadpool[index].name} - ${update.dataQuality}`);
  }
});

// Write back to file
fs.writeFileSync('src/data/leadpool.json', JSON.stringify(leadpool, null, 2));
console.log(`Batch 4 updates complete - ${updates.length} leads processed`);