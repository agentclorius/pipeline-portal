#!/usr/bin/env python3
"""
Process next 100 leads to reach the 150 target
"""

import json
import time
import requests
import re

def clean_html(text):
    """Remove HTML tags and clean text"""
    clean = re.compile('<.*?>')
    text = re.sub(clean, ' ', text)
    text = ' '.join(text.split())
    return text.lower()

def quick_analyze(url):
    """Quick ITAD analysis"""
    try:
        if not url or url.strip() == "":
            return "reject", "No website", 0
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
        
        if response.status_code != 200:
            return "reject", f"HTTP {response.status_code}", 0
        
        content = clean_html(response.text)
        
        # Quick disqualifiers
        disqualifiers = [
            'web design', 'software development', 'hosting', 'domain',
            'retail store', 'consumer sales', 'repair only', 'phone repair',
            'parts supplier only', 'components only'
        ]
        
        for disq in disqualifiers:
            if disq in content:
                return "reject", f"Disqualified: {disq}", 0
        
        # ITAD scoring
        score = 0
        indicators = []
        
        # High value indicators
        high_value = [
            'data destruction', 'data erasure', 'nist', 'dod', 'asset disposal',
            'it disposal', 'weee', 'r2 certified', 'e-stewards', 'degaussing',
            'shredding', 'certificate of destruction'
        ]
        
        for indicator in high_value:
            if indicator in content:
                score += 10
                indicators.append(indicator)
        
        # Medium value
        medium_value = [
            'remarketing', 'refurbishment', 'itad', 'lifecycle services',
            'asset recovery', 'processing facility', 'collection service'
        ]
        
        for indicator in medium_value:
            if indicator in content:
                score += 5
                indicators.append(indicator)
        
        # Basic recycling
        basic = ['it recycling', 'computer recycling', 'electronics recycling']
        for indicator in basic:
            if indicator in content:
                score += 2
                indicators.append(indicator)
        
        # Determine result
        if score >= 15:
            return "qualified", f"Score: {score}, Key: {indicators[0] if indicators else 'N/A'}", min(score + 50, 85)
        elif score >= 8:
            return "maybe", f"Score: {score}, Found: {len(indicators)} indicators", score + 50
        else:
            return "reject", f"Low ITAD score: {score}", score
            
    except Exception as e:
        return "reject", f"Error: {str(e)[:50]}", 0

def process_next_100():
    """Process leads 51-150"""
    
    # Load batch
    with open('scripts/unverified_batch.json', 'r') as f:
        all_leads = json.load(f)
    
    # Take leads 51-150
    batch = all_leads[50:150]
    
    print(f"Processing next {len(batch)} leads (51-150)...")
    
    qualified = []
    rejected = []
    maybe = []
    
    for i, lead in enumerate(batch):
        name = lead['name']
        website = lead.get('website', '')
        industry = lead.get('industry', '')
        
        print(f"{i+51}/150: {name}")
        
        # Quick industry filter
        if industry.lower() in ['broker', 'trading', 'distribution', 'retail']:
            result = {
                'id': lead['id'],
                'name': name,
                'decision': 'reject',
                'reason': f'Industry: {industry}',
                'score': 0,
                'website': website
            }
            rejected.append(result)
            print(f"❌ REJECT: Industry filter - {industry}")
            continue
        
        # Analyze website
        decision, reason, score = quick_analyze(website)
        
        result = {
            'id': lead['id'],
            'name': name,
            'decision': decision,
            'reason': reason,
            'score': score,
            'website': website,
            'industry': industry
        }
        
        if decision == 'qualified':
            qualified.append(result)
            print(f"✅ QUALIFIED: {name} - {reason}")
        elif decision == 'maybe':
            maybe.append(result)
            print(f"⚠️  MAYBE: {name} - {reason}")
        else:
            rejected.append(result)
            print(f"❌ REJECT: {name} - {reason}")
        
        time.sleep(0.8)  # Rate limiting
        
        # Progress checkpoint every 25
        if (i + 1) % 25 == 0:
            print(f"\nProgress checkpoint {i+51}/150:")
            print(f"Qualified: {len(qualified)}, Maybe: {len(maybe)}, Rejected: {len(rejected)}\n")
    
    # Save results
    results = {
        'batch': 'leads_51-150',
        'qualified': qualified,
        'maybe': maybe,
        'rejected': rejected,
        'summary': {
            'total': len(batch),
            'qualified': len(qualified),
            'maybe': len(maybe),
            'rejected': len(rejected)
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('scripts/batch2_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n--- BATCH 2 COMPLETE ---")
    print(f"Processed: {len(batch)}")
    print(f"Qualified: {len(qualified)}")
    print(f"Maybe: {len(maybe)}")
    print(f"Rejected: {len(rejected)}")
    
    return results

if __name__ == "__main__":
    process_next_100()