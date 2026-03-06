#!/usr/bin/env python3
"""
Data enrichment script for processing 150 unverified leads
Verifies ITAD capabilities and updates lead status
"""

import json
import time
import requests
from urllib.parse import urlparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LeadEnricher:
    def __init__(self):
        self.qualified_count = 0
        self.rejected_count = 0
        self.processed_count = 0
        self.qualified_leads = []
        self.rejected_leads = []
        
    def check_website(self, url):
        """Check if website exists and is accessible"""
        if not url or url.strip() == "":
            return False, "No website provided"
        
        try:
            # Clean up URL
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                return True, "Website accessible"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, f"Website error: {str(e)[:50]}"
    
    def analyze_itad_potential(self, lead):
        """Analyze if lead is potentially a genuine ITAD processor"""
        name = lead.get('name', '').lower()
        industry = lead.get('industry', '').lower()
        website = lead.get('website', '')
        
        # Red flags - likely NOT ITAD processors
        red_flags = [
            'broker', 'trading', 'distribution', 'epos', 'retail', 'sales',
            'consultant', 'advisory', 'software', 'development', 'marketing'
        ]
        
        # ITAD indicators
        itad_keywords = [
            'recycling', 'disposal', 'asset', 'weee', 'erasure', 'destruction',
            'refurb', 'remarketing', 'recovery', 'processing'
        ]
        
        # Check for red flags
        for flag in red_flags:
            if flag in name or flag in industry:
                return False, f"Red flag: {flag}"
        
        # Check for ITAD indicators
        for keyword in itad_keywords:
            if keyword in name:
                return True, f"ITAD indicator: {keyword}"
        
        return None, "Manual review needed"
    
    def process_lead(self, lead):
        """Process a single lead"""
        lead_id = lead['id']
        name = lead['name']
        website = lead.get('website', '')
        
        logging.info(f"Processing {lead_id}: {name}")
        
        # Check website accessibility
        website_ok, website_status = self.check_website(website)
        
        # Analyze ITAD potential
        itad_potential, analysis = self.analyze_itad_potential(lead)
        
        # Make decision
        if not website_ok:
            decision = 'reject'
            reason = f"Website issue: {website_status}"
            score = None
        elif itad_potential is False:
            decision = 'reject'
            reason = analysis
            score = None
        else:
            # For this batch run, I'll mark potential ITADs for manual review
            decision = 'manual_review'
            reason = analysis
            score = None
        
        # Update lead data
        result = {
            'id': lead_id,
            'name': name,
            'website': website,
            'decision': decision,
            'reason': reason,
            'score': score,
            'original_industry': lead.get('industry'),
            'analysis': analysis
        }
        
        if decision == 'reject':
            self.rejected_leads.append(result)
            self.rejected_count += 1
        else:
            # For manual review leads, we'll process them separately
            pass
            
        self.processed_count += 1
        
        return result
    
    def process_batch(self):
        """Process the extracted batch of leads"""
        # Load the extracted batch
        with open('scripts/unverified_batch.json', 'r', encoding='utf-8') as f:
            leads = json.load(f)
        
        results = []
        
        for i, lead in enumerate(leads[:50]):  # Start with first 50
            try:
                result = self.process_lead(lead)
                results.append(result)
                
                # Brief pause to avoid overwhelming servers
                time.sleep(0.5)
                
                if (i + 1) % 10 == 0:
                    logging.info(f"Processed {i + 1}/{len(leads)} leads")
                    
            except Exception as e:
                logging.error(f"Error processing {lead['id']}: {e}")
        
        # Save results
        with open('scripts/enrichment_results.json', 'w', encoding='utf-8') as f:
            json.dump({
                'processed': self.processed_count,
                'qualified': self.qualified_count,
                'rejected': self.rejected_count,
                'results': results,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f, indent=2)
        
        logging.info(f"Batch complete: {self.processed_count} processed, {self.rejected_count} rejected")
        return results

if __name__ == "__main__":
    enricher = LeadEnricher()
    enricher.process_batch()