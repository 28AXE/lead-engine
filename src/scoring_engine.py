#!/usr/bin/env python3
"""
Lead Engine — Scoring Engine
Transform raw prospect data → 40-point score → HOT/WARM/COLD verdict

Target Geos: UK, FR, BE, CA
Target Verticals: casino, solar, restricted_ecom, saas
"""

import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

# Hard disqualifiers
DISQUALIFIERS = {
    'max_domain_age_years': 3,
    'max_meta_ads': 100,
    'min_influencer_count': 1,  # 0 = no marketing DNA
}


def check_disqualifiers(prospect: Dict[str, Any]) -> Optional[str]:
    """Return disqualification reason if applicable, None otherwise."""

    # Domain age > 3 years
    domain_age_days = prospect.get('domain_age_days', 0)
    if domain_age_days > DISQUALIFIERS['max_domain_age_years'] * 365:
        return f"Domain too old ({domain_age_days // 365} years)"

    # Meta ads > 100
    meta_ads = prospect.get('meta_ads_count', 0)
    if meta_ads > DISQUALIFIERS['max_meta_ads']:
        return f"Too many Meta ads ({meta_ads})"

    # Zero influencers = no marketing DNA
    influencers = prospect.get('influencer_count', 0)
    if influencers < DISQUALIFIERS['min_influencer_count']:
        return "No influencer presence (no marketing DNA)"

    # Casino without license
    if prospect.get('vertical') == 'casino':
        if not prospect.get('has_gambling_license', False):
            return "Casino without valid license"

    # Blacklisted (Casino.guru complaints)
    if prospect.get('blacklisted', False):
        return "Blacklisted on Casino.guru/AskGamblers"

    return None


def score_domain_age(age_days: int) -> int:
    """Score domain age: 0-10 points"""
    if age_days < 90:       # < 3 months
        return 10
    elif age_days < 180:    # 3-6 months
        return 9
    elif age_days < 365:    # 6-12 months
        return 7
    elif age_days < 547:    # 12-18 months
        return 5
    elif age_days < 730:    # 18-24 months
        return 3
    elif age_days < 1095:   # 2-3 years
        return 2
    else:                   # > 3 years
        return 0


def score_meta_ads(ad_count: int) -> int:
    """Score Meta ad activity: 0-9 points"""
    if ad_count == 0:
        return 8   # Gap to exploit
    elif ad_count <= 10:
        return 9   # Testing phase
    elif ad_count <= 30:
        return 6   # Some presence
    elif ad_count <= 100:
        return 3   # Already invested
    else:
        return 0   # Too committed


def score_budget_signal(prospect: Dict[str, Any]) -> int:
    """Score budget signals: 0-9 points"""
    score = 0

    # Influencer presence (0-4 points)
    influencers = prospect.get('influencer_count', 0)
    if influencers >= 10:
        score += 4
    elif influencers >= 5:
        score += 3
    elif influencers >= 3:
        score += 2
    elif influencers >= 1:
        score += 1

    # Google Ads running (0-3 points)
    if prospect.get('google_ads_running', False):
        score += 3

    # Funding raised (0-2 points)
    if prospect.get('funding_raised', False):
        score += 2

    # Employee count 10-50 (0-2 points) - relevant for solar
    employee_count = prospect.get('employee_count', 0)
    if 10 <= employee_count <= 50:
        score += 2

    return min(score, 9)


def score_vertical_fit(prospect: Dict[str, Any]) -> int:
    """Score vertical fit: 0-10 points"""
    vertical = prospect.get('vertical', 'other')

    base_scores = {
        'casino': 8,
        'solar': 7,
        'restricted_ecom': 8,
        'saas': 6,
    }

    score = base_scores.get(vertical, 3)

    # Bonus: Crypto-friendly (casino, restricted_ecom)
    if vertical in ['casino', 'restricted_ecom']:
        if prospect.get('crypto_accepted', False):
            score += 2

    # Bonus: Certifications (solar)
    if vertical == 'solar':
        certs = prospect.get('certifications', [])
        if 'RGE' in certs or 'MCS' in certs or 'Certified' in str(certs):
            score += 2

    # Bonus: Tech stack signals
    tech_stack = prospect.get('tech_stack', [])
    if 'Shopify' in tech_stack:
        score += 1  # E-com = budget signal

    return min(score, 10)


def generate_hooks(prospect: Dict[str, Any], score_breakdown: Dict[str, int]) -> Dict[str, Any]:
    """Generate outreach hooks based on prospect data."""
    vertical = prospect.get('vertical', 'other')
    hooks = {
        'outreach_angle': '',
        'talking_points': []
    }

    # Primary angle based on vertical
    if vertical == 'casino':
        hooks['outreach_angle'] = "Competitor spy intel"
        hooks['talking_points'].append("I analyzed your competitors' Meta ad strategies")
    elif vertical == 'solar':
        hooks['outreach_angle'] = "Subsidy-driven demand on Meta"
        hooks['talking_points'].append("Government subsidies are driving 3x ROAS on Meta")
    elif vertical == 'restricted_ecom':
        hooks['outreach_angle'] = "Whitelisting + ad management"
        hooks['talking_points'].append("I specialize in getting restricted brands whitelisted")
    elif vertical == 'saas':
        hooks['outreach_angle'] = "CAC reduction vs Google Ads"
        hooks['talking_points'].append("Meta CAC is 30-50% lower than Google for your vertical")

    # Add specific talking points from score breakdown
    if score_breakdown.get('domain', 0) >= 9:
        hooks['talking_points'].append("Recently launched (urgent growth mode)")

    if prospect.get('meta_ads_count', 0) <= 10:
        hooks['talking_points'].append(f"Only {prospect.get('meta_ads_count', 0)} Meta ads — leaving money on the table")

    if prospect.get('influencer_count', 0) >= 5:
        hooks['talking_points'].append(f"{prospect.get('influencer_count', 0)} influencers promoting you — not retargeting on Meta")

    if prospect.get('crypto_accepted', False):
        hooks['talking_points'].append("Crypto-friendly (fast decisions, digital-native)")

    return hooks


def calculate_score(prospect: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate total score and verdict for a prospect.

    Returns:
        dict with total score, breakdown, verdict, and priority
    """

    # Check disqualifiers first
    disqualifier = check_disqualifiers(prospect)
    if disqualifier:
        return {
            'total': 0,
            'max': 40,
            'verdict': 'DISQUALIFY',
            'priority': 'Remove',
            'reason': disqualifier,
            'breakdown': {
                'domain': 0,
                'meta': 0,
                'budget': 0,
                'vertical': 0
            }
        }

    # Calculate individual scores
    domain_score = score_domain_age(prospect.get('domain_age_days', 0))
    meta_score = score_meta_ads(prospect.get('meta_ads_count', 0))
    budget_score = score_budget_signal(prospect)
    vertical_score = score_vertical_fit(prospect)

    total = domain_score + meta_score + budget_score + vertical_score

    # Determine verdict
    if total >= 30:
        verdict = 'HOT'
        priority = '24h'
    elif total >= 22:
        verdict = 'WARM'
        priority = '1 week'
    elif total >= 15:
        verdict = 'COLD'
        priority = '30 days'
    else:
        verdict = 'DISQUALIFY'
        priority = 'Remove'

    # Generate hooks
    hooks = generate_hooks(prospect, {
        'domain': domain_score,
        'meta': meta_score,
        'budget': budget_score,
        'vertical': vertical_score
    })

    return {
        'total': total,
        'max': 40,
        'breakdown': {
            'domain': domain_score,
            'meta': meta_score,
            'budget': budget_score,
            'vertical': vertical_score
        },
        'verdict': verdict,
        'priority': priority,
        'hooks': hooks
    }


def process_prospects(prospects: list) -> list:
    """Process a batch of prospects and return scored results."""
    results = []

    for prospect in prospects:
        score_result = calculate_score(prospect)
        result = {
            'prospect': {
                'name': prospect.get('name', 'Unknown'),
                'domain': prospect.get('domain', 'unknown.com'),
                'vertical': prospect.get('vertical', 'other'),
                'geo': prospect.get('geo', 'Unknown')
            },
            'score': score_result
        }
        results.append(result)

    # Sort by score descending
    results.sort(key=lambda x: x['score']['total'], reverse=True)

    return results


# Demo / Test mode
if __name__ == '__main__':
    # Test prospects
    test_prospects = [
        {
            'name': 'Degen Casino',
            'domain': 'degen.com',
            'vertical': 'casino',
            'geo': 'UK',
            'domain_age_days': 120,  # 4 months
            'meta_ads_count': 5,
            'influencer_count': 6,
            'crypto_accepted': True,
            'has_gambling_license': True,
            'google_ads_running': True,
            'tech_stack': ['Shopify', 'Bitcoin']
        },
        {
            'name': 'SolarTech France',
            'domain': 'solartech.fr',
            'vertical': 'solar',
            'geo': 'FR',
            'domain_age_days': 400,  # ~13 months
            'meta_ads_count': 0,
            'influencer_count': 2,
            'employee_count': 25,
            'certifications': ['RGE'],
            'google_ads_running': True,
        },
        {
            'name': 'CBD Store',
            'domain': 'cbdstore.ca',
            'vertical': 'restricted_ecom',
            'geo': 'CA',
            'domain_age_days': 200,
            'meta_ads_count': 15,
            'influencer_count': 4,
            'crypto_accepted': True,
            'tech_stack': ['Shopify'],
        },
        {
            'name': 'Old Casino',
            'domain': 'oldcasino.com',
            'vertical': 'casino',
            'geo': 'UK',
            'domain_age_days': 1500,  # ~4 years - DISQUALIFY
            'meta_ads_count': 5,
            'influencer_count': 3,
        },
    ]

    print("=" * 60)
    print("LEAD ENGINE — SCORING RESULTS")
    print("=" * 60)

    results = process_prospects(test_prospects)

    for result in results:
        prospect = result['prospect']
        score = result['score']

        print(f"\n{prospect['name']} ({prospect['domain']})")
        print(f"  Vertical: {prospect['vertical']} | Geo: {prospect['geo']}")
        print(f"  Score: {score['total']}/{score['max']}")
        print(f"  Breakdown: Domain={score['breakdown']['domain']}, Meta={score['breakdown']['meta']}, Budget={score['breakdown']['budget']}, Vertical={score['breakdown']['vertical']}")
        print(f"  Verdict: {score['verdict']} (Priority: {score['priority']})")

        if score.get('hooks'):
            print(f"  Hook: {score['hooks']['outreach_angle']}")
            for point in score['hooks']['talking_points']:
                print(f"    • {point}")

        if score.get('reason'):
            print(f"  ❌ Disqualified: {score['reason']}")

    print("\n" + "=" * 60)
    print(f"Total prospects: {len(results)}")
    print(f"HOT: {sum(1 for r in results if r['score']['verdict'] == 'HOT')}")
    print(f"WARM: {sum(1 for r in results if r['score']['verdict'] == 'WARM')}")
    print(f"COLD: {sum(1 for r in results if r['score']['verdict'] == 'COLD')}")
    print(f"DISQUALIFY: {sum(1 for r in results if r['score']['verdict'] == 'DISQUALIFY')}")
