import fs from 'fs';

// Read the leadpool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

const updates = [
  // Qualified ITAD companies
  {
    id: 'org-954',
    dataQuality: 'verified',
    notes: ['QUALIFIED: Ready Set Recycle - Specialist in electronic lost property processing. GDPR/NIST compliant data erasure, 79% reduction in destruction vs traditional methods. ISO 14001, WEEE certified.'],
    stage: 'qualified',
    score: 75,
    isPipeline: true,
    services: ['Electronic Lost Property Processing', 'GDPR/NIST Data Erasure', 'Reuse & Recycling'],
    certifications: ['ISO 14001', 'WEEE Certified'],
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-967',
    dataQuality: 'verified',
    notes: ['QUALIFIED: Secure IT Recycle (ITRsecure) - Professional ITAD & data security. UK-wide coverage, ISO 9001/27001/14001 accredited, ICO registered, GDPR/WEEE compliant.'],
    stage: 'qualified',
    score: 78,
    isPipeline: true,
    services: ['IT Asset Disposal', 'Certified Data Sanitisation', 'Secure Collection'],
    certifications: ['ISO 9001', 'ISO 27001', 'ISO 14001', 'ICO Registered'],
    lastVerified: new Date().toISOString()
  },
  // Bulk process brokers (rejected)
  {
    id: 'org-739',
    dataQuality: 'rejected',
    notes: ['REJECTED: Printer Maintenance - Printer service company, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-769',
    dataQuality: 'rejected',
    notes: ['REJECTED: SHB Solutions Ltd - Marked as Broker. Equipment broker, not ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-770',
    dataQuality: 'rejected',
    notes: ['REJECTED: Silent Computing - Marked as Broker. PC specialist, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-775',
    dataQuality: 'rejected',
    notes: ['REJECTED: SNStockSolutions - Marked as Broker. Stock/inventory broker, not ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-908',
    dataQuality: 'rejected',
    notes: ['REJECTED: CES Telecom - Telecom equipment broker, not ITAD processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-912',
    dataQuality: 'rejected',
    notes: ['REJECTED: IT Product Supply - Marked as Broker. Product supplier, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-916',
    dataQuality: 'rejected',
    notes: ['REJECTED: Global Computer Spares - Marked as Broker. Spares supplier, not ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-917',
    dataQuality: 'rejected',
    notes: ['REJECTED: Silicon Alley - Marked as Broker. Equipment broker, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-918',
    dataQuality: 'rejected',
    notes: ['REJECTED: Greyhound Networks - Marked as Broker. Network equipment broker.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-922',
    dataQuality: 'rejected',
    notes: ['REJECTED: ORM Systems - Marked as Broker. Systems broker, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-925',
    dataQuality: 'rejected',
    notes: ['REJECTED: Networking Services Limited - Marked as Broker. Network services, not ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-926',
    dataQuality: 'rejected',
    notes: ['REJECTED: Shape Systems - Marked as Broker. Systems broker, not ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-929',
    dataQuality: 'rejected',
    notes: ['REJECTED: PICS Telecom - Marked as Broker. Telecom equipment broker.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-930',
    dataQuality: 'rejected',
    notes: ['REJECTED: ViralVPS - Marked as Broker. VPS hosting, not ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-935',
    dataQuality: 'rejected',
    notes: ['REJECTED: Lafone Communications - Office phones direct, telecom reseller, not ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  // Process IT Service Provider marked leads (generally not ITAD processors)
  {
    id: 'org-742',
    dataQuality: 'rejected',
    notes: ['REJECTED: Proactive Distribution - Marked as IT Service Provider. Distribution company, not ITAD processing.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-911',
    dataQuality: 'rejected',
    notes: ['REJECTED: Telenova - Marked as IT Service Provider. General IT services, not ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-928',
    dataQuality: 'rejected',
    notes: ['REJECTED: Wellnex UK - Marked as IT Service Provider/Broker. Not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-931',
    dataQuality: 'rejected',
    notes: ['REJECTED: geotek.biz Associates - Marked as IT Service Provider. General IT, not ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-932',
    dataQuality: 'rejected',
    notes: ['REJECTED: Telecoms Traders - Marked as IT Service Provider. Telecoms trading, not ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-934',
    dataQuality: 'rejected',
    notes: ['REJECTED: SQS - tape drive repair specialist, not comprehensive ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-939',
    dataQuality: 'rejected',
    notes: ['REJECTED: CAB IT Services - General IT service provider, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-956',
    dataQuality: 'rejected',
    notes: ['REJECTED: Nerds2u - Consumer IT support service, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-964',
    dataQuality: 'rejected',
    notes: ['REJECTED: Eurosoft (UK) - Software/IT service provider, not ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  // Process some no-website entries
  {
    id: 'org-937',
    dataQuality: 'rejected',
    notes: ['REJECTED: ICT-TWS Company Ltd - No website provided. Cannot verify ITAD operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-976',
    dataQuality: 'rejected',
    notes: ['REJECTED: Colosseum Tandlægerne - Appears to be dental practice (Danish). Not ITAD.'],
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
console.log(`Batch 5 updates complete - ${updates.length} leads processed`);