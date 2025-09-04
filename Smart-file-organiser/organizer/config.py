from pathlib import Path
import yaml


def load_settings(config_path: Path) -> dict:
    """
    Load settings from a YAML config file.
    Returns a dictionary with watch_dir, output_dir, and rules.
    """

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Validate keys
    required_keys = ["watch_dir", "output_dir", "rules"]
    for key in required_keys:
        if key not in data:
            raise KeyError(f"Missing required config key: {key}")

    # Expand ~ and make absolute paths
    data["watch_dir"] = str(Path(data["watch_dir"]).expanduser().resolve())
    data["output_dir"] = str(Path(data["output_dir"]).expanduser().resolve())

    return data
