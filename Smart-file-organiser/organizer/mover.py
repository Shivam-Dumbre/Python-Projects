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
