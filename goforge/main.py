import logging
import argparse

from goforge.config_parser import parse_config
from goforge.writer import sql_maker, handler_maker, server_maker
from goforge.file_manager.file_manager import FileManager

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def entrypoint():
    parser = argparse.ArgumentParser(description="generate Golang-Postgres CRUD backend blazingly fast 💙")
    parser.add_argument("-c", "--config-file", required=True, help="""path for goforge config file,
                        documentation: https://github.com/PrashantBtkl/goforge?tab=readme-ov-file#api-configuration-documentation""")
    parser.add_argument("-d", "--delete", action="store_true", help="delete the project")
    args = parser.parse_args()
    config_file = args.config_file
    data = parse_config(config_file)
    if data == {}:
        return
    file_manager = FileManager(data['project_path'])
    if args.delete:
        file_manager.delete_project()
        return
    file_manager.create_golang_project_template()
    # creates sqlc generated models and query files
    # setups docker compose postgres db for local testing
    sql_maker.SqlMaker(data['project_path'], data).make()
    # creates handler files for each handler
    try:
        handler_maker.generate_handlers(data['project_path'], data['handlers'])
    except Exception as e:
        logging.error("failed to generate handlers: %s",e)
        file_manager.delete_project(exception=True)
        return
    # generates main.go and runs all go commands
    try:
        server_maker.ServerMaker(data['project_path'], data['project_mod'], data['db'], data['handlers']).make()
    except Exception as e:
        logging.error("failed to generate server: %s", e)
        file_manager.delete_project(exception=True)
        return
    logging.info("your project has been created")

if __name__ == '__main__':
    entrypoint()
