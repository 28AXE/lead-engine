# Scoring Engine — Specification

**Last Updated:** 2026-04-28
**Target Geos:** UK, FR, BE, CA

---

## Overview

Transform raw prospect data → 40-point score → HOT/WARM/COLD verdict

---

## Input Schema (Per Prospect)

```json
{
  "name": "Casino Name",
  "domain": "example.com",
  "vertical": "casino | solar | restricted_ecom | saas",
  "geo": "UK | FR | BE | CA",
  
  // Raw data from APIs
  "domain_age_days": 180,
  "meta_ads_count": 5,
  "influencer_count": 4,
  "crypto_accepted": true,
  "google_ads_running": true,
  "funding_raised": false,
  "employee_count": 25,
  "certifications": ["RGE", "MCS"],
  "tech_stack": ["Shopify", "Bitcoin", "Klaviyo"]
}
```

---

## Scoring Functions

### 1. Domain Age Score (0-10 points)

```python
def score_domain_age(age_days):
    if age_days < 90:      # < 3 months
        return 10
    elif age_days < 180:   # 3-6 months
        return 9
    elif age_days < 365:   # 6-12 months
        return 7
    elif age_days < 547:   # 12-18 months
        return 5
    elif age_days < 730:   # 18-24 months
        return 3
    elif age_days < 1095:  # 2-3 years
        return 2
    else:                  # > 3 years
        return 0
```

### 2. Meta Ad Activity Score (0-9 points)

```python
def score_meta_ads(ad_count):
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
```

### 3. Budget Signal Score (0-9 points)

```python
def score_budget_signal(prospect):
    score = 0
    
    # Influencer presence
    if prospect['influencer_count'] >= 10:
        score += 4
    elif prospect['influencer_count'] >= 5:
        score += 3
    elif prospect['influencer_count'] >= 3:
        score += 2
    elif prospect['influencer_count'] >= 1:
        score += 1
    
    # Google Ads running
    if prospect['google_ads_running']:
        score += 3
    
    # Funding raised (SaaS vertical)
    if prospect['funding_raised']:
        score += 2
    
    # Employee count (solar/subsidized)
    if 10 <= prospect['employee_count'] <= 50:
        score += 2
    
    return min(score, 9)  # Cap at 9
```

### 4. Vertical Fit Score (0-10 points)

```python
def score_vertical_fit(prospect):
    vertical = prospect['vertical']
    
    base_scores = {
        'casino': 8,
        'solar': 7,
        'restricted_ecom': 8,
        'saas': 6,
        'other': 3
    }
    
    score = base_scores.get(vertical, 3)
    
    # Bonus: Crypto-friendly (casino, ecom)
    if vertical in ['casino', 'restricted_ecom']:
        if prospect['crypto_accepted']:
            score += 2
    
    # Bonus: Certifications (solar)
    if vertical == 'solar':
        if 'RGE' in prospect['certifications'] or 'MCS' in prospect['certifications']:
            score += 2
    
    # Bonus: Tech stack signals
    if 'Shopify' in prospect['tech_stack']:
        score += 1  # E-com = budget signal
    
    return min(score, 10)  # Cap at 10
```

---

## Total Score & Verdict

```python
def calculate_score(prospect):
    domain_score = score_domain_age(prospect['domain_age_days'])
    meta_score = score_meta_ads(prospect['meta_ads_count'])
    budget_score = score_budget_signal(prospect)
    vertical_score = score_vertical_fit(prospect)
    
    total = domain_score + meta_score + budget_score + vertical_score
    
    if total >= 30:
        verdict = "HOT"
        priority = "24h"
    elif total >= 22:
        verdict = "WARM"
        priority = "1 week"
    elif total >= 15:
        verdict = "COLD"
        priority = "30 days"
    else:
        verdict = "DISQUALIFY"
        priority = "Remove"
    
    return {
        "total": total,
        "max": 40,
        "breakdown": {
            "domain": domain_score,
            "meta": meta_score,
            "budget": budget_score,
            "vertical": vertical_score
        },
        "verdict": verdict,
        "priority": priority
    }
```

---

## Disqualifiers (Hard Rules)

Apply BEFORE scoring:

| Condition | Action |
|-----------|--------|
| Domain age > 3 years | ❌ Disqualify |
| Meta ads > 100 | ❌ Disqualify |
| Influencer count = 0 | ❌ Disqualify (no marketing DNA) |
| Casino without license | ❌ Disqualify |
| Blacklisted (Casino.guru) | ❌ Disqualify |

---

## Output Format

```json
{
  "prospect": {
    "name": "Example Casino",
    "domain": "example.com",
    "vertical": "casino",
    "geo": "UK"
  },
  "score": {
    "total": 32,
    "max": 40,
    "breakdown": {
      "domain": 9,
      "meta": 9,
      "budget": 7,
      "vertical": 7
    },
    "verdict": "HOT",
    "priority": "24h"
  },
  "hooks": {
    "outreach_angle": "Competitor intel",
    "talking_points": [
      "3+ influencers active",
      "Only 5 Meta ads (competitor X has 50+)",
      "Crypto-friendly, UK geo"
    ]
  },
  "data_sources": {
    "domain": "WhoisXML",
    "ads": "Meta Ad Library",
    "influencers": "Manual/Vibe",
    "crypto": "Site check"
  }
}
```

---

## Implementation Plan

| Step | Task | Tools |
|------|------|-------|
| 1 | Build Python scoring module | Pure Python |
| 2 | Integrate WhoisXML API | `requests` |
| 3 | Integrate Meta Ad Library | `requests` or AdLibrary.com SDK |
| 4 | Integrate Vibe Prospecting | MCP or direct API |
| 5 | Build batch processor | Process 100+ prospects |
| 6 | Export to CSV/JSON | For closers |

---

## Notes for AI Continuation

- Scoring logic is the CORE IP — keep it sharp, iterate on conversion data
- Disqualifiers are hard rules — don't waste time on bad leads
- Output format designed for closer handoff
- Geo filtering: UK, FR, BE, CA only
- Verticals: casino (core), solar (high-ticket), restricted_ecom (whitelisting), saas (performance)
