#!/usr/bin/env python3
import json
import requests
import time
from datetime import datetime
import sys

def load_leadpool():
    with open('/tmp/pipeline-portal/src/data/leadpool.json', 'r') as f:
        return json.load(f)

def save_leadpool(leads):
    with open('/tmp/pipeline-portal/src/data/leadpool.json', 'w') as f:
        json.dump(leads, f, indent=2)

def get_unverified_leads(leads, limit=150):
    unverified = []
    for lead in leads:
        quality = lead.get('dataQuality', '').lower()
        if quality not in ['verified', 'rejected']:
            unverified.append(lead)
        if len(unverified) >= limit:
            break
    return unverified

def check_website(url):
    if not url or url.strip() == '':
        return {'accessible': False, 'reason': 'No website'}
    
    if not url.startswith('http'):
        url = 'https://' + url
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; ReturnaBot/1.0)'
        })
        
        content = response.text.lower()
        
        # ITAD keywords
        itad_keywords = ['itad', 'asset disposal', 'data destruction', 'electronics recycling', 
                        'computer recycling', 'hardware disposal', 'refurbishment', 'remanufacturing',
                        'processing facility', 'erasure', 'wiping', 'e-waste']
        
        itad_score = sum(1 for keyword in itad_keywords if keyword in content)
        
        return {
            'accessible': True,
            'itad_score': itad_score,
            'status_code': response.status_code
        }
        
    except Exception as e:
        return {'accessible': False, 'reason': str(e)[:50]}

def screen_lead(lead, index, total):
    name = lead['name']
    website = lead.get('website', 'NO WEBSITE')
    
    print(f"[{index}/{total}] {name}")
    print(f"  Website: {website}")
    
    # Flush output
    sys.stdout.flush()
    
    website_info = check_website(website)
    
    if not website_info['accessible']:
        decision = 'rejected'
        reason = f"Website issue: {website_info['reason']}"
    elif website_info['itad_score'] >= 2:
        decision = 'promoted'
        reason = f"ITAD focus (score: {website_info['itad_score']})"
        lead['score'] = 75
        lead['stage'] = 'qualified'
        lead['isPipeline'] = True
    else:
        decision = 'rejected' 
        reason = f"Limited ITAD focus (score: {website_info['itad_score']})"
    
    # Update lead
    lead['dataQuality'] = 'verified' if decision == 'promoted' else 'rejected'
    lead['lastVerified'] = datetime.utcnow().isoformat() + 'Z'
    
    if 'notes' not in lead:
        lead['notes'] = []
    lead['notes'].append(f"Evening enrichment {datetime.now().strftime('%Y-%m-%d %H:%M')}: {reason}")
    
    print(f"  Result: {decision.upper()} - {reason}")
    print("")
    
    return decision

def main():
    print("🌙 EVENING DATA ENRICHMENT")
    print("=" * 50)
    
    leads = load_leadpool()
    unverified = get_unverified_leads(leads, 150)
    
    print(f"Processing {len(unverified)} unverified leads...")
    print("")
    
    promoted = 0
    rejected = 0
    
    for i, lead in enumerate(unverified, 1):
        try:
            decision = screen_lead(lead, i, len(unverified))
            if decision == 'promoted':
                promoted += 1
            else:
                rejected += 1
            
            # Save periodically
            if i % 25 == 0:
                save_leadpool(leads)
                print(f"💾 Progress saved (processed {i}/{len(unverified)})")
                print("")
            
            time.sleep(1)  # Rate limiting
            
        except KeyboardInterrupt:
            print("Interrupted by user")
            break
        except Exception as e:
            print(f"  ERROR: {e}")
    
    # Final save
    save_leadpool(leads)
    
    print("=" * 50)
    print(f"COMPLETED")
    print(f"Promoted: {promoted}")
    print(f"Rejected: {rejected}")
    print(f"Total: {promoted + rejected}")
    
    # Check remaining
    remaining = get_unverified_leads(load_leadpool(), 1000)
    print(f"Remaining unverified: {len(remaining)}")

if __name__ == "__main__":
    main()