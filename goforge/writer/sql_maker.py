import os
import logging
import subprocess

import yaml
from jinja2 import Environment, FileSystemLoader

class SqlMaker:
    """
    A class to generate SQL-related files and setup database for a Go project.

    Handles SQL query generation, schema setup, Docker composition for Postgres,
    and SQLC code generation.

    Attributes:
        project_path (str): Path to the project root
        handlers (list): List of API handler configurations
        schema_file (str): Path to the source schema file
        sqlcfile_path (str): Path to SQLC configuration file
        sqlc_queries_path (str): Path to generated SQL queries
        schema_file_path (str): Path to schema file in project
    """
    def __init__(self, project_path: str, rules) -> None:
        self.project_path = project_path
        self.handlers = rules['handlers']
        self.schema_file = rules['schema_file']
        self.sqlcfile_path = os.path.join(project_path, "sqlc.yml")
        self.sqlc_queries_path = ""
        self.schema_file_path = ""
        self._populate_sql_paths()

    def _populate_sql_paths(self):
        """
        Extract SQL file paths from SQLC configuration file.
        Sets paths for queries and schema files.
        """
        try:
            with open(self.sqlcfile_path, 'r') as file:
                data = yaml.safe_load(file)
            self.sqlc_queries_path = os.path.join(self.project_path, data['sql'][0]['queries'])
            self.schema_file_path = data['sql'][0]['schema']
        except yaml.YAMLError as e:
            logging.error("Error parsing YAML file: %s", e)
        except FileNotFoundError as e:
            logging.error("File not found: %s", e)
        except Exception as e:
            logging.error("An error occurred: %s", e)

    def make(self):
        """
        Execute the complete SQL setup process.
        Generates queries, sets up schema, creates database, and runs SQLC.
        """
        self.generate_query_sql()
        self.create_schema_file()
        self.create_postgres_db()
        self.generate_sqlc()

    def generate_query_sql(self):
        """
        Generate SQL query file from handler configurations.
        Creates SQLC-compatible query definitions.
        """
        querysql = ""
        for handler in self.handlers:
            sql = handler['sql']
            sqlstr = f"-- name: {sql['name']} :{sql['annotation']}\n{sql['query']};\n\n"
            querysql += sqlstr
        try:
            with open(self.sqlc_queries_path, 'w') as file:
                file.write(querysql)
        except FileNotFoundError as e:
            logging.error("File not found: %s", e)
        except Exception as e:
            logging.error("An error occurred: %s", e)

    def create_schema_file(self):
        """
        Copy schema file to project directory.
        """
        try:
            with open(self.schema_file, 'r') as source_file:
                contents = source_file.read()
                schema_path = os.path.join(self.project_path, self.schema_file_path)
                with open(schema_path, 'w') as f:
                    f.write(contents)
        except Exception as e:
            logging.error("An error occurred: %s", e)

    def create_postgres_db(self):
        """
        Generate Docker Compose configuration for PostgreSQL.
        Sets up database container with schema initialization.
        """
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
        compose_path = os.path.join(self.project_path, 'docker-compose.yml')
        with open(compose_path, 'w') as f:
            f.write(rendered_template)

    def generate_sqlc(self):
        """
        Run SQLC code generation.
        Changes to project directory before running command.
        """
        os.chdir(self.project_path)
        result = subprocess.run(['sqlc', 'generate'], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error("Error: %s", result.stderr)
