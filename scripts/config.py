import yaml

def load_config(config_file):
    with open(config_file, 'r') as file:
        cfg = yaml.safe_load(file)
    return cfg

def save_config(config_file, cfg):
    with open(config_file, 'w') as file:
        yaml.safe_dump(cfg, file)
