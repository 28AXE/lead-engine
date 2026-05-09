# Ajouter un Nouveau Vertical — Guide Pas à Pas

Ce guide vous permet d'ajouter un nouveau vertical **sans toucher une seule ligne de code**.

---

## Étape 1 : Copier la Configuration de Base

```bash
# Créer le répertoire des verticaux s'il n'existe pas
mkdir -p config/verticals

# Copier la config par défaut comme template
cp config/vertical.config.yaml config/verticals/votre_vertical.yaml
```

---

## Étape 2 : Modifier les Paramètres de Base

Ouvrez `config/verticals/votre_vertical.yaml` et modifiez :

```yaml
# Nom interne du vertical (utilisé dans les exports)
vertical: "votre_vertical"

# Description pour votre équipe
description: "Description claire de votre cible"

# Mode simulation (true = pas d'appels API)
dry_run: false

# Zones géographiques ciblées (codes ISO 2 lettres)
geo:
  - "FR"      # France
  - "BE"      # Belgique
  - "CH"      # Suisse
  - "CA"      # Canada
  - "LU"      # Luxembourg

# Mots-clés pour la recherche (utilisés par les APIs)
keywords:
  - "mot-clé 1"
  - "mot-clé 2"
  - "mot-clé 3"
```

### Exemple : Agence Immobilière
```yaml
vertical: "immobilier"
description: "Agences immobilières et property tech France"
geo:
  - "FR"
  - "BE"
keywords:
  - "agence immobilière"
  - "property management"
  - "transaction immobilière"
  - "immobilier luxe"
```

---

## Étape 3 : Choisir les Signaux

Sélectionnez les sources de données pertinentes pour votre vertical :

```yaml
signals:
  - vibe_api              # B2B database (SaaS, tech, services)
  - google_maps           # Commerces locaux (artisans, retail)
  - apify_instagram       # Influenceurs (D2C, lifestyle)
  - pappers               # Registry FR (France uniquement)
```

### Tableau de Décision

| Votre Cible | Signaux Recommandés |
|-------------|---------------------|
| Artisans / locaux | `google_maps`, `pappers` |
| SaaS / Tech B2B | `vibe_api`, `linkedin_jobs` |
| E-commerce D2C | `apify_instagram`, `meta_ad_library` |
| Agences / services | `vibe_api`, `pappers`, `meta_ad_library` |
| France uniquement | `pappers` est pertinent |
| International | Évitez `pappers` (FR only) |

---

## Étape 4 : Ajuster les Weights de Scoring

Le scoring total fait 40 points. Répartissez-les selon ce qui compte pour votre vertical :

```yaml
scoring_weights:
  domain_age: 10      # 0-10 pts : âge du domaine (jeune = plus de points)
  ad_activity: 9      # 0-9 pts : activité publicitaire (sweet spot: 0-10 ads)
  budget_signal: 9    # 0-9 pts : signaux de budget (influenceurs, Google Ads, funding)
  vertical_fit: 12    # 0-12 pts : adéquation avec les keywords du vertical
```

### Exemples de Répartition

**Pour un vertical "jeunes pousses" (startups) :**
```yaml
scoring_weights:
  domain_age: 12      # Très important : on veut des domaines récents
  ad_activity: 8      # Secondaire
  budget_signal: 10   # Funding = signal fort
  vertical_fit: 10    # Tech/SaaS fit
```

**Pour un vertical "established businesses" :**
```yaml
scoring_weights:
  domain_age: 6       # Moins important
  ad_activity: 12     # Activité ads = signal d'investissement
  budget_signal: 12   # Budget marketing confirmé
  vertical_fit: 10    # Fit secteur
```

**Pour un vertical "restricted industries" (CBD, casino) :**
```yaml
scoring_weights:
  domain_age: 10      # Nouveaux entrants = opportunité
  ad_activity: 10     # Besoin de whitelisting
  budget_signal: 10   # Marges élevées
  vertical_fit: 10    # Fit vertical restrictif
```

---

## Étape 5 : Configurer les Thresholds

Définissez vos seuils de qualification :

```yaml
scoring_thresholds:
  hot: 30    # ≥30 pts = 🔥 HOT (outreach sous 24h)
  warm: 22   # 22-29 pts = 🟡 WARM (outreach sous 1 semaine)
  cold: 15   # 15-21 pts = 🔵 COLD (nurture campaign)
             # <15 pts = ❌ DISQUALIFIED
```

### Ajuster selon votre appétit

| Votre Stratégie | Thresholds |
|-----------------|------------|
| Qualitative (peu mais qualifié) | `hot: 32, warm: 25, cold: 18` |
| Volume (tester beaucoup) | `hot: 28, warm: 20, cold: 12` |
| Équilibrée (défaut) | `hot: 30, warm: 22, cold: 15` |

---

## Étape 6 : Personnaliser l'Outreach

```yaml
outreach:
  tone: "direct et professionnel"     # Ton des messages
  value_prop: "plus de leads qualifiés"  # Proposition de valeur
```

### Exemples par Vertical

| Vertical | Tone | Value Prop |
|----------|------|------------|
| Artisans | "local et direct" | "plus de chantiers sans démarchage" |
| SaaS | "data-driven" | "ROI mesurable en 30 jours" |
| Agences | "expert à expert" | "scalez vos performances Meta" |
| E-commerce | "growth-focused" | "multipliez vos ventes par 3" |

---

## Étape 7 : Configurer les Notifications

```yaml
notifications:
  slack_webhook: "https://hooks.slack.com/services/XXX/YYY/ZZZ"
  discord_webhook: "https://discord.com/api/webhooks/XXX/YYY"
  notify_on: ["HOT", "WARM"]   # Quels verdicts déclenchent une notif
```

### Options

| notify_on | Cas d'usage |
|-----------|-------------|
| `["HOT"]` | Seulement les meilleurs leads (défaut) |
| `["HOT", "WARM"]` | Volume moyen, pour tester |
| `["HOT", "WARM", "COLD"]` | Tout notifier (déconseillé) |

---

## Étape 8 : Tester le Vertical

```bash
# Mode simulation (sans appels API)
python -m src.main --vertical votre_vertical --dry-run

# Vérifier les outputs
ls -la outputs/
cat outputs/leads_export.csv
open outputs/report_*.html
```

---

## Étape 9 : Passer en Production

```bash
# 1. Désactiver dry_run dans le YAML
# Edit config/verticals/votre_vertical.yaml
dry_run: false

# 2. Lancer le pipeline complet
python -m src.main --vertical votre_vertical

# 3. Vérifier les notifications
# Check Slack/Discord pour les alerts HOT
```

---

## Checklist Finale

- [ ] `vertical` et `description` renseignés
- [ ] `geo` correspond à la zone cible
- [ ] `keywords` pertinents pour le vertical
- [ ] `signals` cohérents avec la cible
- [ ] `scoring_weights` total = 40
- [ ] `scoring_thresholds` définis
- [ ] `outreach` personnalisé
- [ ] `notifications` configurées (optionnel)
- [ ] Test `--dry-run` passé
- [ ] CSV et HTML générés correctement

---

## Dépannage

### "No leads found"
→ Vérifiez que vos `keywords` ne sont pas trop restrictifs
→ Essayez avec `--dry-run` pour tester le pipeline

### "API key not configured"
→ Ajoutez la clé dans `.env` ou passez en `dry_run: true`

### Scores trop bas/hauts
→ Ajustez `scoring_weights` et `scoring_thresholds`

---

**Besoin d'aide ?** Consultez `docs/API_REFERENCE.md` pour les détails techniques de chaque API.
