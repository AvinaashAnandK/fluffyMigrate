from pathlib import Path
import pandas as pd
import ast 
import logging

from .parserutils import python_imports_mapper
from .utils import get_classification_report

def compile_imports_map(git_url):
    fileClassificationReportPath = get_classification_report(git_url)
    file_df = pd.read_csv(str(fileClassificationReportPath))

    def imports_mapper_handler(row):
        try:
            if row['extension'] in ['.py', '.ipynb']:
                return python_imports_mapper(row['filepath'], git_url)
            return ""
        except Exception as e:
            logging.error(f"Error processing file {row['filepath']}: {e}")
            return ""

    file_df['imports_map'] = file_df.apply(imports_mapper_handler, axis=1)

    file_df.fillna("", inplace=True)
    file_df.to_csv(str(fileClassificationReportPath), index=False)

def compile_dependancy_map(git_url):
    fileClassificationReportPath = get_classification_report(git_url)
    file_df = pd.read_csv(str(fileClassificationReportPath))

    dependancy_import_types = {
        '.py': {
            'Python File Import': 'imports file',
            'Entity within Python File Import': 'imports module',
            'Init.py imports': 'init.py further depends on other files'
        },
        '.ipynb': {
            'Python File Import': 'imports file',
            'Entity within Python File Import': 'imports module',
            'Init.py imports': 'init.py further depends on other files'
        }
    }

    def dependancy_mapper_handler(row):
        if pd.isna(row['imports_map']):
            return ""  # or handle it in a way that makes sense for your context

        try:
            imports_list = ast.literal_eval(row['imports_map'])
            extension = row['extension']
            dependant_files = []

            for _import in imports_list:
                import_path_clean = _import['import_path_clean']
                import_type = _import['import_type']

                if import_type in dependancy_import_types.get(extension, {}):
                    filtered_df = file_df[file_df['filepath'].str.endswith(import_path_clean)]
                    if len(filtered_df) > 0:
                        node_path = filtered_df['filepath'].iloc[0]
                        result = {
                            'node': node_path.split("/repos/")[1],
                            'node_desc': dependancy_import_types[extension][import_type]
                        }
                        dependant_files.append(result)

            return dependant_files if dependant_files else ""
        except ValueError as e:
            logging.error(f"Error processing imports_map for file {row['filepath']}: {e}")
            return ""
        except Exception as e:
            logging.error(f"Other error processing file {row['filepath']}: {e}")
            return ""

    def path_cleaner(path):
        return path.split("/code/")[1]

    file_df['dependancy_map'] = file_df.apply(dependancy_mapper_handler, axis=1)
    file_df['filepath_clean'] = file_df['filepath'].apply(lambda x: path_cleaner(x))
    
    file_df.fillna("", inplace=True)
    file_df.to_csv(str(fileClassificationReportPath), index=False)