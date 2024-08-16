package handlers

import (
	"net/http"
	// TODO: replace hardcoded models import
	"example.com/crud/models"
	"github.com/labstack/echo/v4"
)

func UpdateUser(c echo.Context) error {
	request := new(models.UpdateUserNameParams)
	if err := c.Bind(request); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	response, err := models.UpdateUserName(c.Request().Context(), request)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServer, err.Error())
	}
	return c.JSON(http.StatusOK, response)
}
