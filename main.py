from agents import sql_maker
import parser
from file_manager.file_manager import FileManager

project_path = "example"
config_file = "./example.yml"

file_manager = FileManager(project_path)
file_manager.deleteProject()
data = parser.parse_yaml_config(config_file)
file_manager.createGolangProjectTemplate()

# sqlc
sql_maker.query_sql_generator.query_sql_generator(project_path, data['handlers'])
sql_maker.query_sql_generator.schema_file(project_path, data['schema_file'])
sql_maker.query_sql_generator.sqlc_generate(project_path)

print("done")


