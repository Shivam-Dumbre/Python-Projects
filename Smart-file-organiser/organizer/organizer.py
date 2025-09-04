import os
from pathlib import Path
from .config import load_settings
from .core import FileOrganizer


def main():
    # Point to config.yaml in the project root
    config_path = Path(__file__).resolve().parent.parent / "config.yaml"

    settings = load_settings(config_path)

    watch_dir = Path(settings["watch_dir"])
    output_dir = Path(settings["output_dir"])
    rules = settings["rules"]

    print(f"Watching folder: {watch_dir}")

    organizer = FileOrganizer(watch_dir, output_dir, rules)
    organizer.run()


if __name__ == "__main__":
    main()
