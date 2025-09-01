from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time, logging
from .rules import pick_destination
from .mover import move_file
from .config import Settings

class Handler(FileSystemEventHandler):
    def __init__(self, cfg: Settings):
        self.cfg = cfg

    def on_created(self, event):
        if event.is_directory: return
        path = Path(event.src_path)
        time.sleep(0.5)
        dest = pick_destination(path, self.cfg)
        move_file(path, dest, self.cfg.dry_run, self.cfg.conflict)

def run_watcher(cfg: Settings):
    logging.info(f"Watching {cfg.watch_dir}")
    obs = Observer()
    obs.schedule(Handler(cfg), str(cfg.watch_dir), recursive=False)
    obs.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()
