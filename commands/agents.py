import typer

app = typer.Typer()

@app.command()
def create():
    typer.echo("Create agent")


@app.command()
def list():
    typer.echo("List agents:")


if __name__ == "__main__":
    app()