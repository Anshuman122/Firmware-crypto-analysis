# Hinglish: Dynamic runner ke liye command-line tool.

import typer
from crypto_finder.dynamic_runner.core import DynamicRunner
from crypto_finder.common.logging import log
import json

def dynamic_run(
    shellcode: str = typer.Option(
        ...,
        "--shellcode",
        "-s",
        help="The hexadecimal shellcode string to execute.",
    ),
):
    """
    Emulates a piece of x86-64 shellcode and prints the execution trace.
    """
    log.info("CLI command invoked for dynamic shellcode execution.")
    try:
        # Hex string ko bytes me convert karo
        code_bytes = bytes.fromhex(shellcode)
    except ValueError:
        typer.secho("❌ Error: Invalid hexadecimal string in --shellcode.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    runner = DynamicRunner()
    result = runner.emulate(code=code_bytes)

    typer.secho(f"--- Emulation Result ---", fg=typer.colors.CYAN, bold=True)
    typer.echo(json.dumps(result, indent=4))