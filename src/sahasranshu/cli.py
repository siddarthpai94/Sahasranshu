"""CLI interface for sahasranshu."""

import typer
from pathlib import Path
from typing import Optional

app = typer.Typer(help="Sahasranshu policy analysis system")


@app.command()
def run(
    input: Path = typer.Option(..., help="Input directory or file"),
    output: Path = typer.Option("results/", help="Output directory"),
    verbose: bool = typer.Option(False, help="Enable verbose logging"),
) -> None:
    """Run the analysis pipeline."""
    typer.echo(f"Running sahasranshu pipeline...")
    typer.echo(f"Input: {input}")
    typer.echo(f"Output: {output}")
    if verbose:
        typer.echo("Verbose mode enabled")


@app.command()
def version() -> None:
    """Show version."""
    from . import __version__
    typer.echo(f"sahasranshu {__version__}")


if __name__ == "__main__":
    app()
