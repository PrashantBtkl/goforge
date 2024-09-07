import yaml
import os
import logging
import subprocess
from jinja2 import Environment, FileSystemLoader

class SqlMaker:
    def __init__(self, project_path: str, rules) -> None:
        self.project_path = project_path
        self.handlers = rules['handlers']
        self.schema_file = rules['schema_file']
        self.sqlcfile_path = os.path.join(project_path, "sqlc.yml") 
        self.sqlc_queries_path = ""
        self.schema_file_path = ""

        self._populateSqlPaths()

    def _populateSqlPaths(self):
        try:
            with open(self.sqlcfile_path, 'r') as file:
                data = yaml.safe_load(file)
            self.sqlc_queries_path = os.path.join(self.project_path, data['sql'][0]['queries'])
            self.schema_file_path = data['sql'][0]['schema']
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file: {e}")
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def Make(self):
        self.querySqlGenerator()
        self.schemaFile()
        self.createPostgresDb()
        self.sqlcGenerate()

    def querySqlGenerator(self):
        querysql = ""
        for handler in self.handlers:
            sql = handler['sql']
            sqlstr = f"-- name: {sql['name']} :{sql['annotation']}\n{sql['query']};\n\n"
            querysql += sqlstr
    
        try:
            with open(self.sqlc_queries_path, 'w') as file:
                file.write(querysql)
    
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def schemaFile(self):
        try:
            with open(self.schema_file, 'r') as source_file:
                contents = source_file.read()
                schema_path = os.path.join(self.project_path, self.schema_file_path)
                f = open(schema_path, 'w')
                f.write(contents)
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def createPostgresDb(self):
        docker_compose_template = """services:
   postgres:
     image: postgres:16
     restart: unless-stopped
     environment:
       - POSTGRES_USER=postgres
       - POSTGRES_PASSWORD=postgres
     ports:
       - "5432:5432"
     volumes:
       - ./{{schema_file_path}}:/docker-entrypoint-initdb.d/create_tables.sql"""

        env = Environment(loader=FileSystemLoader(""))
        template = env.from_string(docker_compose_template)
        rendered_template = template.render(schema_file_path=self.schema_file_path)
        f = open(os.path.join(self.project_path, 'docker-compose.yml'), 'w')
        f.write(rendered_template)

    def sqlcGenerate(self):
        # TODO: there should be a better way to do this
        os.chdir(self.project_path)
    
        result = subprocess.run(['sqlc', 'generate'], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error("Error:", result.stderr)
