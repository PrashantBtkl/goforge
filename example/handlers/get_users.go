package handlers

import (
	"net/http"

	"example.com/crud/models"
	"github.com/labstack/echo/v4"
)

func GetUsers(c echo.Context) error {

	var request models.GetUsersParams
	if err := c.Bind(&request); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	response, err := Client.GetUsers(c.Request().Context(), request)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}

	return c.JSON(http.StatusOK, response)

}
