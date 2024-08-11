-- name: UpdateUserName :exec
update users set name = $1 where id = $2;

-- name: CreateUser :exec
insert into users (name, email) values ($1, $2);

-- name: GetUsers :many
select id, name, email from users;

