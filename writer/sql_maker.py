import yaml
import os
import subprocess

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
            f = open(os.path.join(project_path, data['sql'][0]['schema']), 'w')
            f.write(contents)

        print(f"Contents copied from {source_path} to {sqlcfile}")

    except IOError as e:
        print(f"An error occurred: {e}")

def sqlc_generate(project_path):
    os.chdir(project_path)
    result = subprocess.run(['sqlc', 'generate'], capture_output=True, text=True)
    
    # Print the output
    print(result.stdout)
    
    # Check if there were any errors
    if result.returncode != 0:
        print("Error:", result.stderr)
