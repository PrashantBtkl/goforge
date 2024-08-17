package handlers

import (
	"net/http"
	// TODO: replace hardcoded models import

	"github.com/labstack/echo/v4"
)

func GetUsers(c echo.Context) error {
	response, err := Client.GetUsers(c.Request().Context())
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, response)
}
