package handlers


func GetUsers(c echo.Context) error {
	request := new(models.GetUsersParams})
	if err := c.Bind(request); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
    response, err := models.GetUsers(c.Request().Context(), request)
    if err != nil {
		return echo.NewHTTPError(http.StatusInternalServer, err.Error())
    }
	return c.JSON(http.StatusOK, response)
}