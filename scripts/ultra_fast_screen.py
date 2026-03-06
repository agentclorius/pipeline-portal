#!/usr/bin/env python3
"""
Ultra-fast screening - name/industry analysis only
"""

import json
import time

def ultra_fast_screen(lead):
    """Screen based on name and industry only - no network calls"""
    
    name = lead['name'].lower()
    industry = lead.get('industry', '').lower()
    website = lead.get('website', '').strip()
    
    # Immediate rejects
    reject_patterns = [
        'broker', 'trading', 'distribution', 'epos', 'retail', 'sales',
        'consultant', 'advisory', 'software', 'development', 'marketing',
        'web design', 'hosting', 'domain', 'phone repair', 'repair',
        'parts', 'component', 'supplier', 'wholesaler', 'dealer'
    ]
    
    for pattern in reject_patterns:
        if pattern in name or pattern in industry:
            return {
                'id': lead['id'],
                'name': lead['name'],
                'decision': 'reject',
                'reason': f'Pattern: {pattern}',
                'score': 0,
                'website': website
            }
    
    # No website = reject
    if not website or website == '':
        return {
            'id': lead['id'],
            'name': lead['name'],
            'decision': 'reject',
            'reason': 'No website',
            'score': 0,
            'website': website
        }
    
    # Strong ITAD patterns in name
    strong_patterns = [
        'recycl', 'disposal', 'destruct', 'erasure', 'asset',
        'weee', 'refurb', 'remarket', 'recover', 'lifecycle'
    ]
    
    strong_count = sum(1 for pattern in strong_patterns if pattern in name)
    
    # Industry indicators
    itad_industries = ['itad', 'recycling', 'disposal', 'recovery']
    has_itad_industry = any(ind in industry for ind in itad_industries)
    
    # Decision logic
    if strong_count >= 2:
        return {
            'id': lead['id'],
            'name': lead['name'],
            'decision': 'qualified',
            'reason': f'Multiple ITAD indicators in name ({strong_count})',
            'score': 70 + (strong_count * 3),
            'website': website
        }
    elif strong_count == 1 or has_itad_industry:
        return {
            'id': lead['id'],
            'name': lead['name'],
            'decision': 'maybe',
            'reason': f'Single ITAD indicator or industry match',
            'score': 60,
            'website': website
        }
    else:
        return {
            'id': lead['id'],
            'name': lead['name'],
            'decision': 'reject',
            'reason': 'No clear ITAD indicators',
            'score': 0,
            'website': website
        }

def process_remaining_ultra_fast():
    """Ultra-fast processing of remaining leads"""
    
    # Load batch
    with open('scripts/unverified_batch.json', 'r') as f:
        all_leads = json.load(f)
    
    # Process leads 51-150
    remaining = all_leads[50:150]
    
    print(f"Ultra-fast screening {len(remaining)} leads (51-150)...")
    
    qualified = []
    maybe = []
    rejected = []
    
    for i, lead in enumerate(remaining):
        result = ultra_fast_screen(lead)
        
        if result['decision'] == 'qualified':
            qualified.append(result)
            print(f"{i+51}/150: ✅ {lead['name']} - {result['reason']}")
        elif result['decision'] == 'maybe':
            maybe.append(result)
            print(f"{i+51}/150: ⚠️  {lead['name']} - {result['reason']}")
        else:
            rejected.append(result)
    
    # Summary statistics  
    print(f"\n--- ULTRA FAST SCREENING RESULTS ---")
    print(f"Batch 2 (leads 51-150): {len(remaining)} leads")
    print(f"Qualified: {len(qualified)}")
    print(f"Maybe: {len(maybe)}")
    print(f"Rejected: {len(rejected)}")
    
    # Print qualified leads
    if qualified:
        print(f"\n✅ QUALIFIED LEADS ({len(qualified)}):")
        for lead in qualified:
            print(f"  - {lead['name']} (Score: {lead['score']})")
    
    if maybe:
        print(f"\n⚠️  MAYBE LEADS ({len(maybe)}):")
        for lead in maybe:
            print(f"  - {lead['name']}")
    
    # Save results
    results = {
        'batch': 'ultra_fast_51-150',
        'qualified': qualified,
        'maybe': maybe,
        'rejected': rejected,
        'summary': {
            'total': len(remaining),
            'qualified': len(qualified),
            'maybe': len(maybe),
            'rejected': len(rejected)
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('scripts/ultra_fast_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    process_remaining_ultra_fast()