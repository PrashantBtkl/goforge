
from agents import sql_maker
import parser
import coder

project_path = "example"
config_file = "./example.yml"

coder.delete_project(project_path)
data = parser.parse_yaml_config(config_file)
coder.create_golang_project_template(project_path)

# sqlc
sql_maker.query_sql_generator.query_sql_generator(project_path, data['handlers'])
sql_maker.query_sql_generator.schema_file(project_path, data['schema_file'])
sql_maker.query_sql_generator.sqlc_generate(project_path)

print("done")


