import typer

app = typer.Typer()


@app.command(name="backup")
def backup(
	src: str = typer.Option(..., help="Source directory"),
	dest: str = typer.Option(..., help="Destination directory"),
	publication: str = typer.Option("--private", help="Publication type"),
):
	from commands.backup import Backup

	Backup(src=src, dest=dest, publication=publication).execute()
