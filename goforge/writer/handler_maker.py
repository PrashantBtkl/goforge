import os
import logging
from jinja2 import Environment, FileSystemLoader

class HandlerMaker:
    def __init__(self, project_path, handler):
        self.project_path = project_path
        self.model_name = handler['sql']['name']
        self.name = handler['name']
        self.path = handler['path']
        self.method = handler['request']['method']
        self.request_params = self._requestParams()
        self.file_path = self._createHandlerFile()
        self.has_params = self._hasParams(handler['sql']['query'])
        self.sql_returns = self._sqlReturns(handler['sql']['annotation'])
        self._createConfig()

    def _hasParams(self, sql):
        for ch in sql:
            if ch == '$':
                return True
        return False

    def _sqlReturns(self, annotation):
        if annotation == 'exec':
            return False
        return True

    def _requestParams(self):
        return self.model_name[0].upper() + self.model_name[1:] + "Params"

    def _createHandlerFile(self):
        file_name =  ''.join(['_' + ch.lower() if i > 0 and ch.isupper() else ch.lower() for i, ch in enumerate(self.name)])
        # we already change our working directory while we generate sqlc.yml file
        # TODO: generalize current folder location
        file_path = os.path.join('handlers', f"{file_name}.go")
        try:
            with open(file_path, 'w') as f:
                f.write('package handlers\n\n')
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        return file_path

    # TODO: refactor db initialization
    def _createConfig(self):
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
            logging.error(f"An error occurred: {e}")

    def generate_handler(self):
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
            logging.error(f"An error occurred: {e}")

    def _get_request_binding(self):
        if not self.has_params:
            return ""
        return f"""
    var request models.{self.request_params}
    if err := c.Bind(&request); err != nil {{
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }}"""

    def _get_query_execution(self):
        context = "c.Request().Context()"
        query_call = f"s.Queries.{self.model_name}"
        
        if self.has_params:
            args = f"{context}, request"
        else:
            args = context

        if self.sql_returns:
            return f"\n    response, err := {query_call}({args})"
        else:
            return f"\n    err := {query_call}({args})"

    def _get_response(self):
        error_handling = """
    if err != nil {
        s.Logger.Error("failed to execute sql", "err", err.Error())
        return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
    }"""
        
        if self.sql_returns:
            return f"{error_handling}\n    return c.JSON(http.StatusOK, response)"
        else:
            return f"{error_handling}\n    return c.JSON(http.StatusOK, nil)"

def GenerateHandlers(project_path, handlers):
    for handler in handlers:
        HandlerMaker(project_path, handler).generate_handler()

