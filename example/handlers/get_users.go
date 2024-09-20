package handlers

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func (s *Server) GetUsers(c echo.Context) error {

	response, err := s.Queries.GetUsers(c.Request().Context())

	if err != nil {
		s.Logger.Error("failed to execute sql", "err", err.Error())
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, response)
}
