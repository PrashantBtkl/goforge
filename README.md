<p align="center">

<h1 align="center">GoForge</h1>

<p align="center">

 <div align="center">
	 
[![PyPi package version](https://img.shields.io/pypi/v/goforge)](https://pypi.org/project/goforge/)	 
[![PyPi downloads](https://static.pepy.tech/badge/goforge)](https://pypi.org/project/goforge/)
[![PyPI version](https://img.shields.io/pypi/pyversions/goforge?color=%2344CC11&style=flat-square)](https://pypi.org/project/goforge/)
 </div>
<br>
    generate the entire CRUD backend for golang echo and postgres with one command
    <br />
    <br />
    
## Description
 This tool is designed to be used for starting a project and editing the files later. It uses sqlc to generate all the sql related code. Make sure sqlc, goimports, gofmt, and docker are installed.

 ## Installation
 ```bash
pip install goforge
```
## Quick start
```bash
$ goforge --config-file example.yml

Folder 'example' deleted successfully.
initiated golang project: example.com/crud
Container example-postgres-1  Created
done
```

## API Configuration Documentation

edit the yaml as per your requirements
```yaml
project_path: "example"
schema_file: "example.sql"
project_mod: "example.com/crud"
handlers:
  - name: CreateUser
    path: "/v1/api/user"
    sql:
       name: CreateUser
       annotation: exec
       query: "insert into users (name, email) values ($1, $2)"
    request:
       method: "POST"
  - name: GetUsers
    path: "/v1/api/users"
    sql:
      name: GetUsers
      annotation: many
      query: "select id, name, email from users"
    request:
      method: "GET"
```

This document describes the configuration for an API project using a YAML file.

-   `project_path`: Specifies the root directory for the project.
-   `schema_file`:  Defines the SQL schema file for the project.
-  `handlers`: The configuration defines API handlers
	-  `name` : name of handler in PascalCase
	- `path` : api path
	- `sql` : configuration for sql queries
		-  `name` : name of sql query function
		- `annotation` : ranges from "one", "many" and "exec"
		- `query` : sql query with variable params syntax of psql
	- `request.method` : defines the http verb of the api path
