import os
import shutil
import logging

class FileManager:
    def __init__(self, project_path):
        self.project_path = project_path

    #TODO: By default project shouldnt be deleted
    def deleteProject(self):
        try:
            shutil.rmtree(self.project_path)
            logging.info(f"Folder '{self.project_path}' deleted successfully.")
        except Exception as e:
            logging.error(f"Error deleting folder: {e}")
    
    def createGolangProjectTemplate(self):
        os.mkdir(self.project_path)
    
        handlers_dir = os.path.join(self.project_path, 'handlers')
        os.mkdir(handlers_dir)
    
        models_dir = os.path.join(self.project_path, 'models')
        os.mkdir(models_dir)
    
        main_file = os.path.join(self.project_path, 'main.go')
        with open(main_file, 'w') as f:
            f.write('package main\n')
    
        self._createSqlc()
    
    
    def _createSqlc(self):
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

