import fs from 'fs';

// Read the leadpool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

const updates = [
  {
    id: 'org-699',
    dataQuality: 'rejected',
    notes: ['REJECTED: Basic IT reseller (PC247). No ITAD processing facilities, just laptop/PC buying/selling.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-700',
    dataQuality: 'rejected', 
    notes: ['REJECTED: No web presence found. Cannot verify ITAD operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-703',
    dataQuality: 'rejected',
    notes: ['REJECTED: Computer systems/software sales company (Basingstoke). Not ITAD processing.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-705',
    dataQuality: 'rejected',
    notes: ['REJECTED: Consumer electronics retailer (Narmi-tech Shopify store). Sells refurbished Apple products to consumers, not B2B ITAD.'],
    stage: 'rejected', 
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-709',
    dataQuality: 'rejected',
    notes: ['REJECTED: IBM hardware reseller/refurbisher (neu-comp). Limited to IBM equipment resale, not comprehensive ITAD services.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-711',
    dataQuality: 'rejected',
    notes: ['REJECTED: No verifiable web presence found for Newelltek Wellington Somerset. Cannot confirm ITAD operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-748',
    dataQuality: 'verified',
    notes: ['QUALIFIED: Resource Development UK - BSI-certified remanufacturer (BS Standards 8887-220/211). Est. 1994, WEEE accredited, 100% UK facility in Rochester. Serves education/business/public sector.'],
    stage: 'qualified',
    score: 75,
    isPipeline: true,
    services: ['Computer Remanufacturing', 'Refurbishment', 'BSI-Certified Process'],
    certifications: ['BSI BS 8887-220', 'BSI BS 8887-211', 'WEEE Exemption'],
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-752',
    dataQuality: 'rejected',
    notes: ['REJECTED: Recommerce IT - refurbished equipment retailer with consumer focus. No evidence of corporate ITAD services or data destruction facilities.'],
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
console.log('Updates complete');