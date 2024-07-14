import yaml

def load_config(config_file):
    """
    Load configuration from a YAML file.

    Parameters:
    config_file (str): Path to the YAML configuration file.

    Returns:
    dict: Configuration parameters.
    """
    with open(config_file, 'r') as file:
        cfg = yaml.safe_load(file)
    return cfg
