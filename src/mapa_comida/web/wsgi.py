import os
import yaml
from src.mapa_comida.web import create_application

path = os.environ.get('MAPA_COMIDA_CONFIG', 'config.yml')
with open(path, mode="r", encoding='utf-8') as yaml_file:
    config = yaml.load(yaml_file)

app = create_application(config)
