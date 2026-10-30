import yaml


def load_config(path: str = "configs/base.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)
