from writer import sql_maker, handler_maker, server_maker
import parser
from file_manager.file_manager import FileManager

project_path = "example"
config_file = "./example.yml"

file_manager = FileManager(project_path)
file_manager.deleteProject()
data = parser.parse_yaml_config(config_file)
file_manager.createGolangProjectTemplate()

# sqlc
sql_maker.query_sql_generator(project_path, data['handlers'])
sql_maker.schema_file(project_path, data['schema_file'])
sql_maker.sqlc_generate(project_path)

# handler
handler_maker.generateHandlers(project_path, data['handlers'])

# server
server_maker.ServerMaker(project_path, data['handlers'])

print("done")


