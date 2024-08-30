package handlers

import (
	"database/sql"

	"example.com/crud/models"
)

type Server struct {
	Queries *models.Queries
}

func New(db *sql.DB) *Server {
	return &Server{
		Queries: models.New(db),
	}

}
