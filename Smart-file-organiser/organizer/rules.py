from pathlib import Path
from .config import Settings

def pick_destination(file: Path, cfg: Settings) -> Path:
    name = file.name
    for rule in cfg.rules:
        if rule.pattern.search(name):
            return cfg.dest_root / rule.dest
    return cfg.dest_root / cfg.default_destination
