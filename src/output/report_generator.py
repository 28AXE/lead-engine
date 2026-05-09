"""Report generator for lead summaries and analytics."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class ReportGenerator:
    """Generates standalone HTML reports with inline CSS/JS."""

    def __init__(self, output_dir: str | Path = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(
        self,
        leads: list[dict[str, Any]],
        vertical: str = "Unknown",
        stats: dict[str, Any] | None = None,
    ) -> Path:
        """Generate HTML report and return path."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filepath = self.output_dir / f"report_{timestamp}.html"

        hot_count = sum(1 for l in leads if l.get("verdict") == "HOT")
        warm_count = sum(1 for l in leads if l.get("verdict") == "WARM")
        total = len(leads)

        html = self._build_html(
            leads=leads,
            vertical=vertical,
            timestamp=timestamp,
            total=total,
            hot=hot_count,
            warm=warm_count,
            stats=stats or {},
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        return filepath

    def _build_html(
        self,
        leads: list[dict[str, Any]],
        vertical: str,
        timestamp: str,
        total: int,
        hot: int,
        warm: int,
        stats: dict[str, Any],
    ) -> str:
        """Build complete HTML document."""
        return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lead Engine Report — {vertical}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; color: #333; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}

        header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; }}
        header h1 {{ font-size: 2rem; margin-bottom: 10px; }}
        header .meta {{ opacity: 0.8; font-size: 0.9rem; }}

        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-card .value {{ font-size: 2.5rem; font-weight: bold; }}
        .stat-card .label {{ color: #666; font-size: 0.85rem; text-transform: uppercase; }}
        .stat-card.hot .value {{ color: #e74c3c; }}
        .stat-card.warm .value {{ color: #f39c12; }}
        .stat-card.cold .value {{ color: #3498db; }}
        .stat-card.total .value {{ color: #2ecc71; }}

        .top-leads {{ margin-bottom: 30px; }}
        .top-leads h2 {{ margin-bottom: 15px; color: #1a1a2e; }}
        .top-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }}
        .lead-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid #e74c3c; }}
        .lead-card.warm {{ border-left-color: #f39c12; }}
        .lead-card .lead-name {{ font-weight: bold; font-size: 1.1rem; margin-bottom: 8px; }}
        .lead-card .lead-domain {{ color: #666; font-size: 0.9rem; }}
        .lead-card .lead-score {{ display: inline-block; background: #e74c3c; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; margin-top: 10px; }}
        .lead-card.warm .lead-score {{ background: #f39c12; }}

        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        th {{ background: #1a1a2e; color: white; padding: 15px; text-align: left; cursor: pointer; user-select: none; }}
        th:hover {{ background: #16213e; }}
        th.sorted-asc::after {{ content: ' ▲'; }}
        th.sorted-desc::after {{ content: ' ▼'; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f8f9fa; }}

        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }}
        .badge.hot {{ background: #e74c3c; color: white; }}
        .badge.warm {{ background: #f39c12; color: white; }}
        .badge.cold {{ background: #3498db; color: white; }}
        .badge.disqualified {{ background: #95a5a6; color: white; }}

        footer {{ text-align: center; padding: 30px; color: #666; font-size: 0.85rem; }}

        .sortable {{ transition: background 0.2s; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Lead Engine Report</h1>
            <div class="meta">
                <strong>Vertical:</strong> {vertical} |
                <strong>Date:</strong> {timestamp.replace('_', ' ')} |
                <strong>Total:</strong> {total} leads
            </div>
        </header>

        <div class="stats">
            <div class="stat-card total">
                <div class="value">{total}</div>
                <div class="label">Total Leads</div>
            </div>
            <div class="stat-card hot">
                <div class="value">{hot}</div>
                <div class="label">🔥 Hot</div>
            </div>
            <div class="stat-card warm">
                <div class="value">{warm}</div>
                <div class="label">🟡 Warm</div>
            </div>
            <div class="stat-card cold">
                <div class="value">{total - hot - warm}</div>
                <div class="label">Cold</div>
            </div>
        </div>

        {self._top_leads_section(leads[:5])}

        <h2 style="margin-bottom: 15px; color: #1a1a2e;">Tous les leads</h2>
        <table id="leads-table">
            <thead>
                <tr>
                    <th class="sortable" data-sort="name">Nom</th>
                    <th class="sortable" data-sort="domain">Domaine</th>
                    <th class="sortable" data-sort="score">Score</th>
                    <th class="sortable" data-sort="verdict">Verdict</th>
                    <th class="sortable" data-sort="email">Email</th>
                </tr>
            </thead>
            <tbody>
                {self._table_rows(leads)}
            </tbody>
        </table>

        <footer>
            <strong>Powered by Lead Engine</strong> — Automated Prospect Qualification System
        </footer>
    </div>

    <script>
        // Inline vanilla JS for table sorting
        const table = document.getElementById('leads-table');
        const headers = table.querySelectorAll('th.sortable');
        let sortDir = {{}};

        headers.forEach(th => {{
            th.addEventListener('click', () => {{
                const key = th.dataset.sort;
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));

                sortDir[key] = sortDir[key] === 'asc' ? 'desc' : 'asc';

                rows.sort((a, b) => {{
                    let aVal = a.cells[th.cellIndex].textContent;
                    let bVal = b.cells[th.cellIndex].textContent;

                    if (key === 'score') {{
                        aVal = parseInt(aVal) || 0;
                        bVal = parseInt(bVal) || 0;
                    }}

                    if (sortDir[key] === 'asc') {{
                        return aVal > bVal ? 1 : -1;
                    }} else {{
                        return aVal < bVal ? 1 : -1;
                    }}
                }});

                rows.forEach(row => tbody.appendChild(row));

                headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));
                th.classList.add(sortDir[key] === 'asc' ? 'sorted-asc' : 'sorted-desc');
            }});
        }});
    </script>
</body>
</html>
"""

    def _top_leads_section(self, top_leads: list[dict[str, Any]]) -> str:
        """Generate top 5 leads section."""
        if not top_leads:
            return ""

        cards = []
        for lead in top_leads:
            verdict_class = "warm" if lead.get("verdict") == "WARM" else ""
            cards.append(f"""
            <div class="lead-card {verdict_class}">
                <div class="lead-name">{lead.get('name', 'N/A')}</div>
                <div class="lead-domain">{lead.get('domain', 'N/A')}</div>
                <span class="lead-score">Score: {lead.get('score', 0)}</span>
            </div>
            """)

        return f"""
        <div class="top-leads">
            <h2>🏆 Top 5 Leads</h2>
            <div class="top-grid">{''.join(cards)}</div>
        </div>
        """

    def _table_rows(self, leads: list[dict[str, Any]]) -> str:
        """Generate table rows."""
        rows = []
        for lead in leads:
            verdict = lead.get("verdict", "COLD").lower()
            rows.append(f"""
            <tr>
                <td>{lead.get('name', 'N/A')}</td>
                <td>{lead.get('domain', 'N/A')}</td>
                <td><strong>{lead.get('score', 0)}</strong></td>
                <td><span class="badge {verdict}">{lead.get('verdict', 'COLD')}</span></td>
                <td>{lead.get('email', '-')}</td>
            </tr>
            """)
        return "".join(rows)
