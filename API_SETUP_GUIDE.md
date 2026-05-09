# API Setup Guide — Step by Step

**Last Updated:** 2026-04-28

---

## 1. WhoisXML API — Signup Guide

**URL:** https://drs.whoisxmlapi.com/signup
**Time:** 2-3 minutes
**Free Tier:** 500 credits (one-time, no credit card)

### Steps

1. **Go to signup page**
   - URL: https://drs.whoisxmlapi.com/signup

2. **Choose signup method**
   - Sign up with Google (recommended)
   - Sign up with Microsoft
   - Sign up with Email

3. **⚠️ CRITICAL: Use a BUSINESS EMAIL**
   - ✅ GOOD: `you@yourcompany.com`, `contact@yourdomain.com`
   - ❌ BAD: `@gmail.com`, `@yahoo.com`, `@protonmail.com`
   - Why: Business emails get 500 credits, personal emails get only 50 credits

4. **Fill in registration form**
   - First Name
   - Last Name
   - Business Email
   - Company Name
   - Password

5. **Verify email**
   - Check inbox for confirmation link
   - Click to activate account

6. **Get API Key**
   - Login to dashboard: https://whois.whoisxmlapi.com/user/login
   - Go to "API Keys" or "Account Settings"
   - Copy your API key (looks like: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

7. **Test the API**
   ```bash
   curl "https://whois.whoisxmlapi.com/services/whois-server?apiKey=YOUR_API_KEY&domainName=google.com"
   ```

8. **Save key to CONFIG.md**
   - Open `/home/nima/lead-engine/CONFIG.md`
   - Add under "WhoisXML API" section

### Expected Response Format
```json
{
  "WhoisRecord": {
    "createdDate": "1997-09-15",
    "updatedDate": "2024-08-15",
    "expiresDate": "2028-09-14",
    "domainName": "google.com"
  }
}
```

---

## 2. Meta Ad Library API — Two Options

### Option A: Official Meta API (Free, Slow)

**Time:** 1-3 weeks for approval
**Cost:** Free
**Limits:** 200 calls/hour

#### Steps

1. **Identity Verification**
   - Go to: https://www.facebook.com/ID
   - Upload government ID
   - Wait 1-3 days for approval

2. **Create Meta Developer Account**
   - Go to: https://developers.facebook.com/
   - Click "Get Started"
   - Accept Platform Policy

3. **Create New App**
   - My Apps → Create App
   - App Type: "Business" or "Other"
   - Fill app details

4. **Add Ads Archive Product**
   - In app dashboard, add "Ads Archive" product
   - Configure permissions

5. **Generate Access Token**
   - Go to Graph API Explorer: https://developers.facebook.com/tools/explorer/
   - Select your app
   - Generate token with `ads_read` permission

6. **App Review (The Long Part)**
   - Submit for review
   - Explain use case: "Competitor research for agency clients"
   - Wait 1-3 weeks

7. **Test API Call**
   ```bash
   curl -G \
     -d "search_terms=casino" \
     -d "ad_reached_countries=['US']" \
     -d "access_token=YOUR_TOKEN" \
     "https://graph.facebook.com/v25.0/ads_archive"
   ```

---

### Option B: AdLibrary.com (Paid, Fast)

**URL:** https://www.adlibrary.com/
**Time:** Immediate
**Cost:** Paid (pricing on request)
**Limits:** Higher than official API

#### Steps

1. **Go to website**
   - https://www.adlibrary.com/

2. **Request Demo / Pricing**
   - Contact form on homepage
   - Mention: "Meta/Facebook ad intelligence for agency"

3. **Get API Key**
   - After signup, API key provided in dashboard
   - Documentation sent via email

4. **Test API**
   - Endpoint format provided in onboarding
   - Typically: `https://api.adlibrary.com/v1/ads?query=...`

---

## Recommendation for Lead Engine

| API | Decision | Why |
|-----|----------|-----|
| **WhoisXML** | ✅ Sign up NOW | Free, 2 minutes, essential for scoring |
| **Meta Ad Library** | ⏸️ Start with AdLibrary.com (if budget) OR Official (if patient) | Official API = weeks of delay |

### MVP Path (Fastest)
1. Sign up WhoisXML today (2 min)
2. Contact AdLibrary.com for pricing/demo (same day)
3. If AdLibrary too expensive → fall back to official Meta API (start process, wait while building other parts)

### Cost-Conscious Path
1. Sign up WhoisXML today (2 min)
2. Start official Meta API process (1-3 weeks wait)
3. Build scoring engine with mock data while waiting

---

## Your Action Items

- [ ] **WhoisXML API** — Sign up at https://drs.whoisxmlapi.com/signup (use business email!)
- [ ] **Meta Ad Library** — Decide: AdLibrary.com (fast, paid) or Official (slow, free)
- [ ] **Save API keys** — I'll update CONFIG.md once you have them

---

## Notes for AI Continuation

- WhoisXML signup is quick win — user can do immediately
- Meta decision depends on budget vs timeline preference
- Scoring engine can be built with placeholder/mock data while waiting for APIs
- User has closers ready — speed matters, but don't block on APIs if can build offline
