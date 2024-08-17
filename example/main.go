package main

import (
	"database/sql"
	"log"

	"example.com/crud/handlers"
	"example.com/crud/models"
	"github.com/labstack/echo/v4"
	_ "github.com/lib/pq"
)

func main() {
	e := echo.New()
	// TODO: refactor db initilization
	connStr := "host=localhost port=5432 user=postgres dbname=postgres password=postgres sslmode=disable"
	var err error
	handlers.Db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
	defer handlers.Db.Close()
	handlers.Client = models.New(handlers.Db)

	e.PATCH("/v1/api/user", handlers.UpdateUser)

	e.POST("/v1/api/user", handlers.CreateUser)

	e.GET("/v1/api/users", handlers.GetUsers)

	e.Logger.Fatal(e.Start(":8080"))
}
