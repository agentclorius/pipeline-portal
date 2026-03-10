#!/usr/bin/env python3
import json
import requests
import time
from datetime import datetime
import concurrent.futures
from urllib.parse import urljoin, urlparse
import re

def load_leadpool():
    with open('/tmp/pipeline-portal/src/data/leadpool.json', 'r') as f:
        return json.load(f)

def save_leadpool(leads):
    with open('/tmp/pipeline-portal/src/data/leadpool.json', 'w') as f:
        json.dump(leads, f, indent=2)

def get_unverified_leads(leads, limit=150):
    """Get unverified leads that need processing"""
    unverified = []
    for lead in leads:
        quality = lead.get('dataQuality', '').lower()
        if quality not in ['verified', 'rejected']:
            unverified.append(lead)
        if len(unverified) >= limit:
            break
    return unverified

def quick_website_check(url):
    """Check if website exists and analyze ITAD relevance"""
    if not url or url.strip() == '' or '@' in url:
        return {'accessible': False, 'reason': 'No valid website URL'}
    
    # Clean URL
    if not url.startswith('http'):
        url = 'https://' + url
    
    try:
        response = requests.get(url, timeout=8, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ReturnaBot/1.0)'
        }, allow_redirects=True)
        
        if response.status_code != 200:
            return {'accessible': False, 'reason': f'HTTP {response.status_code}'}
            
        content = response.text.lower()
        title = ''
        title_match = re.search(r'<title[^>]*>([^<]*)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        
        # ITAD processing/facility keywords
        processing_keywords = [
            'itad', 'it asset disposal', 'asset disposal', 'data destruction', 
            'electronics recycling', 'computer recycling', 'hardware disposal',
            'secure data wiping', 'asset recovery', 'it equipment disposal',
            'electronic waste', 'e-waste', 'computer disposal', 'server disposal',
            'hard drive destruction', 'data sanitization', 'asset liquidation',
            'technology disposal', 'equipment recycling', 'it decommissioning',
            'refurbishment', 'remanufacturing', 'processing facility', 'warehouse',
            'asset processing', 'erasure', 'wiping', 'disposition'
        ]
        
        # Facility/operations keywords
        facility_keywords = [
            'facility', 'warehouse', 'processing center', 'operations center',
            'certified facility', 'secure facility', 'processing services',
            'own facility', 'in-house processing', 'iso certified', 'r2 certified'
        ]
        
        # Disqualifying keywords (resellers/distributors/consultants)
        disqualify_keywords = [
            'distributor', 'reseller', 'consultant', 'software only',
            'consulting services', 'supply chain', 'procurement', 'sourcing',
            'components', 'spare parts', 'inventory management',
            'electronic components', 'semiconductor', 'end-of-life sourcing',
            'network infrastructure', 'optical infrastructure', 'fiber',
            'networking equipment', 'telecoms', 'connectivity solutions'
        ]
        
        processing_score = sum(1 for keyword in processing_keywords if keyword in content)
        facility_score = sum(1 for keyword in facility_keywords if keyword in content)
        disqualify_score = sum(1 for keyword in disqualify_keywords if keyword in content)
        
        # Check for placeholder content
        placeholder_indicators = ['coming soon', 'under construction', 'website is coming', 
                                'new website', 'site down', 'maintenance', 'parked domain']
        is_placeholder = any(indicator in content for indicator in placeholder_indicators)
        
        return {
            'accessible': True,
            'title': title,
            'processing_score': processing_score,
            'facility_score': facility_score,
            'disqualify_score': disqualify_score,
            'is_placeholder': is_placeholder,
            'content_length': len(content),
            'has_itad_processing': processing_score >= 3,
            'has_facilities': facility_score >= 1,
            'is_disqualified': disqualify_score >= 2
        }
        
    except Exception as e:
        return {'accessible': False, 'reason': str(e)[:100]}

def make_decision(lead, website_info):
    """Make promote/reject decision based on ITAD processing capability"""
    name = lead['name']
    
    if not website_info['accessible']:
        return 'rejected', f"Website not accessible: {website_info['reason']}"
    
    if website_info['is_placeholder']:
        return 'rejected', "Website shows placeholder/parked domain content"
    
    if website_info['is_disqualified']:
        return 'rejected', f"Non-ITAD business (distributor/consultant/components - score: {website_info['disqualify_score']})"
    
    # Strong ITAD with facilities = promote
    if website_info['has_itad_processing'] and website_info['has_facilities']:
        return 'promoted', f"ITAD processor with facilities (processing: {website_info['processing_score']}, facilities: {website_info['facility_score']})"
    
    # Strong ITAD processing but no clear facilities = still promote (benefit of doubt)
    if website_info['has_itad_processing']:
        return 'promoted', f"ITAD processor (processing: {website_info['processing_score']})"
    
    if website_info['content_length'] < 500:
        return 'rejected', "Minimal website content, insufficient business information"
    
    # Default to rejected if no clear ITAD processing capability
    return 'rejected', f"No clear ITAD processing capability (processing: {website_info['processing_score']}, facilities: {website_info['facility_score']})"

def screen_lead(lead):
    """Screen a single lead for ITAD processing capability"""
    website = lead.get('website', '')
    name = lead['name']
    location = f"{lead.get('address', '')}, {lead.get('country', '')}"
    
    print(f"🔍 {name}")
    print(f"   📍 {location}")
    print(f"   🌐 {website if website else 'NO WEBSITE'}")
    
    website_info = quick_website_check(website)
    decision, reason = make_decision(lead, website_info)
    
    # Update lead
    lead['dataQuality'] = 'verified' if decision == 'promoted' else 'rejected'
    lead['lastVerified'] = datetime.utcnow().isoformat() + 'Z'
    lead['updatedAt'] = datetime.utcnow().isoformat() + 'Z'
    
    if 'notes' not in lead:
        lead['notes'] = []
    lead['notes'].append(f"Evening enrichment {datetime.now().strftime('%Y-%m-%d %H:%M')}: {reason}")
    
    if decision == 'promoted':
        # Set as qualified with score
        lead['stage'] = 'qualified'
        if website_info.get('has_facilities', False):
            lead['score'] = 85  # Higher score for verified facilities
        else:
            lead['score'] = 75  # Standard score for ITAD processing
        
        # Add to pipeline
        lead['isPipeline'] = True
        
        # Update services if not set
        if not lead.get('services'):
            lead['services'] = ['ITAD Processing']
    
    print(f"   → {decision.upper()}: {reason}")
    return decision

def main():
    print("🌙 EVENING DATA ENRICHMENT - Priority Lead Screening")
    print("=" * 60)
    print("Target: 150 unverified leads")
    print("Focus: ITAD processing/erasure/refurb with own facilities")
    print("=" * 60)
    
    leads = load_leadpool()
    unverified = get_unverified_leads(leads, limit=150)
    
    print(f"\n📊 Found {len(unverified)} unverified leads to process")
    
    if len(unverified) == 0:
        print("✅ All leads are already verified!")
        return
    
    promoted = 0
    rejected = 0
    errors = 0
    
    start_time = time.time()
    
    for i, lead in enumerate(unverified, 1):
        try:
            print(f"\n[{i}/{len(unverified)}]", end=" ")
            decision = screen_lead(lead)
            
            if decision == 'promoted':
                promoted += 1
            else:
                rejected += 1
                
            # Rate limiting to avoid overwhelming servers
            time.sleep(1.5)
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            errors += 1
    
    # Save updated leadpool
    save_leadpool(leads)
    
    # Summary
    duration = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"📈 EVENING ENRICHMENT COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Promoted to pipeline: {promoted}")
    print(f"❌ Rejected: {rejected}")
    print(f"⚠️  Errors: {errors}")
    print(f"📊 Total processed: {promoted + rejected}")
    print(f"⏱️  Duration: {duration/60:.1f} minutes")
    
    # Check remaining
    remaining_leads = load_leadpool()
    remaining_unverified = get_unverified_leads(remaining_leads, limit=1000)
    print(f"🔄 Remaining unverified: {len(remaining_unverified)}")
    
    if promoted > 0:
        print(f"\n🚀 Next step: Rebuild portal with 'npm run build' and deploy")

if __name__ == "__main__":
    main()