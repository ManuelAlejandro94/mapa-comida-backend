from src.crud.web import create_application
from yaml import Loader
import logging
import yaml


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Ejecuta la aplicación en un servidor autocontenido en modo de desarrollo'
    )

    parser.add_argument(
        '-c', '--config',
        default='config.yml',
        help='Archivo de configuración'
    )

    parser.add_argument(
        '-p', '--port',
        default=5000,
        help='Puerto por defecto'
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    with open(args.config, mode="r", encoding='utf-8') as yaml_file:
        config = yaml.load(yaml_file, Loader)

    app = create_application(config)

    app.run(host="0.0.0.0", port=args.port)


if __name__ == '__main__':
    main()
