import yaml
import os

def load_config(path="config/settings.yaml") -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found at {path}")
    with open(path, 'r') as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    cfg = load_config()
    print(f"Loaded config for {cfg['app']['name']}")
