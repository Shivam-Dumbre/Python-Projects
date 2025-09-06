import typer
from pathlib import Path
from organizer.config import load_settings
from organizer.core import FileOrganizer

app = typer.Typer(help="Smart File Organizer CLI")

@app.command()
def run(
    watch_dir: Path = typer.Argument(..., help="Folder to watch"),
    dest_root: Path = typer.Argument(..., help="Destination root folder"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate without moving files"),
    conflict: str = typer.Option("rename", "--conflict", help="File conflict handling: rename | overwrite"),
):
    """
    Run the file organizer for a specific watch directory and destination.
    """
    # Load settings from arguments instead of YAML
    from organizer.config import Settings, Rule
    settings = Settings(
        watch_dir=watch_dir,
        dest_root=dest_root,
        dry_run=dry_run,
        conflict=conflict,
        rules=[],  # For now just use defaults, or load from YAML later
        default_dest="Others"
    )

    organizer = FileOrganizer(settings)
    organizer.run()


@app.command()
def from_config(
    config_path: Path = typer.Argument("config.yaml", help="Path to YAML config file")
):
    """
    Run the file organizer using a config.yaml file.
    """
    settings = load_settings(config_path)
    organizer = FileOrganizer(settings)
    organizer.run()


if __name__ == "__main__":
    app()
