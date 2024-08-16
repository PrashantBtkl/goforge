import os
from string import Template

class HandlerMaker:
    def __init__(self, project_path, handler):
        self.project_path = project_path
        self.model_name = handler['sql']['name']
        self.name = handler['name']
        self.path = handler['path']
        self.method = handler['request']['method']
        self.request_params = self._requestParams(self.model_name)
        self.file_path = self._createHandlerFile(self.name)

    def _requestParams(self, model_name):
        return model_name[0].upper() + model_name[1:] + "Params"

    def _createHandlerFile(self, name):
        file_name =  ''.join(['_' + ch.lower() if i > 0 and ch.isupper() else ch.lower() for i, ch in enumerate(name)])
        # we already change our working directory while we generate sqlc.yml file
        # TODO: generalize current folder location
        file_path = os.path.join('handlers', f"{file_name}.go")
        try:
            with open(file_path, 'w') as f:
                f.write('package handlers\n\n')
        except Exception as e:
            print(f"An error occurred: {e}")

        return file_path


    # TODO: create different templates for GET, POST, DELETE, ... methods
    # TODO: check if sql has returns
    def genrateHandler(self):
        handler_template = """
import (
    "net/http"
    // TODO: replace hardcoded models import
    "example.com/crud/models"
	"github.com/labstack/echo/v4"
)

func $name(c echo.Context) error {
	request := new(models.$request_params)
	if err := c.Bind(request); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
    response, err := models.$model_name(c.Request().Context(), request)
    if err != nil {
		return echo.NewHTTPError(http.StatusInternalServer, err.Error())
    }
	return c.JSON(http.StatusOK, response)
}"""
        template = Template(handler_template)
        result = template.substitute(name=self.name, request_params= self.request_params, model_name=self.model_name)
        try:
            with open(self.file_path, 'a') as f:
                f.write(result)
        except Exception as e:
            print(f"An error occurred: {e}")

def generateHandlers(project_path, handlers):
    for handler in handlers:
        HandlerMaker(project_path, handler).genrateHandler()

