import logging

from goforge.config_parser import parseConfig
from goforge.writer import sql_maker, handler_maker, server_maker
from goforge.file_manager.file_manager import FileManager
import argparse

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def entrypoint():
    parser = argparse.ArgumentParser(description="generate Golang-Postgres CRUD backend blazingly fast 💙")
    parser.add_argument("-c", "--config-file", required=True, help="""path for goforge config file,
                        documentation: https://github.com/PrashantBtkl/goforge?tab=readme-ov-file#api-configuration-documentation""")
    parser.add_argument("-d", "--delete", action="store_true", help="delete the project")
    
    args = parser.parse_args()
    config_file = args.config_file
    
    data = parseConfig(config_file)
    file_manager = FileManager(data['project_path'])

    if args.delete:
        file_manager.deleteProject()
        return
    
    file_manager.createGolangProjectTemplate()
    
    # creates sqlc generated models and query files
    # setups docker compose postgres db for local testing
    sql_maker.SqlMaker(data['project_path'], data).Make()
    
    # creates handler files for each handler
    try:
        handler_maker.GenerateHandlers(data['project_path'], data['handlers'])
    except Exception as e:
        logging.error(f"failed to generate handlers: {e}")
        file_manager.deleteProject(exception=True)
        return

    
    # generates main.go and runs all go commands
    try:
        server_maker.ServerMaker(data['project_path'], data['project_mod'], data['db'], data['handlers']).Make()
    except Exception as e:
        logging.error(f"failed to generate server: {e}")
        file_manager.deleteProject(exception=True)
        return


    logging.info("your project has been created")

if __name__ == '__main__':
    entrypoint()


