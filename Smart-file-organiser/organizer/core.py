import os
import shutil
import time
from pathlib import Path

class FileOrganizer:
    def __init__(self, watch_dir: Path, output_dir: Path, rules: list):
        self.watch_dir = Path(watch_dir)
        self.output_dir = Path(output_dir)
        self.rules = rules  # list of dicts from config.yaml

    def get_category(self, filename: str):
        """Return category name based on file extension."""
        ext = Path(filename).suffix.lower()
        for rule in self.rules:
            if ext in rule["extensions"]:
                return rule["name"]
        return "Others"  # fallback

    def move_file(self, filename: str, category: str):
        """Move file into output_dir/category."""
        src_path = self.watch_dir / filename
        dest_dir = self.output_dir / category
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_path = dest_dir / filename
        try:
            shutil.move(str(src_path), str(dest_path))
            print(f"Moved: {filename} -> {dest_dir}")
        except Exception as e:
            print(f"Error moving {filename}: {e}")

    def run(self):
        """Continuously watch the folder and organize files."""
        print(f"Watching folder: {self.watch_dir}")
        while True:
            try:
                for filename in os.listdir(self.watch_dir):
                    file_path = self.watch_dir / filename
                    if file_path.is_file():
                        category = self.get_category(filename)
                        self.move_file(filename, category)
                time.sleep(3)
            except KeyboardInterrupt:
                print("\nStopped watching.")
                break
