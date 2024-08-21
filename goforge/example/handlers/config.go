package handlers

import (
	"database/sql"

	"github.com/gamezop/quizzop_api/models"
)

var Db *sql.DB
var Client *models.Queries
