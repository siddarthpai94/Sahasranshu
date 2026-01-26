import typer

app = typer.Typer(
    add_completion=False,
    help="Sahasranshu: US–India delta-first quant research system"
)

@app.command()
def hello() -> None:
    """Sanity check command."""
    typer.echo("Sahasranshu CLI is working")

def run() -> None:
    # This is the canonical entrypoint for Typer apps.
    app()

if __name__ == "__main__":
    run()