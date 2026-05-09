# Lead Engine

[![Stars](https://img.shields.io/github/stars/28AXE/lead-engine?style=flat)](https://github.com/28AXE/lead-engine)
[![Forks](https://img.shields.io/github/forks/28AXE/lead-engine?style=flat)](https://github.com/28AXE/lead-engine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

[![GitHub Topics](https://img.shields.io/badge/topics-lead--generation%20%7C%20b2b%20%7C%20sales%20%7C%20automation-blue)](https://github.com/28AXE/lead-engine)

<p align="center">
  <strong>🎯 Automated B2B lead generation with multi-signal scoring</strong><br>
  Find, enrich, and score qualified prospects from 9+ data sources
</p>

Lead Engine identifies qualified leads by combining multiple data sources (APIs, scrapers, public databases), enriches them with contact info, scores them using a configurable 40-point algorithm, and notifies your team instantly when HOT prospects are detected.

---

## Demo

```
╔════════════════════════════════════════╗
║     ███╗   ██╗ █████╗  ██████╗██╗  ██╗║
║     ████╗  ██║██╔══██╗██╔════╝██║  ██║║
║     ██╔██╗ ██║███████║██║     ███████║║
║     ██║╚██╗██║██╔══██║██║     ██╔══██║║
║     ██║ ╚████║██║  ██║╚██████╗██║  ██║║
║     ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝║
║          E N G I N E                   ║
╚════════════════════════════════════════╝

ℹ Loading configuration: config/vertical.config.yaml
✓ Vertical: plomberie — Plombiers et chauffagistes locaux France
ℹ Geos: FR, BE | Keywords: plombier, chauffagiste, sanitaire

==================================================
STEP 1: SOURCING
==================================================
⠋ Sourcing via vibe_api...
✓ Found 3 prospects via vibe_api
⠋ Sourcing via google_maps...
✓ Found 3 prospects via google_maps
ℹ Total prospects sourced: 6

==================================================
STEP 2: ENRICHMENT
==================================================
✓ Enriched 6 leads

==================================================
STEP 3: SCORING
==================================================
✓ Scored 6 leads

==================================================
STEP 4: PIPELINE TRACKING
==================================================
✓ Added 6 leads to pipeline

==================================================
STEP 5: NOTIFICATIONS
==================================================
⚠ 2 HOT leads detected!
✓ Notified: Artisan Plomberie Services

==================================================
STEP 6: EXPORT
==================================================
✓ Exported 6 leads to CSV: outputs/leads_export.csv
✓ Generated HTML report: outputs/report_2026-05-01_14-30.html

==================================================
RESULTS
==================================================
┌────────────────────────────────────────────────────────────────────┐
│                         Leads — plomberie                          │
├──────────────┬──────────────┬───────┬──────────┬─────────┬────────┤
│    Nom       │   Domaine    │ Score │ Verdict  │  Email  │Signaux │
├──────────────┼──────────────┼───────┼──────────┼─────────┼────────┤
│ Artisan...   │ artisan-...  │  35   │ 🔥 HOT   │ contact │ google │
│ EcoChauf...  │ ecochauf...  │  28   │ 🟡 WARM  │ -       │ pappers│
└──────────────┴──────────────┴───────┴──────────┴─────────┴────────┘

✓ 6 leads analysés — 2 HOT 🔥 — 3 WARM 🟡 — durée : 4.2s

✓ Pipeline completed successfully!
```

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/nima/lead-engine.git
cd lead-engine

# 2. Install
pip install -r requirements.txt

# 3. Configure API keys
cp .env.example .env
# Edit .env with your API keys

# 4. Test run (no API calls)
python -m src.main --dry-run

# 5. Production run
python -m src.main
```

---

## Changer de Vertical en 3 Étapes

Lead Engine est conçu pour être agnostique au vertical. Changez de cible sans toucher au code :

### Étape 1 : Copier la config
```bash
cp config/vertical.config.yaml config/verticals/casinos.yaml
```

### Étape 2 : Modifier les paramètres
```yaml
vertical: "casinos"
description: "Online casinos & betting sites"
geo: ["UK", "MT", "CY"]
keywords: ["online casino", "sports betting", "live dealer"]
signals: ["vibe_api", "apify_instagram"]
```

### Étape 3 : Lancer
```bash
python -m src.main --vertical casinos
```

---

## Signaux Disponibles

| Signal | Type | Description | Meilleur pour |
|--------|------|-------------|---------------|
| `vibe_api` | Sourcing | Explorium B2B database (50M+ companies) | SaaS, Tech, B2B services |
| `google_maps` | Sourcing | Google Places API | Commerces locaux, artisans |
| `apify_instagram` | Sourcing | Instagram influencer detection | D2C, lifestyle, e-commerce |
| `whoisxml` | Enrichment | Domain age & ownership | Tous verticaux |
| `hunter_io` | Enrichment | Email discovery | B2B, decision makers |
| `pappers` | Enrichment | French company registry (INPI) | France uniquement |
| `meta_ad_library` | Signal | Meta/Facebook ad activity | E-commerce, D2C |
| `google_ads_transparency` | Signal | Google Ads spend detection | Tous verticaux |
| `linkedin_jobs` | Signal | Hiring signals (growth detection) | SaaS, scale-ups |

---

## Configuration Examples

### Plomberie / Artisans locaux
```yaml
vertical: "plomberie"
geo: ["FR", "BE"]
keywords: ["plombier", "chauffagiste", "sanitaire"]
signals: ["google_maps", "pappers"]
scoring_weights:
  domain_age: 10
  ad_activity: 9
  budget_signal: 9
  vertical_fit: 12
```

### SaaS / Tech B2B
```yaml
vertical: "saas"
geo: ["US", "UK", "DE"]
keywords: ["SaaS", "B2B software", "enterprise platform"]
signals: ["vibe_api", "linkedin_jobs"]
scoring_weights:
  domain_age: 8
  ad_activity: 10
  budget_signal: 12
  vertical_fit: 10
```

### E-commerce Restreint
```yaml
vertical: "restricted_ecom"
geo: ["UK", "MT"]
keywords: ["CBD", "vape", "supplements", "crypto casino"]
signals: ["vibe_api", "meta_ad_library", "apify_instagram"]
scoring_weights:
  domain_age: 12
  ad_activity: 10
  budget_signal: 10
  vertical_fit: 8
```

### Agence Media / Marketing
```yaml
vertical: "agence_media"
geo: ["FR"]
keywords: ["agence digitale", "marketing digital", "publicité en ligne"]
signals: ["vibe_api", "pappers", "meta_ad_library"]
scoring_weights:
  domain_age: 6
  ad_activity: 12
  budget_signal: 12
  vertical_fit: 10
```

---

## Roadmap

| Priority | Feature | Status |
|----------|---------|--------|
| P0 | Complete API integrations (all stubs) | 🔄 In Progress |
| P0 | Add unit tests for all providers | ⏳ Pending |
| P1 | Outreach template generator | ⏳ Pending |
| P1 | CRM integrations (HubSpot, Pipedrive) | ⏳ Pending |
| P2 | Auto-pilot mode (daily scheduled runs) | ⏳ Pending |
| P2 | A/B test outreach hooks | ⏳ Pending |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

**Built with ❤️ by Lead Engine Team**
