import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { parse } from 'csv-parse/sync';

// ─── Load source data ───────────────────────────────────────────────────────

const orgsCSV = readFileSync('data/certus-pipedrive-export-organizations.csv', 'utf-8');
const peopleCSV = readFileSync('data/certus-pipedrive-export-people.csv', 'utf-8');
const existingPipeline = JSON.parse(readFileSync('data/existing-pipeline.json', 'utf-8'));

const orgsRaw = parse(orgsCSV, { columns: true, skip_empty_lines: true });
const peopleRaw = parse(peopleCSV, { columns: true, skip_empty_lines: true });

// ─── Pipeline status mapping (our statuses → Returna stages) ────────────────

const PIPELINE_STATUS_MAP = {
  'Priority': 'qualified',
  'Research': 'researching',
  'Prospect': 'new',
  'Outreach': 'contacted',
};

// Allowed stages
const VALID_STAGES = ['new', 'researching', 'qualified', 'contacted', 'rejected'];

// ─── Country coordinates ─────────────────────────────────────────────────────

const COUNTRY_COORDS = {
  'England': { lat: 52.3555, lng: -1.1743, country: 'United Kingdom' },
  'Scotland': { lat: 56.4907, lng: -4.2026, country: 'United Kingdom' },
  'Wales': { lat: 52.1307, lng: -3.7837, country: 'United Kingdom' },
  'Northern Ireland': { lat: 54.7877, lng: -6.4923, country: 'United Kingdom' },
  'United Kingdom': { lat: 55.3781, lng: -3.4360, country: 'United Kingdom' },
  'California': { lat: 36.7783, lng: -119.4179, country: 'United States' },
  'New Hampshire': { lat: 43.1939, lng: -71.5724, country: 'United States' },
  'Vermont': { lat: 44.5588, lng: -72.5778, country: 'United States' },
  'Rhode Island': { lat: 41.5801, lng: -71.4774, country: 'United States' },
  'District of Columbia': { lat: 38.9072, lng: -77.0369, country: 'United States' },
  'United States': { lat: 37.0902, lng: -95.7129, country: 'United States' },
  'Germany': { lat: 51.1657, lng: 10.4515, country: 'Germany' },
  'France': { lat: 46.2276, lng: 2.2137, country: 'France' },
  'Netherlands': { lat: 52.1326, lng: 5.2913, country: 'Netherlands' },
  'Belgium': { lat: 50.5039, lng: 4.4699, country: 'Belgium' },
  'Ireland': { lat: 53.1424, lng: -7.6921, country: 'Ireland' },
  'Spain': { lat: 40.4637, lng: -3.7492, country: 'Spain' },
  'Italy': { lat: 41.8719, lng: 12.5674, country: 'Italy' },
  'Portugal': { lat: 39.3999, lng: -8.2245, country: 'Portugal' },
  'Sweden': { lat: 60.1282, lng: 18.6435, country: 'Sweden' },
  'Norway': { lat: 60.4720, lng: 8.4689, country: 'Norway' },
  'Denmark': { lat: 56.2639, lng: 9.5018, country: 'Denmark' },
  'Finland': { lat: 61.9241, lng: 25.7482, country: 'Finland' },
  'Poland': { lat: 51.9194, lng: 19.1451, country: 'Poland' },
  'Austria': { lat: 47.5162, lng: 14.5501, country: 'Austria' },
  'Switzerland': { lat: 46.8182, lng: 8.2275, country: 'Switzerland' },
  'Australia': { lat: -25.2744, lng: 133.7751, country: 'Australia' },
  'New Zealand': { lat: -40.9006, lng: 174.8860, country: 'New Zealand' },
  'Canada': { lat: 56.1304, lng: -106.3468, country: 'Canada' },
  'India': { lat: 20.5937, lng: 78.9629, country: 'India' },
  'China': { lat: 35.8617, lng: 104.1954, country: 'China' },
  'Japan': { lat: 36.2048, lng: 138.2529, country: 'Japan' },
  'South Korea': { lat: 35.9078, lng: 127.7669, country: 'South Korea' },
  'Singapore': { lat: 1.3521, lng: 103.8198, country: 'Singapore' },
  'Malaysia': { lat: 4.2105, lng: 101.9758, country: 'Malaysia' },
  'UAE': { lat: 23.4241, lng: 53.8478, country: 'UAE' },
  'South Africa': { lat: -30.5595, lng: 22.9375, country: 'South Africa' },
  'Brazil': { lat: -14.2350, lng: -51.9253, country: 'Brazil' },
  'Mexico': { lat: 23.6345, lng: -102.5528, country: 'Mexico' },
  'Czech Republic': { lat: 49.8175, lng: 15.4730, country: 'Czech Republic' },
  'Hungary': { lat: 47.1625, lng: 19.5033, country: 'Hungary' },
  'Romania': { lat: 45.9432, lng: 24.9668, country: 'Romania' },
  'Bulgaria': { lat: 42.7339, lng: 25.4858, country: 'Bulgaria' },
  'Estonia': { lat: 58.5953, lng: 25.0136, country: 'Estonia' },
};

// Additional pipeline country lookups (for countries like "UK", "USA", "UK/Ireland", "Estonia/Sweden", "Belgium/France")
const PIPELINE_COUNTRY_COORDS = {
  'UK': COUNTRY_COORDS['United Kingdom'],
  'UK/Ireland': COUNTRY_COORDS['United Kingdom'],
  'USA': COUNTRY_COORDS['United States'],
  'Estonia/Sweden': COUNTRY_COORDS['Estonia'],
  'Belgium/France': COUNTRY_COORDS['Belgium'],
};

function getCoordinates(region, state, address) {
  if (state && COUNTRY_COORDS[state]) return COUNTRY_COORDS[state];
  if (region && COUNTRY_COORDS[region]) return COUNTRY_COORDS[region];
  if (address) {
    for (const [key, coords] of Object.entries(COUNTRY_COORDS)) {
      if (address.toLowerCase().includes(key.toLowerCase())) return coords;
    }
  }
  return { lat: 52.3555, lng: -1.1743, country: 'United Kingdom' };
}

function getPipelineCoordinates(country) {
  if (PIPELINE_COUNTRY_COORDS[country]) return PIPELINE_COUNTRY_COORDS[country];
  if (COUNTRY_COORDS[country]) return COUNTRY_COORDS[country];
  return { lat: 52.3555, lng: -1.1743, country: country };
}

function generateSlug(name) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .substring(0, 50);
}

// ─── Build name index from pipeline for dedup ────────────────────────────────

const pipelineNameIndex = new Map();
for (const p of existingPipeline.pipeline) {
  pipelineNameIndex.set(p.company.trim().toLowerCase(), p);
}

// Strict name matcher: exact match only (case-insensitive, trimmed)
function findPipelineMatch(certusName) {
  const lower = certusName.trim().toLowerCase();
  if (pipelineNameIndex.has(lower)) return pipelineNameIndex.get(lower);
  return null;
}

// ─── Process Certus organizations ────────────────────────────────────────────

const allOrganizations = [];
const orgMap = new Map(); // name → org object
const matchedPipelineNames = new Set();

for (const org of orgsRaw) {
  const id = org['Organization - ID'];
  const name = org['Organization - Name'];
  if (!name || name.trim() === '') continue;

  const slug = generateSlug(name);
  const coords = getCoordinates(
    org['Organization - Region of Address'],
    org['Organization - State/county of Address'],
    org['Organization - Address']
  );

  // Check if this Certus org matches one of our pipeline prospects
  const pipelineMatch = findPipelineMatch(name);

  let stage = 'unverified';
  let score = null;
  let pipelineData = null;
  let isPipeline = false;
  let dataQuality = 'unverified';

  if (pipelineMatch) {
    isPipeline = true;
    matchedPipelineNames.add(pipelineMatch.company.trim().toLowerCase());
    stage = PIPELINE_STATUS_MAP[pipelineMatch.status] || 'new';
    score = pipelineMatch.score || null;
    dataQuality = 'verified';
    pipelineData = pipelineMatch;
  }

  const organization = {
    id: `org-${id}`,
    slug,
    name: name.trim(),
    industry: org['Organization - Industry'] || '',
    website: pipelineMatch?.website || org['Organization - Website ']?.trim() || org['Organization - Website']?.trim() || '',
    address: org['Organization - Address'] || '',
    region: pipelineMatch?.region || org['Organization - Region of Address'] || '',
    state: org['Organization - State/county of Address'] || '',
    country: pipelineMatch?.country || coords.country,
    lat: coords.lat,
    lng: coords.lng,
    stage,
    score,
    isPipeline,
    originalLabel: org['Organization - Labels'] || '',
    dataQuality,
    contacts: [],
    notes: pipelineMatch?.notes ? [pipelineMatch.notes] : [],
    certifications: [],
    services: [],
    pipelineData: isPipeline ? {
      flag: pipelineMatch.flag,
      region: pipelineMatch.region,
      employees: pipelineMatch.employees,
      revenue: pipelineMatch.revenue,
      iso27001: pipelineMatch.iso27001,
      iso14001: pipelineMatch.iso14001,
      contact: pipelineMatch.contact,
      nextAction: pipelineMatch.nextAction,
      lastTouch: pipelineMatch.lastTouch,
    } : null,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    lastVerified: isPipeline ? new Date().toISOString() : null,
  };

  // Build certifications from pipeline data
  if (pipelineMatch) {
    if (pipelineMatch.iso27001) organization.certifications.push('ISO 27001');
    if (pipelineMatch.iso14001) organization.certifications.push('ISO 14001');
    if (pipelineMatch.adisa) organization.certifications.push('ADISA');
    if (pipelineMatch.r2) organization.certifications.push('R2');
  }

  allOrganizations.push(organization);
  orgMap.set(name.trim().toLowerCase(), organization);
}

// ─── Add pipeline-only prospects (not in Certus) ─────────────────────────────

for (const p of existingPipeline.pipeline) {
  const nameKey = p.company.trim().toLowerCase();
  if (matchedPipelineNames.has(nameKey) && orgMap.has(nameKey)) continue;
  // Also check if we already added this via fuzzy match
  let alreadyAdded = false;
  for (const org of allOrganizations) {
    if (org.isPipeline && org.pipelineData && org.notes.length > 0 && org.notes[0] === p.notes) {
      alreadyAdded = true;
      break;
    }
  }
  if (alreadyAdded) continue;

  const coords = getPipelineCoordinates(p.country);
  const slug = generateSlug(p.company);
  const stage = PIPELINE_STATUS_MAP[p.status] || 'new';

  const certs = [];
  if (p.iso27001) certs.push('ISO 27001');
  if (p.iso14001) certs.push('ISO 14001');
  if (p.adisa) certs.push('ADISA');
  if (p.r2) certs.push('R2');

  const organization = {
    id: `org-pipeline-${allOrganizations.length + 1}`,
    slug,
    name: p.company.trim(),
    industry: 'ITAD',
    website: p.website || '',
    address: '',
    region: p.region || '',
    state: '',
    country: p.country,
    lat: coords.lat,
    lng: coords.lng,
    stage,
    score: p.score || null,
    isPipeline: true,
    originalLabel: '',
    dataQuality: 'verified',
    contacts: [],
    notes: p.notes ? [p.notes] : [],
    certifications: certs,
    services: [],
    pipelineData: {
      flag: p.flag,
      region: p.region,
      employees: p.employees,
      revenue: p.revenue,
      iso27001: p.iso27001,
      iso14001: p.iso14001,
      contact: p.contact,
      nextAction: p.nextAction,
      lastTouch: p.lastTouch,
    },
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    lastVerified: new Date().toISOString(),
  };

  allOrganizations.push(organization);
  orgMap.set(nameKey, organization);
}

// ─── Process people and link to organizations ────────────────────────────────

const contacts = [];

for (const person of peopleRaw) {
  const name = person['Person - Name'];
  const orgName = person['Person - Organization'];
  if (!name || name.trim() === '') continue;

  const contact = {
    id: `contact-${contacts.length + 1}`,
    name: name.trim(),
    title: person['Person - Title'] || '',
    email: person['Person - Email - Work'] || person['Person - Email - Home'] || person['Person - Email - Other'] || '',
    phone: person['Person - Phone - Work'] || person['Person - Phone - Mobile'] || person['Person - Phone - Home'] || '',
    linkedin: person['Person - LinkedIn Page'] || '',
    organization: orgName || '',
    marketingStatus: person['Person - Marketing status'] || '',
    dataQuality: 'unverified',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  contacts.push(contact);

  if (orgName) {
    const org = orgMap.get(orgName.trim().toLowerCase());
    if (org) {
      org.contacts.push({
        id: contact.id,
        name: contact.name,
        title: contact.title,
        email: contact.email,
        phone: contact.phone,
        linkedin: contact.linkedin,
      });
    }
  }
}

// ─── Separate into pipeline and leadpool ─────────────────────────────────────

const pipeline = allOrganizations.filter(o => o.isPipeline);
const leadpool = allOrganizations.filter(o => !o.isPipeline);

// ─── Calculate stats ─────────────────────────────────────────────────────────

const pipelineByStage = {};
const pipelineByRegion = {};
const pipelineScores = pipeline.filter(o => o.score && o.score > 0).map(o => o.score);

for (const org of pipeline) {
  pipelineByStage[org.stage] = (pipelineByStage[org.stage] || 0) + 1;
  const region = org.pipelineData?.region || org.region || 'Other';
  pipelineByRegion[region] = (pipelineByRegion[region] || 0) + 1;
}

const leadpoolByCountry = {};
const leadpoolByIndustry = {};

for (const org of leadpool) {
  leadpoolByCountry[org.country] = (leadpoolByCountry[org.country] || 0) + 1;
  if (org.industry) {
    leadpoolByIndustry[org.industry] = (leadpoolByIndustry[org.industry] || 0) + 1;
  }
}

const allByStage = {};
const allByCountry = {};
const allByIndustry = {};

for (const org of allOrganizations) {
  allByStage[org.stage] = (allByStage[org.stage] || 0) + 1;
  allByCountry[org.country] = (allByCountry[org.country] || 0) + 1;
  if (org.industry) {
    allByIndustry[org.industry] = (allByIndustry[org.industry] || 0) + 1;
  }
}

const stats = {
  totalOrganizations: allOrganizations.length,
  totalContacts: contacts.length,
  pipeline: {
    total: pipeline.length,
    byStage: pipelineByStage,
    byRegion: pipelineByRegion,
    avgScore: pipelineScores.length > 0 ? Math.round(pipelineScores.reduce((a, b) => a + b, 0) / pipelineScores.length) : 0,
    topScore: pipelineScores.length > 0 ? Math.max(...pipelineScores) : 0,
    scoreDistribution: {
      high: pipelineScores.filter(s => s >= 80).length,
      medium: pipelineScores.filter(s => s >= 70 && s < 80).length,
      low: pipelineScores.filter(s => s > 0 && s < 70).length,
      unscored: pipeline.filter(o => !o.score || o.score === 0).length,
    },
  },
  leadpool: {
    total: leadpool.length,
    byCountry: leadpoolByCountry,
    byIndustry: leadpoolByIndustry,
  },
  byStage: allByStage,
  byCountry: allByCountry,
  byIndustry: allByIndustry,
  lastUpdated: new Date().toISOString(),
};

// ─── Write output files ──────────────────────────────────────────────────────

try { mkdirSync('src/data', { recursive: true }); } catch (e) {}

writeFileSync('src/data/pipeline.json', JSON.stringify(pipeline, null, 2));
writeFileSync('src/data/leadpool.json', JSON.stringify(leadpool, null, 2));
writeFileSync('src/data/organizations.json', JSON.stringify(allOrganizations, null, 2));
writeFileSync('src/data/contacts.json', JSON.stringify(contacts, null, 2));
writeFileSync('src/data/stats.json', JSON.stringify(stats, null, 2));

console.log(`\n=== Pipeline Portal Data Rebuild ===`);
console.log(`Pipeline prospects: ${pipeline.length}`);
console.log(`  By stage: ${JSON.stringify(pipelineByStage)}`);
console.log(`  Avg score: ${stats.pipeline.avgScore}, Top: ${stats.pipeline.topScore}`);
console.log(`  Score dist: ${JSON.stringify(stats.pipeline.scoreDistribution)}`);
console.log(`Lead pool: ${leadpool.length}`);
console.log(`Total organizations: ${allOrganizations.length}`);
console.log(`Total contacts: ${contacts.length}`);
console.log(`Countries: ${Object.keys(allByCountry).length}`);
console.log(`Output: pipeline.json, leadpool.json, organizations.json, contacts.json, stats.json`);
