from pathlib import Path
import shutil, logging, time

def _resolve_conflict(target: Path, policy: str) -> Path:
    if not target.exists() or policy == "overwrite":
        return target
    if policy == "skip":
        return None

    stem, suffix = target.stem, target.suffix
    i = 1
    while True:
        candidate = target.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1
def move_file(src: Path, dest_dir: Path, dry_run: bool, conflict: str) -> bool:
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = dest_dir / src.name
    target = _resolve_conflict(target, conflict)
