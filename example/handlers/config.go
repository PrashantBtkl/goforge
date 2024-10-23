package handlers

import (
	"database/sql"
	"log/slog"

	"example.com/crud/models"
)

type Server struct {
	Queries *models.Queries
	Logger  *slog.Logger
}

func New(db *sql.DB, logger *slog.Logger) *Server {
	return &Server{
		Queries: models.New(db),
		Logger:  logger,
	}

}
