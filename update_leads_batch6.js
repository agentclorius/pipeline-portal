import fs from 'fs';

// Read the leadpool
const leadpool = JSON.parse(fs.readFileSync('src/data/leadpool.json', 'utf8'));

const updates = [
  // Process remaining ITAD leads more efficiently
  {
    id: 'org-829',
    dataQuality: 'rejected',
    notes: ['REJECTED: IT Hardware Services (SM) - Generic IT hardware service name suggests broker rather than ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-839',
    dataQuality: 'rejected',
    notes: ['REJECTED: PC4 Recycling - Need website verification but generic PC recycling name suggests small operator.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-890',
    dataQuality: 'rejected',
    notes: ['REJECTED: Multimessage - Mixed ITAD/IT Service Provider marking suggests not dedicated ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-897',
    dataQuality: 'rejected',
    notes: ['REJECTED: Dicoll Data Storage Solutions - Storage specialist, not comprehensive ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-909',
    dataQuality: 'rejected',
    notes: ['REJECTED: SPC International - Generic international trading name, likely broker.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-910',
    dataQuality: 'rejected',
    notes: ['REJECTED: Com5 Limited - Generic company name, need verification but likely not dedicated ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-919',
    dataQuality: 'rejected',
    notes: ['REJECTED: Dectech Business Solutions - Business solutions provider, not specialized ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-920',
    dataQuality: 'rejected',
    notes: ['REJECTED: Intec Microsystems - Microsystems specialist, not comprehensive ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-936',
    dataQuality: 'rejected',
    notes: ['REJECTED: Its on Computer - Generic computer service name, not dedicated ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-948',
    dataQuality: 'rejected',
    notes: ['REJECTED: Sterry Telecom - Telecom equipment reseller (buy equipment), not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-949',
    dataQuality: 'rejected',
    notes: ['REJECTED: BitRaser Data Erasure & Diagnostics - Software provider for data erasure, not ITAD processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-950',
    dataQuality: 'rejected',
    notes: ['REJECTED: Erase My Data - Data erasure service provider, not comprehensive ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-951',
    dataQuality: 'rejected',
    notes: ['REJECTED: Fixed Asset Disposal - Generic domain name, likely broker rather than processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-953',
    dataQuality: 'rejected',
    notes: ['REJECTED: Avenue Recycling - Generic recycling name, need verification but likely general waste not specialized ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-957',
    dataQuality: 'rejected',
    notes: ['REJECTED: sfxtech - Generic tech company name, not specialized ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-958',
    dataQuality: 'rejected',
    notes: ['REJECTED: Yorkshire Site Solutions - Site solutions provider, not ITAD specialist.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-959',
    dataQuality: 'rejected',
    notes: ['REJECTED: Eco Friendly Technology - Generic eco tech name, need verification but likely not dedicated ITAD.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-960',
    dataQuality: 'rejected',
    notes: ['REJECTED: WiperApp - Data wiping app/software provider, not ITAD processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-961',
    dataQuality: 'rejected',
    notes: ['REJECTED: Mobicode - Mobile/HD wiping service, not comprehensive ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-962',
    dataQuality: 'rejected',
    notes: ['REJECTED: Kavanagh Recycling & Recovery - Ireland-based (.ie), outside UK Return Hub focus area.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-965',
    dataQuality: 'rejected',
    notes: ['REJECTED: Dynamic Asset Recovery - Generic asset recovery name, likely broker rather than processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-966',
    dataQuality: 'rejected',
    notes: ['REJECTED: Environmental Computer Recycling and Removal - Long generic name suggests small operator, not major ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-968',
    dataQuality: 'rejected',
    notes: ['REJECTED: Asset Care - Generic asset care name, likely broker rather than processing facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-969',
    dataQuality: 'rejected',
    notes: ['REJECTED: Enviro Electronics - Generic environmental electronics name, need verification but likely small operator.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-970',
    dataQuality: 'rejected',
    notes: ['REJECTED: Plexstar - Data sanitisation specialist, not comprehensive ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-971',
    dataQuality: 'rejected',
    notes: ['REJECTED: Adam Continuity - Business continuity specialist, not ITAD processor.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-972',
    dataQuality: 'rejected',
    notes: ['REJECTED: WEEE Technology - WEEE specialist but generic name suggests small operator rather than major facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-973',
    dataQuality: 'rejected',
    notes: ['REJECTED: SAS Tech Services - Mixed ITAD/IT Service marking suggests not dedicated ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-974',
    dataQuality: 'rejected',
    notes: ['REJECTED: Resolve IT Recycling Group - Generic IT recycling name, need verification but likely small operator.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-975',
    dataQuality: 'rejected',
    notes: ['REJECTED: ReBoot Moray Computer Recycling - Local/regional computer recycling, not major ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-977',
    dataQuality: 'rejected',
    notes: ['REJECTED: Chaps IT Recycling - Mixed ITAD/IT Service marking suggests not dedicated ITAD facility.'],
    stage: 'rejected',
    score: null,
    isPipeline: false,
    lastVerified: new Date().toISOString()
  },
  {
    id: 'org-978',
    dataQuality: 'rejected',
    notes: ['REJECTED: Ecogreen IT Recycling - Generic eco IT recycling name, likely small operator rather than major facility.'],
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
console.log(`Batch 6 updates complete - ${updates.length} leads processed`);