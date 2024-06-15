import yaml


def load_yaml(filepath: str):
    with open(filepath, "r") as file:
        data = yaml.load(file, yaml.FullLoader)

    return data
