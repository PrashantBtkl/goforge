import logging
import subprocess
from jinja2 import Environment, FileSystemLoader

class ServerMaker:
    """
    A class to generate and initialize a Go server with Echo framework.

    Handles server setup, database configuration, route generation, and project initialization.

    Attributes:
        project_path (str): Path to the project root
        project_mod (str): Go module name
        setup_postgres_local (bool): Whether to setup local Postgres via Docker
        db (dict): Database configuration
        handlers (list): List of API handler configurations
        routes (list): Generated route configurations
    """
    def __init__(self, project_path, project_mod, db, handlers):
        self.project_path = project_path
        self.project_mod = project_mod
        self.setup_postgres_local = db['setup_postgres_local']
        self.db = self._create_db_config(db)
        self.handlers = handlers
        self.routes = []
        self._generate_routes()

    def _generate_routes(self):
        """
        Generate route configurations from handler definitions.
        Each route contains path, HTTP method, and handler name.
        """
        for handler in self.handlers:
            route = dict(
                path=handler['path'],
                method=handler['request']['method'],
                handler=handler['name']
            )
            self.routes.append(route)

    def _create_db_config(self, db) -> dict:
        """
        Create database configuration dictionary.

        Args:
            db (dict): Raw database configuration

        Returns:
            dict: Processed database configuration

        Raises:
            Exception: If required database configuration is missing
        """
        if self.setup_postgres_local:
            return dict(
                host='localhost',
                port=5432,
                user='postgres',
                dbname='postgres',
                password='postgres'
            )
        required_configs = ['host', 'port', 'user', 'dbname', 'password']
        for config in required_configs:
            if config not in db:
                raise Exception(f"database config is missing '{config}'")
        return dict(
            host=db['host'],
            port=db['port'],
            user=db['user'],
            dbname=db['dbname'],
            password=db['password']
        )

    def make(self):
        """
        Execute the server creation process.
        Creates main server file and initializes the project.
        """
        self.create_main_server()
        self.initialize_project()

    def create_main_server(self):
        """
        Generate the main server file with Echo setup, database connection,
        and route definitions.
        """
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
    // TODO: take from env
    connStr := "host={{db.host}} port={{db.port}} user={{db.user}} dbname={{db.dbname}} password={{db.password}} sslmode=disable"
    var err error
    Db, err := sql.Open("postgres", connStr)
    if err != nil {
        logger.Error("failed to connect to postgres database", "err", err.Error())
        panic(err)
    }
    defer Db.Close()
    s := handlers.New(Db, logger)
    {% for route in routes %}
    e.{{route.method}}("{{route.path}}", s.{{route.handler}}){% endfor %}
    
    e.Logger.Fatal(e.Start(":8080"))
}
"""
        env = Environment(loader=FileSystemLoader(""))
        template = env.from_string(template_str)
        rendered_template = template.render(db=self.db, routes=self.routes)
        try:
            with open("main.go", 'w') as f:
                f.write(rendered_template)
        except Exception as e:
            logging.error("An error occurred while writing to main: %s", e)

    def initialize_project(self):
        """
        Initialize the Go project with modules, dependencies, and formatting.
        Sets up local Postgres if configured.
        """
        commands = [
            (['go', 'mod', 'init', self.project_mod], "initiated golang project: %s"),
            (['go', 'mod', 'tidy'], None),
            (['goimports', '-w', '-v', '.'], None),
            (['goimports', '-w', '.'], None)
        ]
        for cmd, success_msg in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if success_msg:
                logging.info(success_msg, self.project_mod)
            if result.returncode != 0:
                logging.error("Error: %s", result.stderr)

        if self.setup_postgres_local:
            result = subprocess.run(['docker', 'compose', 'up', '-d'], 
                                 capture_output=True, text=True)
            logging.info("initiated postgres: %s", result.stderr)
            if result.returncode != 0:
                logging.error("Error: %s", result.stderr)
