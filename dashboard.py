from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich import box
from datetime import datetime

console = Console()

def dashboard(
    portfolio_value: float,
    portfolio_cash: float,
    eur_to_usd: float,
    generated_buy_signals: int,
    positions_scanned: int,
    portfolio_performance: float,
    placed_orders: list
):
    p = Table.grid(padding=(0, 2))
    p.add_column(style="dim")
    p.add_column(justify="right")
    p.add_row("Gesamtwert", f"[bold cyan]{portfolio_value:,.2f} EUR[/]")
    p.add_row("Barbestand", f"[bold green]{portfolio_cash:,.2f} EUR[/]")
    p.add_row("EUR / USD", f"[bold yellow]{eur_to_usd:.3f}[/]")

    performance_color = "green" if portfolio_performance > 0 else "red"
    performance_panel = Panel(
        Text(
            f"{portfolio_performance:.2f} %",
            style=f"bold {performance_color}",
            justify="center"
        ),
        title="Performance",
        border_style=performance_color,
        padding=(1,2)
    )
    portfolio_panel = Panel(
        p,
        title="[bold] Portfolio[/]",
        border_style="cyan",
        box=box.ROUNDED
    )
    scanner = Table.grid(padding=(0, 2))
    scanner.add_column(style="dim")
    scanner.add_column(justify="right", style="bold")
    scanner.add_row("Aktien durchsucht", f"{positions_scanned:,}")
    scanner.add_row("Kaufsignale", f"[green]{generated_buy_signals}[/]")
    scanner_panel = Panel(
        scanner,
        border_style="blue",
        box=box.ROUNDED
    )
    orders_table = Table(
        title="PLATZIERTE ORDERS",
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True
    )
    orders_table.add_column("Ticker")
    orders_table.add_column("ISIN")
    orders_table.add_column("Anzahl", justify="right")
    orders_table.add_column("Order Volume")
    orders_table.add_column("Limit")
    orders_table.add_column("Stop-Loss")
    orders_table.add_column("Fee")

    for order in placed_orders:
        orders_table.add_row(
            order["ticker"],
            order["isin"],
            str(order["amount"]),
            f"[bold]{order["order_volume"]:,.2f} EUR[/]",
            f"[bold green]{order["limit"]:,.2f} EUR[/]",
            f"[bold red]{order["stop_loss"]:,.2f} EUR[/]",
            f"{order["total_fees"]:,.2f} EUR[/]"
        )

    console.clear()
    console.print()
    console.print(
        Panel(
            f"[bold cyan]ERGEBNISSE[/] [dim] | {datetime.now().strftime("%d-%m-%y %H:%M:%S")}[/]",
            border_style="bright_blue",
            box=box.DOUBLE
        )
    )
    console.print(Columns([portfolio_panel, performance_panel], equal=True, expand=True))
    console.print(scanner_panel)
    if len(placed_orders) > 0: 
        console.print(orders_table)
    console.print()