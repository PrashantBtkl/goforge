package main

import (
	"database/sql"
	"log/slog"
	"os"

	"example.com/crud/handlers"
	"github.com/labstack/echo/v4"
	_ "github.com/lib/pq"
)

func main() {
	e := echo.New()
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	// TODO: take from env
	connStr := "host=localhost port=5432 user=postgres dbname=postgres password=postgres sslmode=disable"
	var err error
	Db, err := sql.Open("postgres", connStr)
	if err != nil {
		logger.Error("failed to connect to postgres database", "err", err.Error())
		panic(err)
	}
	defer Db.Close()
	s := handlers.New(Db, logger)

	e.PATCH("/v1/api/user", s.UpdateUser)
	e.POST("/v1/api/user", s.CreateUser)
	e.GET("/v1/api/users", s.GetUsers)

	e.Logger.Fatal(e.Start(":8080"))
}
