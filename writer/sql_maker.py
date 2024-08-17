import yaml
import os
import subprocess
from jinja2 import Environment, FileSystemLoader

def query_sql_generator(project_path, handlers):
    querysql = ""
    for handler in handlers:
        sql = handler['sql']
        sqlstr = f"-- name: {sql['name']} :{sql['annotation']}\n{sql['query']};\n\n"
        querysql += sqlstr

    try:
        # TODO: store data in object instead of loading from yml
        sqlcfile = os.path.join(project_path, "sqlc.yml")
        with open(sqlcfile, 'r') as file:
            data = yaml.safe_load(file)
        f = open(os.path.join(project_path, data['sql'][0]['queries']), 'w')
        f.write(querysql)

    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def schema_file(project_path, source_path):
    try:
        with open(source_path, 'r') as source_file:
            contents = source_file.read()
        sqlcfile = os.path.join(project_path, "sqlc.yml")
        # TODO: store data in object instead of loading from yml
        with open(sqlcfile, 'r') as file:
            data = yaml.safe_load(file)
            schema_file_path = data['sql'][0]['schema']
            schema_path = os.path.join(project_path, schema_file_path)
            f = open(schema_path, 'w')
            f.write(contents)
            createPostgresDb(project_path, schema_file_path)

        print(f"Contents copied from {source_path} to {sqlcfile}")

    except IOError as e:
        print(f"An error occurred: {e}")

def createPostgresDb(project_path, schema_file_path):
    docker_compose_template = """
services:
  postgres:
    image: postgres:16
    restart: unless-stopped
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
    volumes:
      - ./{{schema_file_path}}:/docker-entrypoint-initdb.d/create_tables.sql
      """
    env = Environment(loader=FileSystemLoader(""))
    template = env.from_string(docker_compose_template)
    rendered_template = template.render(schema_file_path=schema_file_path)
    f = open(os.path.join(project_path, 'docker-compose.yml'), 'w')
    f.write(rendered_template)

def sqlc_generate(project_path):
    os.chdir(project_path)
    result = subprocess.run(['sqlc', 'generate'], capture_output=True, text=True)
    
    # Print the output
    print(result.stdout)
    
    # Check if there were any errors
    if result.returncode != 0:
        print("Error:", result.stderr)
