package handlers


func CreateUser(c echo.Context) error {
	request := new(models.CreateUserParams})
	if err := c.Bind(request); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
    response, err := models.CreateUser(c.Request().Context(), request)
    if err != nil {
		return echo.NewHTTPError(http.StatusInternalServer, err.Error())
    }
	return c.JSON(http.StatusOK, response)
}