# Lead Engine — Data Sources & Tools

**Last Updated:** 2026-04-28

---

## 1. Vibe Prospecting (Explorium)

**Status:** ✅ API Key configured
**Key:** `dbcde1a5-3ec4-463c-9c4f-03499ac9da7b`
**Docs:** https://developers.explorium.ai/vibe-prospecting/

### Usage
- Primary sourcing tool for all verticals
- Natural language queries
- Enrichment: contacts, firmographics, technographics, funding

### Sample Queries by Vertical

| Vertical | Query |
|----------|-------|
| Casinos | "online casinos launched in last 12 months with marketing teams" |
| Solar | "solar panel installation companies 10-50 employees France Germany UK" |
| CBD/E-com | "CBD vape supplement companies with online store" |
| SaaS | "gaming apps fintech apps raised seed funding last 6 months" |

---

## 2. Facebook Ad Library

**Status:** ⚠️ Requires identity verification + app review (can take days/weeks)
**URL:** https://www.facebook.com/ads/library/api/
**Docs:** https://developers.facebook.com/docs/graph-api/reference/ads_archive/

### Official API Access Steps
1. **Identity verification** — https://www.facebook.com/ID (required for political/issue ads)
2. **Create Meta Developer App** — https://developers.facebook.com/
3. **Generate Access Token** — Graph API Explorer
4. **App Review** — Can take days to weeks

### API Limitations
| Region | Data Available |
|--------|---------------|
| Political/Issue Ads (Global) | 7 years |
| EU/UK (All Ads) | 1 year (per Digital Services Act) |
| General Commercial (Non-EU) | Limited |

**Rate Limit:** 200 calls/hour

### Alternative: Third-Party APIs
| Provider | URL | Notes |
|----------|-----|-------|
| **AdLibrary.com** | https://www.adlibrary.com/ | All commercial ads, simpler auth, multi-platform |

### Recommendation
- **MVP:** Use third-party (AdLibrary.com) for speed
- **Long-term:** Official API for compliance + cost savings

### Data Needed Per Prospect
- Company name / Page name
- Number of active ads
- Ad creatives (images, videos, copy)
- Run dates (start date, still active Y/N)
- Platforms (FB, IG, Audience Network)
- Estimated impressions (if available)

### Scoring Integration
| Active Ads | Score |
|------------|-------|
| 0 | 8 |
| 1-10 | 9 |
| 11-30 | 6 |
| 31-100 | 3 |
| 100+ | 0 |

---

## 3. Domain Age / Whois

**Status:** ⚠️ Need to select API

### Options

| Service | API | Cost | Speed | Notes |
|---------|-----|------|-------|-------|
| **WhoisXML API** | ✅ REST | Free tier (500/mo) | Fast | Reliable, structured JSON |
| **DomainTools** | ✅ REST | $$$ | Fast | Enterprise grade |
| **WhoisFreaks** | ✅ REST | Free tier | Fast | Good coverage |
| **Python `python-whois`** | ❌ Library | Free | Medium | Self-hosted, rate limit aware |

### Recommendation
Start with **WhoisXML API** (free tier: 500 credits with business email)
- Endpoint: `https://whois.whoisxmlapi.com/services/whois-server`
- Returns: `createdDate`, `updatedDate`, `expiresDate`
- Domain age calculation: `today - createdDate`
- Signup: https://drs.whoisxmlapi.com/signup (use business email for full 500 credits)

### Scoring Integration
| Domain Age | Score |
|------------|-------|
| < 3 months | 10 |
| 3-6 months | 9 |
| 6-12 months | 7 |
| 12-18 months | 5 |
| 18-24 months | 3 |
| 2-3 years | 2 |
| > 3 years | 0 |

---

## 4. Casino-Specific Sources

**Status:** ✅ Public (no auth)

| Source | URL | Data |
|--------|-----|------|
| **Casino.guru** | https://casino.guru/new-casinos | New casinos, ratings, complaints |
| **AskGamblers** | https://www.askgamblers.com/new-casinos | New casinos, player reviews |
| **LCB.org** | https://lcb.org/new-casinos | Casino forum, launch dates |

### Scrape Targets
- Casino name
- Launch date
- License info
- Crypto acceptance (BTC, ETH, USDT)
- Sister sites
- Complaints/red flags

---

## 5. Influencer Presence Check

**Status:** ⚠️ Need to determine method

### Options

| Method | Pros | Cons |
|--------|------|------|
| **Manual search** | Free, accurate | Not scalable |
| **Social Blade API** | ✅ API, influencer stats | Limited search, need username |
| **HypeAuditor** | ✅ API, discovery | $$$ |
| **Moda / InfluencerDB** | ✅ API | $$$ |
| **YouTube/Twitch search** | Free | Rate limits, scraping needed |

### MVP Approach
1. Use Vibe Prospecting `technographics` to detect if company runs influencer campaigns
2. Manual check for top prospects (before outreach)
3. Later: integrate Social Blade API for scale

### Scoring Integration
| Influencer Count | Score |
|------------------|-------|
| 10+ | 9 |
| 5-9 | 8 |
| 3-4 | 7 |
| 1-2 | 5 |
| 0 | 0 (disqualify) |

---

## 6. Additional Enrichment Tools

### For Solar/Subsidized Vertical
| Tool | Purpose |
|------|---------|
| **LinkedIn Company Search** | Company age, employee count, hiring signals |
| **Google Ads Transparency Center** | Check if running Google Ads (budget signal) |
| **RGE Certified List (FR)** | https://france-renov.gouv.fr — official certified installers |
| **MCS Certified List (UK)** | https://www.microgenerationcertification.org |

### For E-com / Restricted Vertical
| Tool | Purpose |
|------|---------|
| **BuiltWith** | Tech stack, e-com platform |
| **Shopify Exchange** | For sale = potential acquisition target |
| **Reddit r/PPC, r/ecommerce** | Find brands complaining about ad bans |

### For SaaS/Apps
| Tool | Purpose |
|------|---------|
| **Crunchbase API** | Funding rounds, investors |
| **Product Hunt** | Launch date, traction signals |
| **App Store / Google Play** | App rankings, reviews |

---

## Tool Priority for MVP

| Priority | Tool | Why |
|----------|------|-----|
| P0 | Vibe Prospecting | ✅ Already have API key, covers sourcing + enrichment |
| P1 | Facebook Ad Library API | Critical for scoring (Meta ad activity) |
| P2 | WhoisXML API | Domain age = key scoring factor |
| P3 | Casino.guru scraper | Casino-specific sourcing |
| P4 | Social Blade / influencer tool | Budget signal verification |

---

## Next Steps

1. **Test Facebook Ad Library API** — Set up app, get access token, test queries
2. **Get WhoisXML API key** — Free tier signup
3. **Run Vibe Prospecting test queries** — Validate data quality per vertical
4. **Build scoring function** — Translate raw data → 40-point score
5. **Create prospect output format** — JSON/CSV for closers

---

## Notes for AI Continuation

- All tools documented with priority order
- Facebook Ad Library and WhoisXML need API setup
- Casino sources are public (no auth needed)
- Influencer detection is the weakest link — may need manual step for MVP
- Scoring logic is defined in PROSPECT_CRITERIA.md
