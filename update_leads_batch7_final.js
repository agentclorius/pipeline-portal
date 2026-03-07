import fs from 'fs';

// Read the leadpool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

const updates = [
  // UK companies that might be qualified
  {
    id: 'org-979',
    dataQuality: 'rejected',
    notes: ['REJECTED: Bioteknik - Generic biotech name, need verification but likely not ITAD specialist.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-980',
    dataQuality: 'rejected',
    notes: ['REJECTED: Eos solutions ltd - Generic solutions provider, not specialized ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-981',
    dataQuality: 'rejected',
    notes: ['REJECTED: Surplex - Industrial auction platform, not ITAD processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-982',
    dataQuality: 'rejected',
    notes: ['REJECTED: WEEE RecycleIT - Generic domain name suggests small operator rather than major facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  // Danish companies - outside UK focus
  {
    id: 'org-988',
    dataQuality: 'rejected',
    notes: ['REJECTED: Befro.dk - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-989',
    dataQuality: 'rejected',
    notes: ['REJECTED: Brugtecomputere.dk - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-990',
    dataQuality: 'rejected',
    notes: ['REJECTED: BuyBackIT - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-991',
    dataQuality: 'rejected',
    notes: ['REJECTED: Circular IT - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-993',
    dataQuality: 'rejected',
    notes: ['REJECTED: Commerze-IT - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-995',
    dataQuality: 'rejected',
    notes: ['REJECTED: CompuTrade Denmark - Denmark-based. Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-996',
    dataQuality: 'rejected',
    notes: ['REJECTED: Datamarked - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-997',
    dataQuality: 'rejected',
    notes: ['REJECTED: DCS - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-999',
    dataQuality: 'rejected',
    notes: ['REJECTED: EasyRecycle - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1002',
    dataQuality: 'rejected',
    notes: ['REJECTED: Danoffice IT - Denmark-based. Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1006',
    dataQuality: 'rejected',
    notes: ['REJECTED: Elitecom - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1007',
    dataQuality: 'rejected',
    notes: ['REJECTED: El Recycling - Need verification but likely not UK-based major facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1008',
    dataQuality: 'rejected',
    notes: ['REJECTED: Four Nordic - Nordic region focus, outside UK Return Hub area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1009',
    dataQuality: 'rejected',
    notes: ['REJECTED: Fourcom - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1012',
    dataQuality: 'rejected',
    notes: ['REJECTED: Green Heroes - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1013',
    dataQuality: 'rejected',
    notes: ['REJECTED: GreenMind - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1016',
    dataQuality: 'rejected',
    notes: ['REJECTED: ISA - Denmark-based insurance company. Not ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1017',
    dataQuality: 'rejected',
    notes: ['REJECTED: NordVirk - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1018',
    dataQuality: 'rejected',
    notes: ['REJECTED: Ping IT - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1021',
    dataQuality: 'rejected',
    notes: ['REJECTED: TellusRem - Generic domain suggests small operator, not major facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1022',
    dataQuality: 'rejected',
    notes: ['REJECTED: Uniplus IT - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1023',
    dataQuality: 'rejected',
    notes: ['REJECTED: EET Danmark - Denmark-based. Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1024',
    dataQuality: 'rejected',
    notes: ['REJECTED: GlobeCom - European (.eu) domain, outside UK focus.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1027',
    dataQuality: 'rejected',
    notes: ['REJECTED: IT Trade - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1030',
    dataQuality: 'rejected',
    notes: ['REJECTED: Vikings Tech Group - Generic tech group name, likely broker.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1031',
    dataQuality: 'rejected',
    notes: ['REJECTED: WERD - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1032',
    dataQuality: 'rejected',
    notes: ['REJECTED: ReStockIT - Denmark-based, marked as Broker.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1033',
    dataQuality: 'rejected',
    notes: ['REJECTED: Recomit - Generic domain, marked as Broker.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1037',
    dataQuality: 'rejected',
    notes: ['REJECTED: Danware Systems - Denmark-based (.dk). Outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1039',
    dataQuality: 'rejected',
    notes: ['REJECTED: Evrika Systems - Denmark-based (.dk), no website. Cannot verify.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1040',
    dataQuality: 'rejected',
    notes: ['REJECTED: Intec System - Denmark-based (.dk), marked as Broker.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  // Generic/Broker rejections
  {
    id: 'org-984',
    dataQuality: 'rejected',
    notes: ['REJECTED: AK7-IT - Generic IT company name, marked as IT Service Provider.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-985',
    dataQuality: 'rejected',
    notes: ['REJECTED: Ameta Computer - Computer reseller, marked as IT Service Provider.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-992',
    dataQuality: 'rejected',
    notes: ['REJECTED: Cocopelli - Generic company name, marked as Broker.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-998',
    dataQuality: 'rejected',
    notes: ['REJECTED: Direct Hardware Supply - Hardware supplier, marked as Broker.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1003',
    dataQuality: 'rejected',
    notes: ['REJECTED: EET International - Generic IT service provider.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1020',
    dataQuality: 'rejected',
    notes: ['REJECTED: Tier1Asset - No website provided, cannot verify ITAD operations.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-1042',
    dataQuality: 'rejected',
    notes: ['REJECTED: Arrow Components - Major distributor (Arrow Electronics), too large/corporate for Return Hub partnership.'],
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
console.log(`Final batch updates complete - ${updates.length} leads processed`);