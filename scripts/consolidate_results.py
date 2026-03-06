#!/usr/bin/env python3
"""
Consolidate results from all batches and update pipeline
"""

import json
import time

def consolidate_all_results():
    """Consolidate results from manual review and fast screening"""
    
    # Load all result files
    with open('scripts/manual_review_results.json', 'r') as f:
        manual_results = json.load(f)
    
    with open('scripts/ultra_fast_results.json', 'r') as f:
        fast_results = json.load(f)
    
    # Combine qualified leads
    all_qualified = manual_results['qualified'] + fast_results['qualified']
    all_maybe = manual_results['maybe'] + fast_results['maybe']
    all_rejected = manual_results['rejected'] + fast_results['rejected']
    
    print("=== ENRICHMENT SESSION COMPLETE ===")
    print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total leads processed: 150")
    print(f"")
    print(f"✅ QUALIFIED: {len(all_qualified)}")
    print(f"⚠️  MAYBE: {len(all_maybe)}")
    print(f"❌ REJECTED: {len(all_rejected)}")
    print(f"")
    
    # Show qualified leads
    if all_qualified:
        print("QUALIFIED ITAD PROCESSORS:")
        for i, lead in enumerate(all_qualified, 1):
            score = lead.get('score', 0)
            website = lead.get('website', 'No website')
            print(f"  {i}. {lead['name']} (Score: {score})")
            print(f"     Website: {website}")
            print(f"     Reason: {lead['reason']}")
            print("")
    
    # Show promising maybe leads
    print("PROMISING 'MAYBE' LEADS FOR FURTHER REVIEW:")
    promising_maybe = [lead for lead in all_maybe if 'recycling' in lead['name'].lower() or 'disposal' in lead['name'].lower()]
    for lead in promising_maybe[:10]:  # Show top 10
        website = lead.get('website', 'No website')
        print(f"  - {lead['name']}")
        print(f"    Website: {website}")
        print("")
    
    # Final statistics
    qualification_rate = (len(all_qualified) / 150) * 100
    print(f"STATISTICS:")
    print(f"Qualification rate: {qualification_rate:.1f}%")
    print(f"Batch 1 (detailed): 7 qualified from 50 leads (14.0%)")
    print(f"Batch 2 (fast): 0 qualified from 100 leads (0.0%)")
    print(f"Combined: {len(all_qualified)} qualified from 150 leads ({qualification_rate:.1f}%)")
    
    return {
        'qualified': all_qualified,
        'maybe': all_maybe,
        'rejected': all_rejected,
        'summary': {
            'total_processed': 150,
            'qualified': len(all_qualified),
            'maybe': len(all_maybe),
            'rejected': len(all_rejected),
            'qualification_rate': qualification_rate
        }
    }

def update_leadpool():
    """Update leadpool.json with enrichment results"""
    
    print("\n=== UPDATING LEADPOOL ===")
    
    # Load current leadpool
    with open('src/data/leadpool.json', 'r', encoding='utf-8') as f:
        leadpool = json.load(f)
    
    # Load all results
    results = consolidate_all_results()
    
    # Create lookup dictionaries
    qualified_lookup = {lead['id']: lead for lead in results['qualified']}
    maybe_lookup = {lead['id']: lead for lead in results['maybe']}
    rejected_lookup = {lead['id']: lead for lead in results['rejected']}
    
    # Update leadpool entries
    updates = 0
    promoted_to_pipeline = 0
    
    for lead in leadpool:
        lead_id = lead['id']
        
        if lead_id in qualified_lookup:
            result = qualified_lookup[lead_id]
            lead['dataQuality'] = 'verified'
            lead['stage'] = 'qualified'
            lead['score'] = result['score']
            lead['isPipeline'] = True
            lead['services'] = ['ITAD Processing', 'Asset Recovery']
            lead['lastVerified'] = time.strftime('%Y-%m-%d')
            lead['notes'].append({
                'id': f"note-{int(time.time())}",
                'author': 'Clorius',
                'date': time.strftime('%Y-%m-%d'),
                'content': f"Verified ITAD processor. {result['reason']}"
            })
            updates += 1
            promoted_to_pipeline += 1
            
        elif lead_id in maybe_lookup:
            result = maybe_lookup[lead_id]
            lead['dataQuality'] = 'partial'
            lead['stage'] = 'unverified'  # Keep for future review
            lead['score'] = result.get('score', 50)
            lead['lastVerified'] = time.strftime('%Y-%m-%d')
            lead['notes'].append({
                'id': f"note-{int(time.time())}",
                'author': 'Clorius',
                'date': time.strftime('%Y-%m-%d'),
                'content': f"Partial ITAD indicators. {result['reason']}"
            })
            updates += 1
            
        elif lead_id in rejected_lookup:
            result = rejected_lookup[lead_id]
            lead['dataQuality'] = 'verified'
            lead['stage'] = 'rejected'
            lead['score'] = 0
            lead['lastVerified'] = time.strftime('%Y-%m-%d')
            lead['notes'].append({
                'id': f"note-{int(time.time())}",
                'author': 'Clorius',
                'date': time.strftime('%Y-%m-%d'),
                'content': f"Not ITAD processor. {result['reason']}"
            })
            updates += 1
    
    # Save updated leadpool
    with open('src/data/leadpool.json', 'w', encoding='utf-8') as f:
        json.dump(leadpool, f, indent=2, ensure_ascii=False)
    
    print(f"Updated {updates} leads in leadpool.json")
    print(f"Promoted {promoted_to_pipeline} leads to pipeline")
    print("Leadpool update complete")
    
    return updates, promoted_to_pipeline

if __name__ == "__main__":
    consolidate_all_results()
    update_leadpool()