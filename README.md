<p align="center">

<h1 align="center">GoForge</h1>

<p align="center">

 <div align="center">
	 
[![PyPi package version](https://img.shields.io/pypi/v/goforge)](https://pypi.org/project/goforge/)	 
[![PyPi downloads](https://static.pepy.tech/badge/goforge)](https://pypi.org/project/goforge/)
[![PyPI version](https://img.shields.io/pypi/pyversions/goforge?color=%2344CC11&style=flat-square)](https://pypi.org/project/goforge/)
<br>
generate entire CRUD backend for golang echo and postgres with one command 💙
</div>
    
## Description
 This tool is designed to be used for starting a project and editing the files later. It uses sqlc to generate all the sql related code. Make sure sqlc, goimports, gofmt, and docker are installed.

 ## Prerequisites
 ```bash
snap install sqlc
go install golang.org/x/tools/cmd/goimports@latest
```

 ## Installation
 ```bash
pip install goforge
```
## Quick start
generate the project code
```bash
$ goforge -c example.yml
```
delete the project
```bash
$ goforge -c example.yml -d
```

## API Configuration Documentation

edit the yaml as per your requirements
```yaml
project_path: "example" # specifies the root directory for the project
schema_file: "example.sql" # defines the sql schema file for the project
project_mod: "example.com/my_crud_app" # go.mod project name
setup_postgres_local: true # setups a postgres docker instance for seamless testing
handlers:
  - name: CreateUser # handler function name
    path: "/v1/api/user" # api path
    sql:
       name: CreateUser # sqlc model method name
       annotation: exec # annotations compatible with sqlc, for eg: "one", "many" and "exec"
       query: "INSERT INTO users (name, email) VALUES ($1, $2)"
    request:
       method: "POST"
  - name: GetUsers
    path: "/v1/api/users"
    sql:
      name: GetUsers
      annotation: many
      query: "SELECT id, name, email FROM users LIMIT $1 AND OFFSET $2"
    request:
      method: "GET"
