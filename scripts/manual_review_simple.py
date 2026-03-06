#!/usr/bin/env python3
"""
Manual review script for potential ITAD candidates - simplified version
"""

import json
import requests
import time
import logging
import re

logging.basicConfig(level=logging.INFO)

def clean_html(text):
    """Remove HTML tags and clean text"""
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text = re.sub(clean, ' ', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.lower()

def analyze_website(url):
    """Analyze website for ITAD services"""
    try:
        if not url.startswith(('http://', 'https://')):
            test_url = 'https://' + url
        else:
            test_url = url
        
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        response = requests.get(test_url, timeout=15, headers=headers, allow_redirects=True)
        
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}", None, 0
        
        content = clean_html(response.text)
        
        # Strong ITAD indicators (10 points each)
        strong_indicators = [
            'data destruction', 'data erasure', 'secure erasure', 'nist', 'dod 5220',
            'asset disposal', 'it disposal', 'weee', 'iso 14001', 'r2 certified',
            'e-stewards', 'asset recovery', 'certificate of destruction',
            'hard drive destruction', 'degaussing', 'shredding'
        ]
        
        # Medium indicators (5 points each)
        medium_indicators = [
            'remarketing', 'refurbishment', 'end of life', 'decommission',
            'processing facility', 'own facility', 'warehouse', 'collection service',
            'pickup service', 'reverse logistics', 'itad', 'lifecycle services'
        ]
        
        # Weak indicators (2 points each)
        weak_indicators = [
            'it recycling', 'computer recycling', 'electronics recycling',
            'laptop', 'desktop', 'server disposal', 'equipment disposal'
        ]
        
        # Negative indicators (disqualifies)
        negative_indicators = [
            'web design', 'software development', 'web hosting', 'domain registration',
            'retail store', 'consumer sales', 'repair shop', 'phone repair',
            'parts only', 'components only'
        ]
        
        # Check for disqualifiers
        for neg in negative_indicators:
            if neg in content:
                return False, f"Disqualified: {neg}", None, 0
        
        # Calculate score
        score = 0
        found_indicators = []
        
        for indicator in strong_indicators:
            if indicator in content:
                score += 10
                found_indicators.append(f"Strong: {indicator}")
        
        for indicator in medium_indicators:
            if indicator in content:
                score += 5
                found_indicators.append(f"Medium: {indicator}")
        
        for indicator in weak_indicators:
            if indicator in content:
                score += 2
                found_indicators.append(f"Weak: {indicator}")
        
        # Business model check
        has_business_indicators = any(term in content for term in [
            'iso certified', 'certified', 'compliant', 'licensed', 'accredited',
            'years experience', 'established', 'professional', 'enterprise'
        ])
        
        if has_business_indicators and score > 0:
            score += 3
            found_indicators.append("Business indicators")
        
        analysis = f"Score: {score}, Found: {', '.join(found_indicators[:3])}"
        
        if score >= 15:
            return True, "High confidence ITAD processor", analysis, score
        elif score >= 8:
            return None, "Possible ITAD processor", analysis, score  
        else:
            return False, "Insufficient ITAD evidence", analysis, score
            
    except Exception as e:
        return False, f"Error: {str(e)[:50]}", None, 0

def process_manual_reviews():
    """Process the manual review leads"""
    
    # Load enrichment results
    with open('scripts/enrichment_results.json', 'r') as f:
        data = json.load(f)
    
    manual_leads = [lead for lead in data['results'] if lead['decision'] == 'manual_review']
    
    print(f"Analyzing {len(manual_leads)} leads requiring manual review...")
    
    qualified = []
    rejected = []
    maybe = []
    
    for i, lead in enumerate(manual_leads):
        name = lead['name']
        website = lead['website']
        
        print(f"\n{i+1}/{len(manual_leads)}: {name}")
        
        if not website:
            result = {
                'id': lead['id'],
                'name': name,
                'decision': 'reject',
                'reason': 'No website',
                'score': 0
            }
            rejected.append(result)
            print("❌ REJECT: No website")
            continue
        
        is_itad, reason, analysis, score = analyze_website(website)
        
        result = {
            'id': lead['id'],
            'name': name,
            'website': website,
            'decision': '',
            'reason': reason,
            'analysis': analysis,
            'score': score
        }
        
        if is_itad is True:
            result['decision'] = 'qualified'
            qualified.append(result)
            print(f"✅ QUALIFIED: {name} - {analysis}")
            
        elif is_itad is None:
            result['decision'] = 'maybe'
            maybe.append(result)
            print(f"⚠️  MAYBE: {name} - {analysis}")
            
        else:
            result['decision'] = 'reject'
            rejected.append(result)
            print(f"❌ REJECT: {name} - {reason}")
        
        time.sleep(1)  # Be respectful
    
    # Save results
    results = {
        'qualified': qualified,
        'maybe': maybe, 
        'rejected': rejected,
        'summary': {
            'total': len(manual_leads),
            'qualified': len(qualified),
            'maybe': len(maybe),
            'rejected': len(rejected)
        },
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('scripts/manual_review_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n--- FINAL SUMMARY ---")
    print(f"Total reviewed: {len(manual_leads)}")
    print(f"Qualified: {len(qualified)}")
    print(f"Maybe: {len(maybe)}")
    print(f"Rejected: {len(rejected)}")
    
    return results

if __name__ == "__main__":
    process_manual_reviews()