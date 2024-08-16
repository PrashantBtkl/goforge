import os
from jinja2 import Environment, FileSystemLoader

class ServerMaker:
    def __init__(self, project_path, handlers):
        self.project_path = project_path
        self.handlers = handlers
        self._generate_routes()
        self.createMainServer()

    def _generate_routes(self):
        self.routes = []
        for handler in self.handlers:
            route = dict(path=handler['path'], method= handler['request']['method'], handler= handler['name'])
            self.routes.append(route)
        


    def createMainServer(self):
        template_str = """
package main

import (
	"github.com/labstack/echo/v4"
)


func main() {
	e := echo.New()

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

