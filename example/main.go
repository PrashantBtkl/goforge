package main

import (
	"example.com/crud/handlers"
	"example.com/crud/models"
	"github.com/labstack/echo/v4"
)

func main() {
	e := echo.New()
	handlers.Client = models.New(handlers.Db)

	e.PATCH("/v1/api/user", handlers.UpdateUser)

	e.POST("/v1/api/user", handlers.CreateUser)

	e.GET("/v1/api/users/:id", handlers.GetUsers)

	e.Logger.Fatal(e.Start(":8080"))
}
