import os
import shutil
class FileManager:
    def __init__(self, project_path):
        self.project_path = project_path

    def deleteProject(self):
        try:
            shutil.rmtree(self.project_path)
            print(f"Folder '{self.project_path}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting folder: {e}")
    
    def createGolangProjectTemplate(self):
        os.mkdir(self.project_path)
    
        api_dir = os.path.join(self.project_path, 'api')
        os.mkdir(api_dir)
    
        handlers_dir = os.path.join(api_dir, 'handlers')
        os.mkdir(handlers_dir)
    
        models_dir = os.path.join(self.project_path, 'models')
        os.mkdir(models_dir)
    
        routes_file = os.path.join(api_dir, 'routes.go')
        with open(routes_file, 'w') as f:
            f.write('package api\n')
    
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
        output_db_file_name: "db.gen"
        output_models_file_name: "models.gen"
        output_files_suffix: ".gen"
                    """)

