import os
import subprocess
from jinja2 import Environment, FileSystemLoader

class ServerMaker:
    def __init__(self, project_path, project_mod, handlers):
        self.project_path = project_path
        self.project_mod = project_mod
        self.handlers = handlers
        self.routes = []
        self._generate_routes()

    def _generate_routes(self):
        for handler in self.handlers:
            route = dict(path=handler['path'], method= handler['request']['method'], handler= handler['name'])
            self.routes.append(route)

    def Make(self):
        self.createMainServer()
        self.initializeProject()

    def createMainServer(self):
        template_str = """
package main

import (
    "database/sql"
	"github.com/labstack/echo/v4"
    _ "github.com/lib/pq"
)


func main() {
	e := echo.New()
    // TODO: refactor db initilization
    connStr := "host=localhost port=5432 user=postgres dbname=postgres password=postgres sslmode=disable"
    var err error
    handlers.Db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
	defer handlers.Db.Close()
	handlers.Client = models.New(handlers.Db)

    {% for route in routes %}
    e.{{route.method}}("{{route.path}}", handlers.{{route.handler}})
    {% endfor %}
    
	e.Logger.Fatal(e.Start(":8080"))
    }
"""
        env = Environment(loader=FileSystemLoader(""))
        template = env.from_string(template_str)
        rendered_template = template.render(routes=self.routes)
        #main_file = os.path.join('handlers', f"{file_name}.go")
        try:
            # we already change our working directory while we generate sqlc.yml file
            # TODO: generalize current folder location
            with open("main.go", 'w') as f:
                f.write(rendered_template)
        except Exception as e:
            print(f"An error occurred while writing to main: {e}")

    # assumes current directory is in project
    def initializeProject(self):
        # TODO: make project name customizable
        result = subprocess.run(['go', 'mod', 'init', self.project_mod], capture_output=True, text=True)
        print("initiated golang project:", self.project_mod)
        if result.returncode != 0:
            print("Error:", result.stderr)
        result = subprocess.run(['go', 'mod', 'tidy'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error:", result.stderr)
        result = subprocess.run(['gofmt', '.'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error:", result.stderr)
        result = subprocess.run(['goimports', '-w', '.'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error:", result.stderr)
        result = subprocess.run(['docker', 'compose', 'up', '-d'], capture_output=True, text=True)
        print(result.stdout, result.stderr)
        if result.returncode != 0:
            print("Error:", result.stderr)





