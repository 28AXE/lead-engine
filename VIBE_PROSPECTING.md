# Vibe Prospecting Integration

**API Key:** `dbcde1a5-3ec4-463c-9c4f-03499ac9da7b`
**Provider:** Explorium
**Docs:** https://developers.explorium.ai/vibe-prospecting/

---

## Capabilities

### Data Coverage
- 150M+ Business Entities
- 800M+ Professional Profiles
- 4000+ Data Signals
- 50+ Data Sources

### Core Functions
1. **Company Search** — Find companies by name, domain, or attributes
2. **Contact Discovery** — Locate and enrich business contacts
3. **Lead List Building** — Create targeted lead lists
4. **Meeting Prep** — Get business and contact insights

---

## Filters Available (Natural Language)

| Filter | Example Query |
|--------|---------------|
| Job Title | "Find CTOs at fintech companies" |
| Location | "in San Francisco" |
| Company Size | "with 50-200 employees" |
| Industry | "SaaS companies" |
| Funding Events | "that raised funding in the last 90 days" |
| Technology | "that use Salesforce" |
| Team Changes | "companies that recently expanded their engineering teams" |

---

## Enrichment Options

| Enrichment | Data Returned |
|------------|---------------|
| `contacts` | Email addresses, phone numbers |
| `firmographics` | Basic company info |
| `technographics` | Full technology stack |
| `funding-and-acquisitions` | Investment history |

---

## Credit System

- Base fetch: ~1 credit per entity
- Enrichments: Additional credits per type
- Results capped at 1,000 per query

---

## Lead Engine Use Cases

### For Casinos
Query: "Online casinos launched in last 12 months with marketing teams"
Enrichment: contacts (for outreach), technographics (payment processors = crypto check)

### For Solar/Subsidized
Query: "Solar panel installation companies with 10-50 employees in France Germany UK"
Enrichment: contacts, firmographics

### For Restricted E-com
Query: "CBD vape supplement companies with online store"
Enrichment: contacts, technographics (Shopify = e-com signal)

### For Apps/SaaS
Query: "Gaming apps fintech apps that raised seed funding in last 6 months"
Enrichment: funding-and-acquisitions, contacts

---

## Next Steps

1. **Test API** — Run sample queries for each vertical
2. **Map fields** — Understand what data Vibe returns vs what we need for scoring
3. **Build scoring logic** — Translate Vibe data into our 40-point system
4. **Automate** — Set up recurring queries for new prospects

---

## Sources

- [Vibe Prospecting Main](https://www.vibeprospecting.ai/)
- [Developer Docs](https://developers.explorium.ai/vibe-prospecting/)
- [GitHub MCP](https://github.com/explorium-ai/vibeprospecting-mcp)
