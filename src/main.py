"""Main entry point for the lead engine pipeline."""

import argparse
import time
from pathlib import Path

from .cli.display import (
    console,
    print_banner,
    print_error,
    print_info,
    print_success,
    print_warning,
    display_spinner,
    display_summary,
    LeadTable,
)
from .core.config_loader import ConfigLoader, ConfigError
from .core.scoring_engine import ScoringEngine
from .core.pipeline_tracker import PipelineTracker
from .core.cache_manager import CacheManager
from .output.report_generator import ReportGenerator
from .output.webhook_notifier import WebhookNotifier

# Sourcing providers
from .sourcing.vibe_api import VibeProspectingAPI
from .sourcing.google_maps import GoogleMapsSourcing
from .sourcing.apify_instagram import ApifyInstagramScraper

# Enrichment providers
from .enrichment.whoisxml import WhoisXMLEnrichment
from .enrichment.hunter_io import HunterIOEnrichment
from .enrichment.pappers import PappersEnrichment

# Signal providers
from .signals.meta_ad_library import MetaAdLibrarySignal
from .signals.google_ads_transparency import GoogleAdsTransparencySignal
from .signals.linkedin_jobs import LinkedInJobsSignal


SOURCING_PROVIDERS = {
    "vibe_api": VibeProspectingAPI,
    "google_maps": GoogleMapsSourcing,
    "apify_instagram": ApifyInstagramScraper,
}

ENRICHMENT_PROVIDERS = {
    "whoisxml": WhoisXMLEnrichment,
    "hunter_io": HunterIOEnrichment,
    "pappers": PappersEnrichment,
}

SIGNAL_PROVIDERS = {
    "meta_ad_library": MetaAdLibrarySignal,
    "google_ads_transparency": GoogleAdsTransparencySignal,
    "linkedin_jobs": LinkedInJobsSignal,
}


def run_pipeline(config_path: Path, dry_run: bool = False, export_only: bool = False) -> None:
    """Execute the complete lead generation pipeline."""
    start_time = time.time()

    # Step 1: Display banner
    print_banner()

    # Step 2: Load configuration
    print_info(f"Loading configuration: {config_path}")
    try:
        config = ConfigLoader(config_path)
    except ConfigError as e:
        print_error(str(e))
        return

    print_success(f"Vertical: {config.vertical} — {config.description}")
    print_info(f"Geos: {', '.join(config.geo)} | Keywords: {', '.join(config.keywords)}")

    # Initialize components
    cache = CacheManager(
        ttl_hours=config.cache_ttl_hours,
        enabled=config.cache_enabled,
        dry_run=dry_run,
    )
    tracker = PipelineTracker()
    scoring = ScoringEngine(config)
    notifier = WebhookNotifier(config)
    report_gen = ReportGenerator()

    # Step 3: Sourcing
    print_info("\n" + "=" * 50)
    print_info("STEP 1: SOURCING")
    print_info("=" * 50)

    all_leads = []

    for signal_name in config.signals:
        if signal_name in SOURCING_PROVIDERS:
            provider_class = SOURCING_PROVIDERS[signal_name]
            provider = provider_class(dry_run=dry_run)

            with display_spinner(f"Sourcing via {signal_name}..."):
                leads = provider.execute(config.keywords, config.geo)
                all_leads.extend(leads)
                print_success(f"Found {len(leads)} prospects via {signal_name}")

    if not all_leads:
        print_warning("No leads found. Check your configuration.")
        return

    print_info(f"Total prospects sourced: {len(all_leads)}")

    # Step 4: Enrichment
    print_info("\n" + "=" * 50)
    print_info("STEP 2: ENRICHMENT")
    print_info("=" * 50)

    enriched_leads = []
    for lead in all_leads:
        # Apply enrichment providers
        for enrich_name in ["whoisxml", "hunter_io", "pappers"]:
            if enrich_name in ENRICHMENT_PROVIDERS:
                provider_class = ENRICHMENT_PROVIDERS[enrich_name]
                provider = provider_class(dry_run=dry_run)
                enriched = provider.execute(lead)
                lead.update(enriched)

        enriched_leads.append(lead)

    print_success(f"Enriched {len(enriched_leads)} leads")

    # Step 5: Scoring
    print_info("\n" + "=" * 50)
    print_info("STEP 3: SCORING")
    print_info("=" * 50)

    scored_results = scoring.batch_score(enriched_leads)

    # Add scoring info to leads
    for result in scored_results:
        result["lead"]["score"] = result["score"]
        result["lead"]["verdict"] = result["verdict"]
        result["lead"]["breakdown"] = result["breakdown"]

    # Step 6: Track in pipeline
    print_info("\n" + "=" * 50)
    print_info("STEP 4: PIPELINE TRACKING")
    print_info("=" * 50)

    for result in scored_results:
        lead = result["lead"]
        success, msg = tracker.add_lead(lead)
        if success:
            tracker.update_status(lead["_id"], "scored")

    print_success(f"Added {len(scored_results)} leads to pipeline")

    # Step 7: Notify hot leads
    print_info("\n" + "=" * 50)
    print_info("STEP 5: NOTIFICATIONS")
    print_info("=" * 50)

    hot_leads = [r for r in scored_results if r["verdict"] == "HOT"]
    if hot_leads:
        print_warning(f"{len(hot_leads)} HOT leads detected!")
        for result in hot_leads:
            lead = result["lead"]
            notifications = notifier.notify(lead)
            if any(notifications.values()):
                print_success(f"Notified: {lead.get('name', 'N/A')}")
    else:
        print_info("No HOT leads to notify")

    # Step 8: Export
    print_info("\n" + "=" * 50)
    print_info("STEP 6: EXPORT")
    print_info("=" * 50)

    # Export CSV
    csv_path = Path("outputs/leads_export.csv")
    count = tracker.export_csv(csv_path)
    print_success(f"Exported {count} leads to CSV: {csv_path}")

    # Generate HTML report
    report_path = report_gen.generate(
        leads=[r["lead"] for r in scored_results],
        vertical=config.vertical,
        stats=tracker.stats(),
    )
    print_success(f"Generated HTML report: {report_path}")

    # Step 9: Display summary table
    print_info("\n" + "=" * 50)
    print_info("RESULTS")
    print_info("=" * 50)

    table = LeadTable(title=f"Leads — {config.vertical}")
    for result in scored_results:
        lead = result["lead"]
        signals = lead.get("signals", [])
        lead["signals"] = signals
        table.add_lead(lead, result)

    console.print(table.render())

    # Summary stats
    duration = time.time() - start_time
    stats = tracker.stats()

    display_summary(
        total=stats["total_leads"],
        hot=stats["hot_leads"],
        warm=stats["warm_leads"],
        cold=stats["total_leads"] - stats["hot_leads"] - stats["warm_leads"],
        disqualified=0,  # Could be calculated if needed
        duration=duration,
    )

    print_success("\nPipeline completed successfully!")


def main():
    """CLI entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Lead Engine — Automated prospect sourcing and qualification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m lead_engine.main                          # Run with default config
  python -m lead_engine.main --dry-run                # Use mock data (no API calls)
  python -m lead_engine.main --config custom.yaml     # Use custom config
  python -m lead_engine.main --export-only            # Re-export without API calls
  python -m lead_engine.main --vertical casinos       # Load vertical config
        """,
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/vertical.config.yaml"),
        help="Path to configuration YAML file (default: config/vertical.config.yaml)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run with mock data only (no API calls)",
    )

    parser.add_argument(
        "--export-only",
        action="store_true",
        help="Re-export CSV and HTML without running pipeline",
    )

    parser.add_argument(
        "--vertical",
        type=str,
        help="Load vertical-specific config from config/verticals/{name}.yaml",
    )

    args = parser.parse_args()

    # Handle --vertical flag
    if args.vertical:
        vertical_config = Path(f"config/verticals/{args.vertical}.yaml")
        if vertical_config.exists():
            args.config = vertical_config
        else:
            print_error(f"Vertical config not found: {vertical_config}")
            return

    # Handle --export-only
    if args.export_only:
        print_info("Export-only mode: regenerating CSV and HTML from existing data")
        tracker = PipelineTracker()
        report_gen = ReportGenerator()

        csv_path = Path("outputs/leads_export.csv")
        count = tracker.export_csv(csv_path)
        print_success(f"Exported {count} leads to CSV: {csv_path}")

        leads = tracker.get_all()
        report_path = report_gen.generate(leads=leads, vertical="Export")
        print_success(f"Generated HTML report: {report_path}")
        return

    # Run full pipeline
    run_pipeline(args.config, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
