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

def get_unverified_leads(leads, limit=50):
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
    """Quick check if website exists and get basic content"""
    if not url or url.strip() == '' or '@' in url:
        return {'accessible': False, 'reason': 'No valid website URL'}
    
    # Clean URL
    if not url.startswith('http'):
        url = 'https://' + url
    
    try:
        response = requests.get(url, timeout=8, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; LeadVerifier/1.0)'
        }, allow_redirects=True)
        
        if response.status_code != 200:
            return {'accessible': False, 'reason': f'HTTP {response.status_code}'}
            
        content = response.text.lower()
        title = ''
        title_match = re.search(r'<title[^>]*>([^<]*)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        
        # ITAD-related keywords (broader set)
        itad_keywords = [
            'itad', 'it asset disposal', 'asset disposal', 'data destruction', 
            'electronics recycling', 'computer recycling', 'hardware disposal',
            'secure data wiping', 'asset recovery', 'it equipment disposal',
            'electronic waste', 'e-waste', 'computer disposal', 'server disposal',
            'hard drive destruction', 'data sanitization', 'asset liquidation',
            'technology disposal', 'equipment recycling', 'it decommissioning'
        ]
        
        # Component/distributor keywords (to reject)
        distributor_keywords = [
            'distributor', 'supply chain', 'procurement', 'sourcing',
            'components', 'spare parts', 'inventory management',
            'electronic components', 'semiconductor', 'end-of-life sourcing'
        ]
        
        # Infrastructure keywords (to reject) 
        infrastructure_keywords = [
            'network infrastructure', 'optical infrastructure', 'fiber',
            'networking equipment', 'telecoms', 'connectivity solutions'
        ]
        
        itad_score = sum(1 for keyword in itad_keywords if keyword in content)
        distributor_score = sum(1 for keyword in distributor_keywords if keyword in content)
        infrastructure_score = sum(1 for keyword in infrastructure_keywords if keyword in content)
        
        # Check for placeholder/coming soon content
        placeholder_indicators = ['coming soon', 'under construction', 'website is coming', 
                                'new website', 'site down', 'maintenance']
        is_placeholder = any(indicator in content for indicator in placeholder_indicators)
        
        return {
            'accessible': True,
            'title': title,
            'itad_score': itad_score,
            'distributor_score': distributor_score, 
            'infrastructure_score': infrastructure_score,
            'is_placeholder': is_placeholder,
            'content_length': len(content),
            'has_itad_focus': itad_score >= 2,
            'is_distributor': distributor_score >= 2,
            'is_infrastructure': infrastructure_score >= 1
        }
        
    except Exception as e:
        return {'accessible': False, 'reason': str(e)[:100]}

def make_decision(lead, website_info):
    """Make promote/reject decision based on website analysis"""
    name = lead['name']
    
    if not website_info['accessible']:
        return 'rejected', f"Website not accessible: {website_info['reason']}"
    
    if website_info['is_placeholder']:
        return 'rejected', "Website shows placeholder/coming soon content"
    
    if website_info['has_itad_focus']:
        return 'promoted', f"Strong ITAD focus (score: {website_info['itad_score']})"
    
    if website_info['is_distributor']:
        return 'rejected', f"Electronics/components distributor (score: {website_info['distributor_score']})"
        
    if website_info['is_infrastructure']:
        return 'rejected', f"Network/infrastructure provider (score: {website_info['infrastructure_score']})"
    
    if website_info['content_length'] < 500:
        return 'rejected', "Minimal website content, insufficient business information"
    
    # Default to rejected if no clear ITAD focus
    return 'rejected', f"No clear ITAD focus (itad_score: {website_info['itad_score']})"

def screen_lead_bulk(lead):
    """Screen a single lead efficiently"""
    website = lead.get('website', '')
    print(f"🔍 {lead['name']} | {website}")
    
    website_info = quick_website_check(website)
    decision, reason = make_decision(lead, website_info)
    
    # Update lead
    lead['dataQuality'] = 'verified' if decision == 'promoted' else 'rejected'
    lead['lastVerified'] = datetime.utcnow().isoformat() + 'Z'
    lead['updatedAt'] = datetime.utcnow().isoformat() + 'Z'
    
    if 'notes' not in lead:
        lead['notes'] = []
    lead['notes'].append(f"Bulk-screened {datetime.now().strftime('%Y-%m-%d')}: {reason}")
    
    if decision == 'promoted':
        if 'stage' not in lead or lead['stage'] != 'qualified':
            lead['stage'] = 'qualified'
        if 'score' not in lead or lead['score'] < 70:
            lead['score'] = 75
    
    print(f"   → {decision.upper()}: {reason}")
    return decision

def main():
    print("🚀 Starting bulk lead screening...")
    
    leads = load_leadpool()
    unverified = get_unverified_leads(leads, limit=50)  # Process 50 at a time
    
    print(f"📊 Processing {len(unverified)} unverified leads")
    
    promoted = 0
    rejected = 0
    
    for lead in unverified:
        try:
            decision = screen_lead_bulk(lead)
            if decision == 'promoted':
                promoted += 1
            else:
                rejected += 1
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"   ❌ ERROR processing {lead['name']}: {e}")
    
    # Save results
    save_leadpool(leads)
    
    print(f"\n📈 Bulk screening complete:")
    print(f"   ✅ Promoted: {promoted}")
    print(f"   ❌ Rejected: {rejected}")
    print(f"   📊 Total processed: {promoted + rejected}")
    
    # Check remaining
    remaining = get_unverified_leads(load_leadpool(), limit=1000)
    print(f"   🔄 Remaining unverified: {len(remaining)}")

if __name__ == "__main__":
    main()