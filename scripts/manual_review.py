#!/usr/bin/env python3
"""
Manual review script for potential ITAD candidates
"""

import json
import requests
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO)

class ITADAnalyzer:
    def __init__(self):
        self.qualified_leads = []
        self.rejected_leads = []
        
    def get_website_content(self, url):
        """Get website content for analysis"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
            response = requests.get(url, timeout=15, headers=headers, allow_redirects=True)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text().lower()
                return True, text, response.url
            else:
                return False, f"HTTP {response.status_code}", None
                
        except Exception as e:
            return False, str(e)[:100], None
    
    def analyze_itad_services(self, content, url):
        """Analyze website content for ITAD services"""
        if not content:
            return False, "No content available"
        
        # Strong ITAD indicators
        strong_indicators = [
            'data destruction', 'data erasure', 'secure erasure', 'nist', 'dod',
            'asset disposal', 'it disposal', 'weee', 'iso 14001', 'r2 certification',
            'e-stewards', 'asset recovery', 'remarketing', 'refurbishment',
            'end of life', 'decommission', 'certificate of destruction'
        ]
        
        # Processing facility indicators  
        facility_indicators = [
            'processing facility', 'own facility', 'warehouse', 'processing center',
            'logistics', 'collection service', 'pickup', 'transportation'
        ]
        
        # Weak indicators (could be just resellers)
        weak_indicators = [
            'it recycling', 'computer recycling', 'laptop', 'desktop', 'server'
        ]
        
        # Negative indicators (likely not ITAD processors)
        negative_indicators = [
            'web design', 'software development', 'hosting', 'domain',
            'retail', 'consumer sales', 'repair shop', 'phone repair'
        ]
        
        score = 0
        found_indicators = []
        
        # Check for negative indicators first
        for indicator in negative_indicators:
            if indicator in content:
                return False, f"Negative indicator: {indicator}"
        
        # Check strong indicators
        for indicator in strong_indicators:
            if indicator in content:
                score += 10
                found_indicators.append(indicator)
        
        # Check facility indicators
        for indicator in facility_indicators:
            if indicator in content:
                score += 5
                found_indicators.append(indicator)
        
        # Check weak indicators
        for indicator in weak_indicators:
            if indicator in content:
                score += 2
                found_indicators.append(indicator)
        
        # Determine if qualified
        if score >= 10:
            return True, f"Score: {score}, Indicators: {', '.join(found_indicators[:3])}"
        elif score >= 5:
            return None, f"Maybe - Score: {score}, Indicators: {', '.join(found_indicators[:3])}"
        else:
            return False, f"Low score: {score}, Limited ITAD evidence"
    
    def process_manual_review_leads(self):
        """Process leads that need manual review"""
        
        # Load the enrichment results
        with open('scripts/enrichment_results.json', 'r') as f:
            data = json.load(f)
        
        manual_review_leads = [lead for lead in data['results'] if lead['decision'] == 'manual_review']
        
        print(f"Analyzing {len(manual_review_leads)} leads requiring manual review...")
        
        results = []
        
        for lead in manual_review_leads:
            print(f"\n--- Analyzing {lead['name']} ---")
            
            website = lead['website']
            if not website:
                result = {
                    'id': lead['id'],
                    'name': lead['name'],
                    'decision': 'reject',
                    'reason': 'No website to analyze',
                    'score': 0
                }
                self.rejected_leads.append(result)
                results.append(result)
                continue
            
            # Get website content
            success, content, final_url = self.get_website_content(website)
            
            if not success:
                result = {
                    'id': lead['id'],
                    'name': lead['name'],
                    'decision': 'reject',
                    'reason': f'Website issue: {content}',
                    'score': 0
                }
                self.rejected_leads.append(result)
                results.append(result)
                continue
            
            # Analyze for ITAD services
            is_itad, analysis = self.analyze_itad_services(content, final_url)
            
            if is_itad is True:
                score = 70 + (len(analysis.split(',')) * 2)  # Base score + complexity
                result = {
                    'id': lead['id'],
                    'name': lead['name'],
                    'decision': 'qualified',
                    'reason': 'Verified ITAD processor',
                    'score': min(score, 85),  # Cap at 85
                    'analysis': analysis,
                    'website': final_url or website
                }
                self.qualified_leads.append(result)
                print(f"✅ QUALIFIED: {lead['name']} - {analysis}")
            
            elif is_itad is None:
                result = {
                    'id': lead['id'],
                    'name': lead['name'], 
                    'decision': 'maybe',
                    'reason': 'Partial ITAD indicators',
                    'score': 60,
                    'analysis': analysis,
                    'website': final_url or website
                }
                print(f"⚠️  MAYBE: {lead['name']} - {analysis}")
            
            else:
                result = {
                    'id': lead['id'],
                    'name': lead['name'],
                    'decision': 'reject',
                    'reason': 'Not ITAD processor',
                    'score': 0,
                    'analysis': analysis
                }
                self.rejected_leads.append(result)
                print(f"❌ REJECT: {lead['name']} - {analysis}")
            
            results.append(result)
            time.sleep(1)  # Be respectful to servers
        
        # Save detailed results
        with open('scripts/manual_review_results.json', 'w') as f:
            json.dump({
                'total_reviewed': len(manual_review_leads),
                'qualified': len(self.qualified_leads),
                'rejected': len(self.rejected_leads),
                'results': results,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f, indent=2)
        
        print(f"\n--- SUMMARY ---")
        print(f"Reviewed: {len(manual_review_leads)}")
        print(f"Qualified: {len(self.qualified_leads)}")
        print(f"Rejected: {len(self.rejected_leads)}")
        
        return results

if __name__ == "__main__":
    analyzer = ITADAnalyzer()
    analyzer.process_manual_review_leads()