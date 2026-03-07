import fs from 'fs';

// Read the leadpool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

const updates = [
  {
    id: 'org-712',
    dataQuality: 'rejected',
    notes: ['REJECTED: NH Trading (NW) - computer export/wholesale business. Purchases and supplies ICT hardware globally but no evidence of ITAD processing facilities.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-719',
    dataQuality: 'rejected',
    notes: ['REJECTED: OCC Components - website not found (DNS error). Cannot verify ITAD operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-764',
    dataQuality: 'verified',
    notes: ['QUALIFIED: SecondLife - Complete ITAD services including asset valuation, lifecycle management, certified data wiping, IT recycling. Serves schools and businesses. London-based.'],
    stage: 'qualified',
    score: 73,
    isPipeline: true,
    services: ['IT Asset Valuation', 'Lifecycle Management', 'Data Wiping (Certified)', 'IT Recycling', 'Secure Disposal'],
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-765',
    dataQuality: 'rejected',
    notes: ['REJECTED: Secure Disk Technologies - website under construction. Cannot verify operations.'],
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
console.log('Batch 2 updates complete');