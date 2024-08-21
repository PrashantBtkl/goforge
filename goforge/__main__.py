from goforge.config_parser import parseConfig
from goforge.writer import sql_maker, handler_maker, server_maker
from goforge.file_manager.file_manager import FileManager
import argparse

def entrypoint():
    parser = argparse.ArgumentParser(description="generate golang crud backend")
    parser.add_argument("-c", "--config-file", help="path for goforge config file")
    
    args = parser.parse_args()
    config_file = args.config_file
    
    data = parseConfig(config_file)
    
    file_manager = FileManager(data['project_path'])
    file_manager.deleteProject()
    file_manager.createGolangProjectTemplate()
    
    # creates sqlc generated models and query files
    # setups docker compose postgres db for local testing
    sql_maker.SqlMaker(data['project_path'], data).Make()
    
    # creates handler files for each handler
    handler_maker.generateHandlers(data['project_path'], data['handlers'])
    
    # generates main.go and runs all go commands
    server_maker.ServerMaker(data['project_path'], data['project_mod'], data['handlers']).Make()

    print("done")

if __name__ == '__main__':
    entrypoint()


