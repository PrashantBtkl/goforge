<p align="center">

<h1 align="center">GoForge</h1>

<p align="center">

 <div align="center">
	 
[![PyPi package version](https://img.shields.io/pypi/v/goforge)](https://pypi.org/project/goforge/)	 
[![PyPi downloads](https://static.pepy.tech/badge/goforge)](https://pypi.org/project/goforge/)
[![PyPI version](https://img.shields.io/pypi/pyversions/goforge?color=%2344CC11&style=flat-square)](https://pypi.org/project/goforge/)

<br>
    generate the entire CRUD backend for golang echo and postgres with one command
 </div>
    <br>
    <br>
    
## Description
 This tool is designed to be used for starting a project and editing the files later. It uses sqlc to generate all the sql related code. Make sure sqlc, goimports, gofmt, and docker are installed.

 ## Installation
 ```bash
pip install goforge
```
## Quick start
```bash
$ goforge --config-file example.yml

INFO: Folder 'example' deleted successfully.
INFO: initiated golang project: example.com/crud
INFO: setting up postgres docker
INFO: your project has been created
```

## API Configuration Documentation

edit the yaml as per your requirements
```yaml
project_path: "example" # specifies the root directory for the project
schema_file: "example.sql" # defines the sql schema file for the project
project_mod: "example.com/my_crud_app" # go.mod project name
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
      query: "SELECT id, name, email FROM users"
    request:
      method: "GET"
```
