# Hinglish: Symbolic analyzer ke liye command-line tool.

import typer
from pathlib import Path
from crypto_finder.symbolic.loop_analyzer import SymbolicAnalyzer
from crypto_finder.common.logging import log

def analyze_loops(
    binary_path: Path = typer.Option(
        ...,
        "--binary-path",
        "-b",
        help="The binary file to analyze for loops.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
):
    """
    Finds and reports all loops within a binary file using symbolic analysis.
    """
    log.info(f"CLI command invoked for symbolic loop analysis on '{binary_path.name}'.")
    try:
        analyzer = SymbolicAnalyzer(binary_path=binary_path)
        loops = analyzer.find_loops()
        
        if not loops:
            typer.secho("No loops found in the binary.", fg=typer.colors.YELLOW)
            return

        typer.secho(f"✅ Found {len(loops)} loop(s) in the binary:", fg=typer.colors.GREEN, bold=True)
        for i, loop in enumerate(loops):
            typer.secho(f"\n--- Loop #{i+1} ---", fg=typer.colors.CYAN)
            typer.echo(f"  - Entry Address: {loop['entry_address']}")
            typer.echo(f"  - Nodes in body: {loop['node_count']}")

    except Exception as e:
        log.error(f"Symbolic analysis failed: {e}")
        typer.secho(f"❌ Error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)