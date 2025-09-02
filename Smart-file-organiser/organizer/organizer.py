from pathlib import Path
from .config_loader import load_settings
from .core import FileOrganizer

def main():
    settings = load_settings()
    watch_dir = Path(settings["watch_dir"])
    output_dir = Path(settings["output_dir"])
    rules = settings["rules"]

    organizer = FileOrganizer(watch_dir, output_dir, rules)
    organizer.run()

if __name__ == "__main__":
    main()
