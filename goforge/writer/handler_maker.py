import os
import logging
from jinja2 import Environment, FileSystemLoader

class HandlerMaker:
    """
    A class to generate Go HTTP handlers based on configuration.

    Generates handler files with appropriate request binding, query execution,
    and response handling for a Go web service using Echo framework.

    Attributes:
        project_path (str): Path to the project root
        model_name (str): Name of the database model
        name (str): Handler function name
        path (str): API endpoint path
        method (str): HTTP method
        request_params (str): Name of request parameters struct
        file_path (str): Path to generated handler file
        has_params (bool): Whether SQL query has parameters
        sql_returns (bool): Whether SQL query returns data
    """
    def __init__(self, project_path, handler):
        self.project_path = project_path
        self.model_name = handler['sql']['name']
        self.name = handler['name']
        self.path = handler['path']
        self.method = handler['request']['method']
        self.request_params = self._create_request_params()
        self.file_path = self._create_handler_file()
        self.has_params = self._has_params(handler['sql']['query'])
        self.sql_returns = self._sql_returns(handler['sql']['annotation'])
        self._create_config()

    def _has_params(self, sql):
        """
        Check if SQL query contains parameters.

        Args:
            sql (str): SQL query string

        Returns:
            bool: True if query contains parameters ($), False otherwise
        """
        for ch in sql:
            if ch == '$':
                return True
        return False

    def _sql_returns(self, annotation):
        """
        Determine if SQL query returns data based on annotation.

        Args:
            annotation (str): SQL query annotation

        Returns:
            bool: False if annotation is 'exec', True otherwise
        """
        if annotation == 'exec':
            return False
        return True

    def _create_request_params(self):
        """
        Create parameter struct name from model name.

        Returns:
            str: Capitalized model name with 'Params' suffix
        """
        return self.model_name[0].upper() + self.model_name[1:] + "Params"

    def _create_handler_file(self):
        """
        Create and initialize handler file with package declaration.

        Returns:
            str: Path to created handler file
        """
        file_name = ''.join(['_' + ch.lower() if i > 0 and ch.isupper() else ch.lower() 
                            for i, ch in enumerate(self.name)])
        file_path = os.path.join('handlers', f"{file_name}.go")
        try:
            with open(file_path, 'w') as f:
                f.write('package handlers\n\n')
        except Exception as e:
            logging.error("An error occurred: %s", e)

        return file_path

    def _create_config(self):
        """
        Create config.go file with Server struct definition and constructor.
        """
        file_path = os.path.join('handlers', "config.go")
        try:
            with open(file_path, 'w') as f:
                f.write("""
package handlers

import (
    "database/sql"
    "log/slog"
)

type Server struct {
    Queries *models.Queries
    Logger *slog.Logger
}

func New(db *sql.DB, logger *slog.Logger) *Server {
    return &Server{
        Queries: models.New(db),
        Logger: logger,
    }
}""")
        except Exception as e:
            logging.error("An error occurred: %s", e)

    def generate_handler(self):
        """
        Generate the complete handler function with request binding,
        query execution, and response handling.
        """
        handler_template = """
import (
    "net/http"
    "github.com/labstack/echo/v4"
)

func (s *Server) {{name}}(c echo.Context) error {
    {{request_binding}}
    {{query_execution}}
    {{response}}
}"""
        template_parts = {
            'request_binding': self._get_request_binding(),
            'query_execution': self._get_query_execution(),
            'response': self._get_response(),
        }
        env = Environment(loader=FileSystemLoader(""))
        template = env.from_string(handler_template)
        rendered_template = template.render(
            name=self.name,
            **template_parts
        )
        try:
            with open(self.file_path, 'a') as f:
                f.write(rendered_template)
        except Exception as e:
            logging.error("An error occurred: %s", e)

    def _get_request_binding(self) -> str:
        """
        Generate request binding code if handler has parameters.

        Returns:
            str: Request binding code or empty string
        """
        if not self.has_params:
            return ""
        return f"""
    var request models.{self.request_params}
    if err := c.Bind(&request); err != nil {{
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }}"""

    def _get_query_execution(self) -> str:
        """
        Generate query execution code with appropriate context and parameters.

        Returns:
            str: Query execution code
        """
        context = "c.Request().Context()"
        query_call = f"s.Queries.{self.model_name}"
        if self.has_params:
            args = f"{context}, request"
        else:
            args = context
        if self.sql_returns:
            return f"\n    response, err := {query_call}({args})"
        return f"\n    err := {query_call}({args})"

    def _get_response(self):
        """
        Generate response handling code with error checking.

        Returns:
            str: Response handling code
        """
        error_handling = """
    if err != nil {
        s.Logger.Error("failed to execute sql", "err", err.Error())
        return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
    }"""
        if self.sql_returns:
            return f"{error_handling}\n    return c.JSON(http.StatusOK, response)"
        return f"{error_handling}\n    return c.JSON(http.StatusOK, nil)"

def generate_handlers(project_path, handlers):
    """
    Generate handlers for all provided configurations, checking for duplicates.

    Args:
        project_path (str): Path to project root
        handlers (list): List of handler configurations

    Raises:
        Exception: If duplicate API endpoints are found
    """
    duplicates = set()
    for handler in handlers:
        endpoint = (handler['request']['method'], handler['path'])
        if endpoint in duplicates:
            raise Exception(f"duplicate api found with same path and method {str(endpoint)}")
        HandlerMaker(project_path, handler).generate_handler()
        duplicates.add(endpoint)
