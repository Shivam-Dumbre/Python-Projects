import yaml
from pathlib import Path

def load_settings(config_path: Path):
    """Load rules from the YAML config file."""
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    # Return the rules dictionary directly
    return data["rules"]
