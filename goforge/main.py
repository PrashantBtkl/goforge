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
    handler_maker.GenerateHandlers(data['project_path'], data['handlers'])
    
    # generates main.go and runs all go commands
    server_maker.ServerMaker(data['project_path'], data['project_mod'], data['setup_postgres_local'], data['handlers']).Make()

    logging.info("your project has been created")

if __name__ == '__main__':
    entrypoint()


