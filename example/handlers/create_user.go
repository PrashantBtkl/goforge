package handlers

import (
	"net/http"
	// TODO: replace hardcoded models import
	"example.com/crud/models"
	"github.com/labstack/echo/v4"
)

func CreateUser(c echo.Context) error {

	var request models.CreateUserParams
	if err := c.Bind(&request); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	err := Client.CreateUser(c.Request().Context(), request)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}

	return c.JSON(http.StatusOK, nil)

}
