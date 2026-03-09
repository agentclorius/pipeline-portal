#!/usr/bin/env python3
import json
import requests
import time
from datetime import datetime

def load_leadpool():
    """Load leadpool data"""
    with open('/tmp/pipeline-portal/src/data/leadpool.json', 'r') as f:
        return json.load(f)

def save_leadpool(leads):
    """Save updated leadpool data"""
    with open('/tmp/pipeline-portal/src/data/leadpool.json', 'w') as f:
        json.dump(leads, f, indent=2)

def filter_truly_unverified(leads):
    """Get leads that need verification (not rejected or verified)"""
    unverified = []
    for lead in leads:
        quality = lead.get('dataQuality', '').lower()
        if quality not in ['verified', 'rejected']:
            unverified.append(lead)
    return unverified

def check_website_accessibility(url):
    """Check if website is accessible and returns basic info"""
    if not url or url.strip() == '':
        return {'accessible': False, 'reason': 'No website provided'}
    
    # Clean up URL
    if not url.startswith('http'):
        url = 'https://' + url
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; LeadVerifier/1.0)'
        })
        if response.status_code == 200:
            content = response.text.lower()
            itad_keywords = ['itad', 'it asset disposal', 'asset disposal', 'data destruction', 
                           'electronics recycling', 'computer recycling', 'hardware disposal',
                           'secure data wiping', 'asset recovery']
            
            itad_score = sum(1 for keyword in itad_keywords if keyword in content)
            
            return {
                'accessible': True,
                'status_code': response.status_code,
                'itad_keywords': itad_score,
                'has_itad_focus': itad_score >= 2
            }
        else:
            return {'accessible': False, 'reason': f'HTTP {response.status_code}'}
    except Exception as e:
        return {'accessible': False, 'reason': str(e)}

def screen_lead(lead):
    """Screen a single lead and make promotion/rejection decision"""
    print(f"\n🔍 Screening: {lead['name']}")
    print(f"   Location: {lead.get('address', 'No address')}, {lead.get('country', 'No country')}")
    print(f"   Website: {lead.get('website', 'NO WEBSITE')}")
    
    # Check website
    website_info = check_website_accessibility(lead.get('website', ''))
    
    decision = 'rejected'
    reason = ''
    
    if not website_info['accessible']:
        reason = f"Website not accessible: {website_info['reason']}"
        decision = 'rejected'
    elif website_info.get('has_itad_focus', False):
        reason = f"ITAD-focused website (keywords: {website_info['itad_keywords']})"
        decision = 'promoted'
    else:
        reason = f"Website accessible but minimal ITAD focus (keywords: {website_info.get('itad_keywords', 0)})"
        decision = 'rejected'
    
    # Update lead
    lead['dataQuality'] = 'verified' if decision == 'promoted' else 'rejected'
    lead['lastVerified'] = datetime.utcnow().isoformat() + 'Z'
    lead['updatedAt'] = datetime.utcnow().isoformat() + 'Z'
    
    if 'notes' not in lead:
        lead['notes'] = []
    lead['notes'].append(f"Auto-screened {datetime.now().strftime('%Y-%m-%d')}: {reason}")
    
    print(f"   ✅ {decision.upper()}: {reason}")
    
    return decision

if __name__ == "__main__":
    print("🚀 Starting lead screening session...")
    
    leads = load_leadpool()
    unverified = filter_truly_unverified(leads)
    
    print(f"📊 Found {len(unverified)} leads needing verification")
    
    if len(unverified) == 0:
        print("✅ All leads are already verified or rejected!")
        exit(0)
    
    # Take first 10 for this session
    batch = unverified[:10]
    
    promoted = 0
    rejected = 0
    
    for lead in batch:
        try:
            decision = screen_lead(lead)
            if decision == 'promoted':
                promoted += 1
            else:
                rejected += 1
            time.sleep(2)  # Rate limiting
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
    
    # Save updated data
    save_leadpool(leads)
    
    print(f"\n📈 Session complete:")
    print(f"   Promoted: {promoted}")
    print(f"   Rejected: {rejected}")
    print(f"   Remaining unverified: {len(unverified) - len(batch)}")