import argparse, logging
from pathlib import Path
from .config import load_settings
from .watcher import run_watcher
from .rules import pick_destination
from .mover import move_file

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--once", action="store_true", help="Organize current files and exit")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)
    cfg = load_settings(Path(args.config))

    if args.once:
        for f in cfg.watch_dir.iterdir():
            if f.is_file():
                dest = pick_destination(f, cfg)
                move_file(f, dest, cfg.dry_run, cfg.conflict)
    else:
        run_watcher(cfg)

if __name__ == "__main__":
    main()
