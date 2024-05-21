from .pyparser import PythonParser
import os
import pandas as pd
from ..utils import get_classification_report, get_directory_report, get_stdlibs_path
from pathlib import Path
import ast 

def transform_pyimport_statement(import_line):
    # Remove newline characters and leading/trailing whitespaces
    import_line = import_line.replace('\n', ' ').strip()

    # Handle parentheses and extra commas
    if '(' in import_line and ')' in import_line:
        # Remove parentheses and any spaces near them
        import_line = import_line.replace('(', ' ').replace(')', ' ').strip()

        # Replace multiple spaces with a single space
        import_line = ' '.join(import_line.split())

        # Remove any trailing commas
        if import_line.endswith(','):
            import_line = import_line[:-1]

    return import_line

def parse_import_statement(import_line, current_module_path):
    """
    Parses the import statement and extracts relevant information including the absolute file path.

    Args:
    import_line (str): The import statement line.
    current_module_path (str): The path to the current module.

    Returns:
    dict: A dictionary containing 'alias', 'module', 'functions', 'importpath', and 'codeline' as keys.
    """

    # Initialize the result dictionary
    result = {'alias': '', 'module': '', 'functions': '', 'importpath': '', 'codeline': import_line}

    # Check and handle alias
    if " as " in import_line:
        parts = import_line.split(" as ")
        import_line = parts[0]
        result['alias'] = parts[1]
        
    if "from " in import_line:
        parts = import_line.split(" import ")
        module_part = parts[0].replace("from ", "").strip()
        result['module'] = module_part
        result['functions'] = parts[1].strip()

        # Handling relative imports (with . or ..)
        if module_part.startswith('.'):
            # Count the number of dots to determine the relative depth
            depth = module_part.count('.')

            # Getting the directory of the current module
            current_dir = os.path.dirname(current_module_path)

            # Going up the required levels
            for _ in range(depth - 1):
                current_dir = os.path.dirname(current_dir)

            # Constructing the relative module path
            relative_module_path = module_part.lstrip('.').replace('.', '/')
            result['importpath'] = os.path.join(current_dir, relative_module_path, result['functions'])
        else:
            # Handle absolute path for non-relative imports
            result['importpath'] = os.path.join(module_part.replace(".", "/"), result['functions'])
    else:
        # Handle 'import ...' format
        module_name = import_line.replace("import ", "").strip()
        result['module'] = module_name
        result['importpath'] = os.path.join(module_name.replace(".", "/"))

    # Normalize the file path
    result['importpath'] = os.path.normpath(result['importpath'])


    return result

def python_imports_mapper(filepath, git_url):
    """
    Maps imports in a Python file within a given git repository.

    This function reads the file and directory structure of a repository from
    given CSV files. It then parses a specified Python file to identify its
    import statements. For each import statement, the function determines the
    type of import (e.g., Python File Import, Entity with Python File Import, 
    Init.py imports, or Edge case) based on the repository's file and directory
    structure.

    Parameters:
    filepath (str): The path to the Python file to be parsed.
    giturl (str): The URL of the git repository.

    Returns:
    list: A list of dictionaries, each containing details about an import statement
          including the clean import path and the import type.
    """

    fileClassificationReportPath = get_classification_report(git_url)
    directoryStructurePath = get_directory_report(git_url)
    mappersdirPath = get_stdlibs_path()

    file_df = pd.read_csv(str(fileClassificationReportPath))
    directory_df = pd.read_csv(str(directoryStructurePath))
    pystdlibs_df = pd.read_csv(str(mappersdirPath))

    parser = PythonParser(file_path=filepath)
    parsed_data = parser.parse()
    
    categories = ['imports_all']
    code_segments = parser.get_code_segments(categories, return_as_list=True)
    parsed_import_info = []
    
    for import_line in code_segments:
        transformed_import_line = transform_pyimport_statement(import_line)
        parsed_import = parse_import_statement(transformed_import_line, filepath)
        import_path = parsed_import["importpath"]

        # A. Check for direct Python file import
        if any(pystdlibs_df['package'].str.endswith(import_path)):
            parsed_import['import_path_clean'] = ""
            parsed_import['import_type'] = "Python Std Lib"
        
        elif import_path.count('.') == 0 and import_path.count('/') == 0:
            parsed_import['import_path_clean'] = ""
            parsed_import['import_type'] = "Other Imports"

        elif any(file_df['filepath'].str.endswith(import_path + ".py")):
            parsed_import['import_path_clean'] = import_path + ".py"
            parsed_import['import_type'] = "Python File Import"
        
        # B. Modify import path
        else:
            modified_import_path = '/'.join(import_path.split('/')[:-1])
            # C. Check for entity with Python file import
            if any(file_df['filepath'].str.endswith(modified_import_path + ".py")):
                parsed_import['import_path_clean'] = modified_import_path + ".py"
                parsed_import['import_type'] = "Entity within Python File Import"

            # D. Check for __init__.py imports
            elif any(directory_df['directory_path'].str.endswith(modified_import_path)) and \
                 any(file_df['filepath'].str.endswith(modified_import_path + "/__init__.py")):
                parsed_import['import_path_clean'] = modified_import_path + "/__init__.py"
                parsed_import['import_type'] = "Init.py imports"

            # E. Edge case
            else:
                if any(pystdlibs_df['package'].str.endswith(modified_import_path)):
                    parsed_import['import_path_clean'] = ""
                    parsed_import['import_type'] = "Python Std Lib"
                else:
                    parsed_import['import_path_clean'] = ""
                    parsed_import['import_type'] = "Other Imports"

        parsed_import_info.append(parsed_import)

    return parsed_import_info

def python_init_to_filemapper(parsed_import_list):
    pass
    

