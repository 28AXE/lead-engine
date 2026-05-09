"""Rich-based terminal display for lead results and progress."""

from datetime import datetime
from typing import Any, Optional

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.style import Style
from rich import box


console = Console()

VERDICT_STYLES = {
    "HOT": Style(color="red", bold=True),
    "WARM": Style(color="yellow"),
    "COLD": Style(color="blue"),
    "DISQUALIFIED": Style(color="white", dim=True),
}

VERDICT_EMOJIS = {
    "HOT": "🔥",
    "WARM": "🟡",
    "COLD": "🔵",
    "DISQUALIFIED": "❌",
}


def print_banner() -> None:
    """Display ASCII banner in color."""
    banner = """
╔════════════════════════════════════════╗
║     ███╗   ██╗ █████╗  ██████╗██╗  ██╗║
║     ████╗  ██║██╔══██╗██╔════╝██║  ██║║
║     ██╔██╗ ██║███████║██║     ███████║║
║     ██║╚██╗██║██╔══██║██║     ██╔══██║║
║     ██║ ╚████║██║  ██║╚██████╗██║  ██║║
║     ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝║
║          E N G I N E                   ║
╚════════════════════════════════════════╝
"""
    console.print(Panel(banner, style="bold cyan", box=box.DOUBLE))


def create_progress() -> Progress:
    """Create a progress bar with spinner."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    )


def display_spinner(text: str = "Processing...") -> Progress:
    """Create and return a spinner progress."""
    progress = create_progress()
    progress.add_task(description=text, total=None)
    return progress


class LeadTable:
    """Displays leads in a formatted table."""

    def __init__(self, title: str = "Leads"):
        self.title = title
        self.table = Table(
            title=title,
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
            expand=True,
        )
        self.table.add_column("Nom", style="cyan", no_wrap=True)
        self.table.add_column("Domaine", style="white")
        self.table.add_column("Score", justify="right", style="green")
        self.table.add_column("Verdict", justify="center")
        self.table.add_column("Email", style="dim", no_wrap=True)
        self.table.add_column("Signaux", style="yellow")

    def add_lead(self, lead: dict[str, Any], score_result: dict[str, Any]) -> None:
        """Add a lead row to the table."""
        verdict = score_result.get("verdict", "COLD")
        score = score_result.get("score", 0)
        signals = lead.get("signals", [])
        signals_str = ", ".join(signals[:3]) if signals else "-"

        self.table.add_row(
            lead.get("name", "N/A"),
            lead.get("domain", "N/A"),
            str(score),
            f"{VERDICT_EMOJIS.get(verdict, '')} {verdict}",
            lead.get("email", "-"),
            signals_str,
            style=VERDICT_STYLES.get(verdict),
        )

    def render(self) -> Table:
        """Return the table for rendering."""
        return self.table


def display_summary(
    total: int,
    hot: int,
    warm: int,
    cold: int,
    disqualified: int,
    duration: float,
) -> None:
    """Display final summary panel."""
    summary = f"""
[bold green]✓[/bold green] {total} leads analysés
[red bold]🔥 {hot} HOT[/red bold]
[yellow]🟡 {warm} WARM[/yellow]
[blue]🔵 {cold} COLD[/blue]
[dim]❌ {disqualified} DISQUALIFIED[/dim]

[bold]Durée : {duration:.1f}s[/bold]
"""
    console.print(Panel(summary, title="Résultats", style="bold green", box=box.DOUBLE))


def display_lead(lead: dict[str, Any], score_result: dict[str, Any]) -> None:
    """Display a single lead with its score."""
    verdict = score_result.get("verdict", "COLD")
    score = score_result.get("score", 0)

    console.print(
        Panel(
            f"[bold]{lead.get('name', 'N/A')}[/bold]\n"
            f"Domaine: {lead.get('domain', 'N/A')}\n"
            f"Score: [green bold]{score}[/green bold]\n"
            f"Verdict: [{VERDICT_STYLES[verdict].color} bold]{verdict} {VERDICT_EMOJIS.get(verdict, '')}[/{VERDICT_STYLES[verdict].color} bold]",
            style=VERDICT_STYLES.get(verdict),
        )
    )


def print_error(message: str) -> None:
    """Display error message."""
    console.print(f"[bold red]✗ ERROR:[/bold red] {message}")


def print_warning(message: str) -> None:
    """Display warning message."""
    console.print(f"[bold yellow]⚠ WARNING:[/bold yellow] {message}")


def print_success(message: str) -> None:
    """Display success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_info(message: str) -> None:
    """Display info message."""
    console.print(f"[cyan]ℹ[/cyan] {message}")
