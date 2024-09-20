package handlers

import (
	"net/http"

	"example.com/crud/models"
	"github.com/labstack/echo/v4"
)

func (s *Server) CreateUser(c echo.Context) error {

	var request models.CreateUserParams
	if err := c.Bind(&request); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	err := s.Queries.CreateUser(c.Request().Context(), request)

	if err != nil {
		s.Logger.Error("failed to execute sql", "err", err.Error())
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, nil)
}
