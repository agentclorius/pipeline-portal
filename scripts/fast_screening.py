#!/usr/bin/env python3
"""
Fast screening for remaining leads - efficient approach
"""

import json
import time
import requests

def fast_screen_lead(lead):
    """Quick screening based on name, industry, and basic website check"""
    
    name = lead['name'].lower()
    industry = lead.get('industry', '').lower() 
    website = lead.get('website', '').strip()
    
    # Immediate rejects based on name/industry
    red_flags = [
        'broker', 'trading', 'distribution', 'retail', 'epos', 'sales',
        'consultant', 'advisory', 'software', 'development', 'marketing',
        'web design', 'hosting', 'domain', 'phone repair', 'repair shop'
    ]
    
    for flag in red_flags:
        if flag in name or flag in industry:
            return {
                'id': lead['id'],
                'name': lead['name'],
                'decision': 'reject',
                'reason': f'Red flag: {flag}',
                'score': 0,
                'website': website
            }
    
    # Strong ITAD indicators in name
    strong_itad_names = [
        'recycl', 'disposal', 'asset', 'destruct', 'erasure', 'weee',
        'refurb', 'remarket', 'recover', 'lifecycle', 'itad'
    ]
    
    name_score = 0
    for indicator in strong_itad_names:
        if indicator in name:
            name_score += 10
    
    # Website check
    website_accessible = False
    if website:
        try:
            if not website.startswith(('http://', 'https://')):
                test_url = 'https://' + website
            else:
                test_url = website
            
            response = requests.head(test_url, timeout=5, allow_redirects=True)
            website_accessible = response.status_code == 200
        except:
            website_accessible = False
    
    # Decision logic
    if not website:
        decision = 'reject'
        reason = 'No website'
        score = 0
    elif not website_accessible:
        decision = 'reject'
        reason = 'Website inaccessible'
        score = 0
    elif name_score >= 10:
        decision = 'qualified'
        reason = f'Strong name indicators (score: {name_score})'
        score = 65 + min(name_score, 15)
    elif industry in ['itad'] or 'recycling' in industry:
        decision = 'maybe'
        reason = f'ITAD industry classification'
        score = 60
    else:
        decision = 'reject'
        reason = 'No clear ITAD indicators'
        score = 0
    
    return {
        'id': lead['id'],
        'name': lead['name'],
        'decision': decision,
        'reason': reason,
        'score': score,
        'website': website,
        'industry': industry
    }

def process_all_remaining():
    """Process remaining leads with fast screening"""
    
    # Load the batch
    with open('scripts/unverified_batch.json', 'r') as f:
        all_leads = json.load(f)
    
    # Process leads 51-150
    remaining_leads = all_leads[50:150]
    
    print(f"Fast screening {len(remaining_leads)} remaining leads...")
    
    qualified = []
    maybe = []
    rejected = []
    
    for i, lead in enumerate(remaining_leads):
        result = fast_screen_lead(lead)
        
        if result['decision'] == 'qualified':
            qualified.append(result)
            print(f"{i+51}/150: ✅ QUALIFIED - {lead['name']}")
        elif result['decision'] == 'maybe':
            maybe.append(result)
            print(f"{i+51}/150: ⚠️  MAYBE - {lead['name']}")
        else:
            rejected.append(result)
            print(f"{i+51}/150: ❌ REJECT - {lead['name']} ({result['reason']})")
        
        # Brief pause
        time.sleep(0.2)
        
        if (i + 1) % 25 == 0:
            print(f"\nCheckpoint {i+51}/150: Q:{len(qualified)} M:{len(maybe)} R:{len(rejected)}\n")
    
    # Save results
    results = {
        'batch': 'fast_screening_51-150',
        'qualified': qualified,
        'maybe': maybe,
        'rejected': rejected,
        'summary': {
            'total': len(remaining_leads),
            'qualified': len(qualified),
            'maybe': len(maybe), 
            'rejected': len(rejected)
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('scripts/fast_screening_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n--- FAST SCREENING COMPLETE ---")
    print(f"Total processed: {len(remaining_leads)}")
    print(f"Qualified: {len(qualified)}")
    print(f"Maybe: {len(maybe)}")
    print(f"Rejected: {len(rejected)}")
    
    return results

if __name__ == "__main__":
    process_all_remaining()