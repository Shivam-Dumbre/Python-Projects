from dataclasses import dataclass
from pathlib import Path
import yaml, re

@dataclass
class Rule:
    name: str
    pattern: re.Pattern
    dest: str

@dataclass
class Settings:
    watch_dir: Path
    dest_root: Path
    dry_run: bool
    conflict: str
    rules: list[Rule]
    default_dest: str

def load_settings(path: Path) -> Settings:
    data = yaml.safe_load(path.read_text())
    rules = [Rule(r["name"], re.compile(r["pattern"], re.IGNORECASE), r["dest"])
             for r in data["rules"]]
    return Settings(
        watch_dir=Path(data["watch_dir"]).expanduser(),
        dest_root=Path(data["dest_root"]).expanduser(),
        dry_run=bool(data.get("dry_run", True)),
        conflict=data.get("conflict", "rename"),
        rules=rules,
        default_dest=data.get("default_dest", "Others"),
    )
