import os
import shutil
import logging

class FileManager:
    """
    A class for managing Go project file structure and operations.

    This class handles creation and deletion of Go project templates,
    including setting up standard directories and configuration files.

    Attributes:
        project_path (str): The relative path to the project directory
        full_path (str): The absolute path to the project directory
    """

    def __init__(self, project_path):
        """
        Initialize the FileManager with a project path.

        Args:
            project_path (str): The path where the project will be created
        """
        self.project_path = project_path
        self.full_path = os.path.abspath(project_path)

    def delete_project(self, exception=False):
        """
        Delete the project directory and all its contents.

        Args:
            exception (bool, optional): If True, indicates deletion is due to an 
                                      exception during creation. Defaults to False.

        Logs:
            - Info message about project deletion
            - Success message upon successful deletion
            - Error message if deletion fails
        """
        if exception:
            logging.info("deleting your project since an exception occurred while creation: %s", self.full_path)
        else:
            logging.info("deleting your project: %s", self.full_path)
        try:
            shutil.rmtree(self.full_path)
            logging.info("Folder '%s' deleted successfully.", self.project_path)
        except Exception as e:
            logging.error("Error deleting folder: %s", e)
    
    def create_golang_project_template(self):
        """
        Create a standard Go project directory structure.

        Creates the following structure:
        - project_path/
            - handlers/
            - models/
            - main.go
            - sqlc.yml

        The main.go file is initialized with a basic package declaration.
        Also sets up SQLC configuration through _create_sqlc().
        """
        os.mkdir(self.project_path)
        handlers_dir = os.path.join(self.project_path, 'handlers')
        os.mkdir(handlers_dir)
        models_dir = os.path.join(self.project_path, 'models')
        os.mkdir(models_dir)
        main_file = os.path.join(self.project_path, 'main.go')
        with open(main_file, 'w') as f:
            f.write('package main\n')
        self._create_sqlc()
    
    def _create_sqlc(self):
        """
        Create SQLC configuration file with PostgreSQL settings.

        Creates a sqlc.yml file in the project root with standard configuration
        for PostgreSQL database, including schema and query paths, and various
        code generation options for Go.
        """
        sqlc_file = os.path.join(self.project_path, 'sqlc.yml')
        with open (sqlc_file, 'w') as f:
            f.write("""version: "2"
sql:
  - engine: "postgresql"
    schema: "models/schema.sql"
    queries: "models/queries.sql"
    gen:
      go:
        package: "models"
        out: "./models"
        emit_empty_slices: true
        emit_json_tags: true
        emit_pointers_for_null_types: true
        emit_prepared_queries: true
        omit_unused_structs: true
        output_db_file_name: "db"
        output_models_file_name: "models"
                    """)
