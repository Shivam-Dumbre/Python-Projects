import os
import shutil
import time
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

WATCH_DIR = config["watch_dir"]
DEST_ROOT = config["dest_root"]

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".tar", ".gz"],
    "Music": [".mp3", ".wav"],
    "Scripts": [".py", ".sh", ".js"],
}

def get_category(filename):
    _, ext = os.path.splitext(filename.lower())
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def organize_file(filepath):
    filename = os.path.basename(filepath)
    category = get_category(filename)
    dest_folder = os.path.join(DEST_ROOT, category)

    os.makedirs(dest_folder, exist_ok=True)

    dest_path = os.path.join(dest_folder, filename)
    print(f"Moving {filename} -> {dest_folder}")
    shutil.move(filepath, dest_path)

def watch_folder():
    print(f"Watching folder: {WATCH_DIR}")
    while True:
        for filename in os.listdir(WATCH_DIR):
            filepath = os.path.join(WATCH_DIR, filename)
            if os.path.isfile(filepath):
                organize_file(filepath)
        time.sleep(3)

if __name__ == "__main__":
    from pathlib import Path
    from organizer.config import load_settings

    config_path = Path("configs/config.yaml")
    settings = load_settings(config_path)

    from organizer.core import FileOrganizer
    organizer = FileOrganizer(settings)
    organizer.run()

