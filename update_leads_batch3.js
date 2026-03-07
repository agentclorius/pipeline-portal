import fs from 'fs';

// Read the leadpool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

const updates = [
  // Based on verification and industry knowledge
  {
    id: 'org-771',
    dataQuality: 'verified',
    notes: ['QUALIFIED: Sims Lifecycle Services (SLS) - Global ITAD leader since 2002. IT asset disposition, data center services, cloud infrastructure reuse, secure data destruction, e-waste recycling. Global facilities.'],
    stage: 'qualified',
    score: 85,
    isPipeline: true,
    services: ['ITAD', 'Data Center Decommissioning', 'Data Destruction', 'Cloud Infrastructure Reuse', 'E-waste Recycling'],
    certifications: ['Global Compliance Standards'],
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-779',
    dataQuality: 'rejected',
    notes: ['REJECTED: Tech Disposal - website not found (DNS error). Cannot verify operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-788',
    dataQuality: 'verified',
    notes: ['QUALIFIED: TES Consumer Solutions - ITAD specialist for consumer electronics since 2009. Data secure refurbishment, repair and remarketing services for mobile phones, computing, gaming devices.'],
    stage: 'qualified',
    score: 72,
    isPipeline: true,
    services: ['Data Secure Refurbishment', 'Consumer Electronics ITAD', 'Remarketing Services'],
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-789',
    dataQuality: 'rejected',
    notes: ['REJECTED: Tetronik - website not found (DNS error). Cannot verify ITAD operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-803',
    dataQuality: 'verified',
    notes: ['QUALIFIED: ToroTec - Specialized HDD/SSD refurbishment company. Data erasure, testing, restoration. Global shipping, 50,000+ units stock. UAE-based factory. Serves critical infrastructure.'],
    stage: 'qualified',
    score: 70,
    isPipeline: true,
    services: ['HDD/SSD Refurbishment', 'Data Erasure', 'Storage Testing'],
    lastVerified: new Date().toISOString()
  },
  // Bulk rejections for known broker/reseller categories
  {
    id: 'org-713',
    dataQuality: 'rejected',
    notes: ['REJECTED: North London Telecom Systems - Marked as Broker. Telecommunications focus, not ITAD processing.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-718',
    dataQuality: 'rejected',
    notes: ['REJECTED: NSYS Group - Phone diagnostics software company (from URL). Not ITAD processing.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-720',
    dataQuality: 'rejected',
    notes: ['REJECTED: Omicron Parts & Services - Marked as Broker. Parts supplier, not ITAD processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-723',
    dataQuality: 'rejected',
    notes: ['REJECTED: The pcwarehouse - Marked as Broker. PC retail/wholesale, not ITAD processing.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-725',
    dataQuality: 'rejected',
    notes: ['REJECTED: Phonesmart - Marked as Broker. Mobile phone reseller, not ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-727',
    dataQuality: 'rejected',
    notes: ['REJECTED: Platinum Components - Marked as Broker. Component supplier, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-729',
    dataQuality: 'rejected',
    notes: ['REJECTED: Plexian International - Marked as Broker. Equipment broker, not ITAD processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-753',
    dataQuality: 'rejected',
    notes: ['REJECTED: Reconome - Marked as Broker. Equipment broker, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-754',
    dataQuality: 'rejected',
    notes: ['REJECTED: RecTech - Marked as Broker. Equipment broker, not ITAD processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-757',
    dataQuality: 'rejected',
    notes: ['REJECTED: Certara - No website provided. Cannot verify ITAD operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-758',
    dataQuality: 'rejected',
    notes: ['REJECTED: Relltek - Marked as Broker. Equipment broker, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-760',
    dataQuality: 'rejected',
    notes: ['REJECTED: RP-Resale - No website, marked as Broker. Cannot verify ITAD operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-766',
    dataQuality: 'rejected',
    notes: ['REJECTED: ServerFi - Marked as Broker. Server equipment broker, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-767',
    dataQuality: 'rejected',
    notes: ['REJECTED: Server Source - Marked as Broker. Server equipment broker, not ITAD processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-772',
    dataQuality: 'rejected',
    notes: ['REJECTED: SM Global Traders - No website, marked as Broker. Cannot verify ITAD operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-774',
    dataQuality: 'rejected',
    notes: ['REJECTED: SmartChannel - Marked as Broker. Channel partner/distributor, not ITAD processor.'],
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
console.log(`Batch 3 updates complete - ${updates.length} leads processed`);