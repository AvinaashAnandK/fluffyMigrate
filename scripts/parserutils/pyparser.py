import ast
import nbformat

class PythonParser(ast.NodeVisitor):
    def __init__(self, file_path):
        self.current_parents = []
        self.NESTED_NODE_TYPES = (
        ast.If, ast.Match, ast.MatchValue, ast.MatchSingleton, ast.MatchSequence, 
        ast.MatchStar, ast.MatchMapping, ast.MatchClass, ast.MatchAs, ast.MatchOr, 
        ast.For, ast.While, ast.AsyncFor, ast.Try, ast.TryStar, ast.With, 
        ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)
        self.file_path = file_path
        self.data = {
            "imports_all": [],
            "global_variables": [],
            "control_conditional": [],
            "loops": [],            
            "error_try_except": [],
            "handling_with": [],            
            "classes": [],
            "functions_sync": [],
            "functions_async": [],
            "decorators": []
        }
        if file_path.endswith('.py'):
            with open(file_path, 'r', encoding='utf-8') as file:
                self.tree = ast.parse(file.read())
        elif file_path.endswith('.ipynb'):
            with open(file_path, 'r', encoding='utf-8') as file:
                notebook = nbformat.read(file, as_version=4)
                code_cells = [cell.source for cell in notebook.cells if cell.cell_type == 'code']
                combined_code = '\n'.join(code_cells)
                self.tree = ast.parse(combined_code)
        else:
            raise ValueError("Unsupported file type. Please provide a .py or .ipynb file.")

# Parsing Import Nodes
    def visit_Import(self, node):
        self.data["imports_all"].append((node.lineno, node.end_lineno))

# Parsing ImportFrom nodes
    def visit_ImportFrom(self, node):
        self.data["imports_all"].append((node.lineno, node.end_lineno))

# Stored in global_variables
# Parsing Assign nodes
    def visit_Assign(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["global_variables"].append((node.lineno, node.end_lineno))
        self.generic_visit(node)

# Parsing AnnAssign
    def visit_AnnAssign(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["global_variables"].append((node.lineno, node.end_lineno))
        self.generic_visit(node)

# Parsing AugAssign
    def visit_AugAssign(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["global_variables"].append((node.lineno, node.end_lineno))
        self.generic_visit(node)

# Stored in control_conditional
# Parsing If
    def visit_If(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["control_conditional"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()    
# Parsing Match
    def visit_Match(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["control_conditional"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()    
# Parsing MatchValue 
    def visit_MatchValue(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["control_conditional"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()    
# Parsing MatchSingleton 
    def visit_MatchSingleton(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["control_conditional"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()    
# Parsing MatchSequence  
    def visit_MatchSequence(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["control_conditional"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()    
# Parsing MatchStar 
    def visit_MatchStar(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["control_conditional"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()    
# Parsing MatchMapping 
    def visit_MatchMapping(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["control_conditional"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()    
# Parsing MatchClass
    def visit_MatchClass(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["control_conditional"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()    
# Parsing MatchAs 
    def visit_MatchAs(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["control_conditional"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()    
# Parsing MatchOr   
    def visit_MatchOr(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["control_conditional"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()    

# Stored in loops
# Parsing For
    def visit_For(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["loops"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()   
# Parsing While
    def visit_While(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["loops"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()  
# Parsing AsyncFor
    def visit_AsyncFor(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["loops"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()  

# <!-- "error_try_except": [], -->
# Parsing Try
    def visit_Try(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["error_try_except"].append((node.lineno, node.end_lineno))

        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()
# Parsing TryStar
    def visit_TryStar(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["error_try_except"].append((node.lineno, node.end_lineno))

        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()
        
# <!-- "handling_with": [] -->
# Parsing With 
    def visit_With(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["handling_with"].append((node.lineno, node.end_lineno))

        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()
# Parsing AsyncWith
    def visit_AsyncWith(self, node):
        if not any(isinstance(parent, self.NESTED_NODE_TYPES) for parent in self.current_parents):
            self.data["handling_with"].append((node.lineno, node.end_lineno))

        self.current_parents.append(node)
        self.generic_visit(node)
        self.current_parents.pop()

# <!-- "functions_sync": [], -->
# Parsing FunctionDef
    def visit_FunctionDef(self, node):
        if not any(isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Try)) for parent in self.current_parents):
            self.data["functions_sync"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        for decorator in node.decorator_list:
            self.data["decorators"].append((decorator.lineno, decorator.end_lineno))
        self.generic_visit(node)
        self.current_parents.pop()

# <!-- "classes": [], -->
# Parsing ClassDef
    def visit_ClassDef(self, node):
        if not any(isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Try)) for parent in self.current_parents):
            self.data["classes"].append((node.lineno, node.end_lineno))
        
        self.current_parents.append(node)
        for decorator in node.decorator_list:
            self.data["decorators"].append((decorator.lineno, decorator.end_lineno))
        self.generic_visit(node)
        self.current_parents.pop()

# <!-- "functions_async": [], -->
# Parsing AsyncFunctionDef
    def visit_AsyncFunctionDef(self, node):
        if not any(isinstance(parent, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Try)) for parent in self.current_parents):
            self.data["functions_async"].append((node.lineno, node.end_lineno))

        self.current_parents.append(node)
        for decorator in node.decorator_list:
            self.data["decorators"].append((decorator.lineno, decorator.end_lineno))
        self.generic_visit(node)
        self.current_parents.pop()

    def generic_visit(self, node):
        # Add the current node to the parent stack before visiting children
        self.current_parents.append(node)
        for child in ast.iter_child_nodes(node):
            self.visit(child)
        # Remove the current node from the parent stack after visiting children
        self.current_parents.pop()

    def parse(self):
        self.visit(self.tree)
        return self.data
    
    def get_code_segments(self, categories=None, return_as_list=False):
        code_segments = []

        if self.file_path.endswith('.ipynb'):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                notebook = nbformat.read(file, as_version=4)
                code_cells = [cell.source.split('\n') for cell in notebook.cells if cell.cell_type == 'code']
                flat_code_lines = [line for cell in code_cells for line in cell]
        else:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    flat_code_lines = file.readlines()
            except IOError as e:
                print(f"Error opening file: {e}")
                return

        # Use all categories from parsed_data if no specific categories are provided
        if not categories:
            categories = self.data.keys()

        for category in categories:
            items = self.data.get(category, [])
            category_segments = []
            for start_line, end_line in items:
                code_segment = ''.join(flat_code_lines[start_line-1:end_line])
                category_segments.append(code_segment.strip())

            if return_as_list:
                code_segments.extend(category_segments)
            else:
                print(f"--- {category.upper()} ---")
                print("\n".join(category_segments))
                print("\n")

        if return_as_list:
            return code_segments