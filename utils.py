import yaml


def load_yaml(filepath: str):
    with open(filepath, "r") as file:
        data = yaml.load(file, yaml.FullLoader)

    return data

def load_data_from_yaml(filepath: str):
    with open(filepath, "r") as file:
        data = yaml.load(file, yaml.FullLoader)
    
    return data["data"]

def load_locators_from_yaml(filepath: str):
    with open(filepath, "r") as file:
        data = yaml.load(file, yaml.FullLoader)
    
    return data["locators"]
