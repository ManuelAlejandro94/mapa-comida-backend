import os
import yaml
from src.crud.web import create_application

path = os.environ.get('MAPA-COMIDA_CONFIG', 'config.yml')
with open(path, mode="r", encoding='utf-8') as yaml_file:
    config = yaml.load(yaml_file)

app = create_application(config)
