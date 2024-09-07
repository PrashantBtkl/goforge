import yaml
import logging

def parseConfig(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file: {e}")
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        loggging.error(f"An error occurred: {e}")
