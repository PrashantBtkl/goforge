import os
import logging
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
    "log/slog"
    "database/sql"
	"github.com/labstack/echo/v4"
    _ "github.com/lib/pq"
)


func main() {
	e := echo.New()
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	// TODO: should be configurable from config yaml
	connStr := "host=localhost port=5432 user=postgres dbname=postgres password=postgres sslmode=disable"
	var err error
	Db, err := sql.Open("postgres", connStr)
	if err != nil {
        logger.Error("failed to connect to postgres database", "err", err.Error())
        panic(err)
	}
	defer Db.Close()
	s := handlers.New(Db, logger)

    {% for route in routes %}
    e.{{route.method}}("{{route.path}}", s.{{route.handler}})
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
            logging.error(f"An error occurred while writing to main: {e}")

    # assumes current directory is in project
    def initializeProject(self):
        result = subprocess.run(['go', 'mod', 'init', self.project_mod], capture_output=True, text=True)
        logging.info("initiated golang project: %s", self.project_mod)
        if result.returncode != 0:
            logging.error("Error:", result.stderr)
        result = subprocess.run(['go', 'mod', 'tidy'], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error("Error:", result.stderr)
        result = subprocess.run(['goimports', '-w', '-v', '.'], capture_output=True, text=True)
        if result.returncode != 0:
            logging.error("Error:", result.stderr)
        result = subprocess.run(['docker', 'compose', 'up', '-d'], capture_output=True, text=True)
        logging.info("setting up postgres docker")
        if result.returncode != 0:
            logging.error("Error:", result.stderr)





