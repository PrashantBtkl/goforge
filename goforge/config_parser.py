import logging
import yaml

def parse_config(file_path: str) -> dict:
    """
    takes in relative file path of yaml config and loads the yaml
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except yaml.YAMLError as e:
        logging.error("Error parsing YAML file: %s", e)
        return {}
    except FileNotFoundError:
        logging.error("File not found: %s",file_path)
        return {}
