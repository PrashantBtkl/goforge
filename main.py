from writer import sql_maker, handler_maker, server_maker
import parser
from file_manager.file_manager import FileManager

project_path = "example"
config_file = "./example.yml"
project_mod = "example.com/crud"

file_manager = FileManager(project_path)
file_manager.deleteProject()
data = parser.parse_yaml_config(config_file)
file_manager.createGolangProjectTemplate()

# creates sqlc generated models and query files
# setups docker compose postgres db for local testing
sql_maker.SqlMaker(project_path, data).Make()

# creates handler files for each handler
handler_maker.generateHandlers(project_path, data['handlers'])

# generates main.go and runs all go commands
server_maker.ServerMaker(project_path, project_mod, data['handlers']).Make()

print("done")


