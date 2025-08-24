# Smart File Organizer

A Python utility that automatically organizes files from a "watch" folder (like Downloads) into categorized subfolders inside a destination root directory.  
It helps keep your system neat by sorting files by type (Images, Documents, Videos, Archives, etc.).

---

## Features
- Monitors a folder (e.g., Downloads) for files
- Automatically moves them into category-based subfolders
- Works in one-time batch mode or continuous monitoring mode
- Fully configurable using `config.yaml`

---

## How It Works
1. You define:
   - `watch_dir`: the folder to monitor (e.g., `~/Downloads`)
   - `dest_root`: the root folder where files will be sorted
   - Categories and extensions in `config.yaml`
2. Run the script.
3. Files are moved into organized folders.

---

## Example
Say you have:

watch_dir: "/Users/shivam/Downloads"
dest_root: "/Users/shivam/Sorted"

And `config.yaml` defines:
```yaml
rules:
  Images: [".jpg", ".png", ".gif"]
  Documents: [".pdf", ".docx", ".txt"]
  Videos: [".mp4", ".mkv"]
  Archives: [".zip", ".tar", ".gz"]

If you download holiday.jpg → it will move to:
/Users/shivam/Sorted/Images/holiday.jpg


## Installation
Clone the repo and install dependencies:
git clone https://github.com/yourusername/smart-file-organizer.git
cd smart-file-organizer
pip install -r requirements.txt
