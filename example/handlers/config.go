package handlers

import (
	"database/sql"

	"example.com/crud/models"
)

var Db *sql.DB
var Client *models.Queries
