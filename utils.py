# [START utils.py]
"""
This file creates a dependency graph that depicts the relationships between files.
If the user does not provide a flag, the graph will only create itself from the error stack.
If the user does provide "-g", the graph will contain all files from the repo, with respect to the .gitignore.
If the user does provide "-r", the graph will contain all files from the error stack, alongside all files that are imported/included in the source file, and recursively call itself until all relationships are exhausted.

@Usage: "splat <?-g> <?-r>"
"""
import os
from typing import List, Set, Dict
import ast
from networkx import DiGraph
import subprocess
import json
import re

'''
This function parses through a typical Python error trace stack, and returns a list of all files related.
@note: idx[0] will always be where error was caught
@note: idx[-1] will always be where error truly originated and or raised
'''
def parse_error_stack2(error_info: str) -> List[str]:
  files: List = []
  for line in error_info.split('\n'):
    if line.strip().startswith('File "'):
      file_path = line.split('"')[1]
      files.append(file_path)

  return list(set(files)) # NOTE: We should change this to just { return files } if this doesn't work as intended

'''
this function is changed slightly to help fastAPI lol 
@note: idx[0] will always be where error was caught
@note: idx[-1] will always be where error truly originated and or raised
'''

def parse_error_stack(error_info: str) -> Dict[str, List[str]]:
    """
    Parse through a FastAPI error log and return a dictionary of endpoints and their error types.
    """
    print("DEBUG: Entering parse_error_stack function")
    print("DEBUG: Error info received:")
    print(error_info)
    
    endpoints = []
    error_types = []
    
    # Pattern for FastAPI error logs
    error_pattern = r'INFO:\s+127\.0\.0\.1:\d+ - "GET (/\w+) HTTP/1\.1" (\d+) (.+)'
    
    matches = re.findall(error_pattern, error_info)
    
    print(f"DEBUG: Found {len(matches)} matches")
    for match in matches:
        endpoint, status_code, error_type = match
        endpoints.append(endpoint)
        error_types.append(f"{status_code} {error_type}")
        print(f"DEBUG: Added endpoint: {endpoint}, error: {status_code} {error_type}")

    return {
        "endpoints": list(dict.fromkeys(endpoints)),
        "error_types": list(dict.fromkeys(error_types))
    }


'''
This function is a shorthand redirecting based on if a flag is raised during command call or not.
@Usage: call graph_related_files(pure error string, if flag is raised)
@Returns: None
'''
def graph_related_files(error_info: str, global_flag_raised: bool = False) -> None:
  if global_flag_raised:
    return
  else:
    return

'''
This function runs through the entire repository, and dodges all files that do not start with .py.
@Param: repo_path (str) - the path to the repository to analyze (default is current directory)
@Returns: all traced files of type List[str]
'''
def get_repo_details(repo_path: str = ".") -> List[str]:
  traced_files = []
  gitignore = set()

  # Read the .gitignore, if it exists
  if os.path.exists('.gitignore'):
    with open('.gitgnore', 'r') as f:
      gitignore = set(line.strip() for line in f if line.strip() and not line.startswith("#"))

  for root, _, files in os.walk(repo_path):
    for file in files:
      if (file.endswith('py')):
        full_path = os.path.join(root, file)
        relative_path = os.path.relpath(full_path, repo_path)
        if not any(relative_path.startswith(ignore) for ignore in gitignore):
          traced_files.append(full_path)

  return traced_files

'''
This function runs through a source file, and grabs all files linked by any Nth degree connection.
@Param: file_path (str) - the path of the source file to analyze
@Returns: all files related to the parameter file to any Nth degree in type Set[str]
'''
def get_related_details(file_path: str) -> Set[str]:
  with open(file_path, 'r') as file:
    tree = ast.parse(file.read(), filename=file_path)

  imports = set()
  for node in ast.walk(tree):
    if isinstance(node, ast.Import):
      for alias in node.names:
        imports.add(alias.name)
    elif isinstance(node, ast.ImportFrom):
      if node.module:
        imports.add(node.module)

  return imports

'''
This helper function resolves an import name to an absolute file path.
@Param: import_name (str) - the name of the import to resolve.
@Param: file_path (str) - the path of the source file from which the import is made.
@Returns: absolute path as type str or None if the import cannot be found
'''
def resolve_import(import_name: str, file_path: str) -> str | None:
  dir_path = os.path.dirname(file_path)
  possible_paths = [
    os.path.join(dir_path, f"{import_name.replace('.', '/')}.py"),
    os.path.join(dir_path, import_name, "__init__.py"),
  ]

  for path in possible_paths:
    if os.path.exists(path):
      return os.path.abspath(path)

  return None

'''
Build a dependency graph from a list of files.

This function creates a directed graph of type DiGraph where each node represents a
file, and directed edges represent import relationships between files.

@param files: A list or set of file paths to analyze for dependencies.
@returns: A directed graph (DiGraph) representing the dependencies among the files.
'''
def build_dependency_graph(files: List[str] | Set[str]) -> DiGraph:
  graph = DiGraph()
  for file in files:
    if file not in graph:
      graph.add_node(file)

    imports = get_related_details(file)
    for imp in imports:
      imp_file = resolve_import(imp, file)
      if imp_file and imp_file in files:
        graph.add_edge(file, imp_file)

  return graph

"""
runs repopack

@param takes in a file directory

@returns a json of all of the contents within that function


"""
def run_repopack(files):
  

    """Run Repopack on specific files and return the packed content."""
    try:
        # Create a temporary directory to store the files
        temp_dir = 'temp_repopack'
        os.makedirs(temp_dir, exist_ok=True)

        # Copy the specified files to the temporary directory
        for file in files:
            dest_path = os.path.join(temp_dir, os.path.basename(file))
            with open(file, 'r') as src, open(dest_path, 'w') as dest:
                dest.write(src.read())

        # Run Repopack on the temporary directory
        result = subprocess.run(['repopack', temp_dir, '--style', 'json'], 
                                capture_output=True, text=True, check=True)

        # Clean up the temporary directory
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

        # Parse the JSON output
        packed_content = json.loads(result.stdout)

        return packed_content
    except subprocess.CalledProcessError as e:
        print(f"Error running Repopack: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing Repopack output: {e}")
        return None

# [END utils.py]
#

'''
This function uses a command and tries to check what type the file/directory is.
The idea is that we will have robust solutions specifically for different project types,
meaning that we need to determine what kind of project/file the user is working with.
'''
def detect_framework_or_language(command, directory='.'):
    # Dictionary to map commands, file presence, or file extensions to frameworks/languages
    indicators = {
        'nextjs': {
            'commands': ['next', 'npm run dev', 'yarn dev'],
            'files': ['next.config.js', 'pages'],
            'extensions': ['.jsx', '.tsx']
        },
        'fastapi': {
            'commands': ['uvicorn', 'python main.py'],
            'files': ['main.py'],
            'extensions': ['.py']
        },
        'react': {
            'commands': ['react-scripts start', 'npm start', 'yarn start'],
            'files': ['src/App.js', 'public/index.html'],
            'extensions': ['.jsx', '.tsx']
        },
        'django': {
            'commands': ['python manage.py runserver', 'django-admin'],
            'files': ['manage.py', 'settings.py'],
            'extensions': ['.py']
        },
        'flask': {
            'commands': ['flask run', 'python app.py'],
            'files': ['app.py', 'wsgi.py'],
            'extensions': ['.py']
        },
        'vue': {
            'commands': ['vue-cli-service serve', 'npm run serve'],
            'files': ['src/main.js', 'public/index.html'],
            'extensions': ['.vue']
        },
        'angular': {
            'commands': ['ng serve', 'npm start'],
            'files': ['angular.json', 'src/main.ts'],
            'extensions': ['.ts']
        },
        'express': {
            'commands': ['node server.js', 'npm start'],
            'files': ['server.js', 'app.js'],
            'extensions': ['.js']
        },
        'spring-boot': {
            'commands': ['./mvnw spring-boot:run', 'java -jar'],
            'files': ['pom.xml', 'src/main/java'],
            'extensions': ['.java']
        },
        'ruby-on-rails': {
            'commands': ['rails server', 'rails s'],
            'files': ['config/routes.rb', 'app/controllers'],
            'extensions': ['.rb']
        },
        'laravel': {
            'commands': ['php artisan serve'],
            'files': ['artisan', 'app/Http/Kernel.php'],
            'extensions': ['.php']
        },
        'dotnet': {
            'commands': ['dotnet run', 'dotnet watch run'],
            'files': ['Program.cs', '.csproj'],
            'extensions': ['.cs']
        },
        'go': {
            'commands': ['go run'],
            'files': ['go.mod'],
            'extensions': ['.go']
        },
        'rust': {
            'commands': ['cargo run'],
            'files': ['Cargo.toml'],
            'extensions': ['.rs']
        },
        'kotlin': {
            'commands': ['kotlinc', 'kotlin'],
            'files': [],
            'extensions': ['.kt']
        },
        'scala': {
            'commands': ['scala', 'sbt run'],
            'files': ['build.sbt'],
            'extensions': ['.scala']
        },
        'swift': {
            'commands': ['swift', 'swiftc'],
            'files': ['Package.swift'],
            'extensions': ['.swift']
        },
        'r': {
            'commands': ['Rscript'],
            'files': [],
            'extensions': ['.r', '.R']
        },
        'perl': {
            'commands': ['perl'],
            'files': [],
            'extensions': ['.pl', '.pm']
        },
        'haskell': {
            'commands': ['ghc', 'runghc'],
            'files': [],
            'extensions': ['.hs']
        },
        'lua': {
            'commands': ['lua'],
            'files': [],
            'extensions': ['.lua']
        },
        'julia': {
            'commands': ['julia'],
            'files': [],
            'extensions': ['.jl']
        }
    }

    def check_command(cmd):
        for framework, data in indicators.items():
            if any(c in cmd for c in data['commands']):
                return framework
        return None

    def check_files(dir):
        for framework, data in indicators.items():
            if all(os.path.exists(os.path.join(dir, file)) for file in data['files']):
                return framework
        return None

    def check_file_extension(cmd):
        file_match = re.search(r'\b[\w-]+\.[a-zA-Z0-9]+\b', cmd)
        if file_match:
            file_extension = os.path.splitext(file_match.group())[1]
            for framework, data in indicators.items():
                if file_extension in data['extensions']:
                    return framework
        return None

    # Check command first
    framework = check_command(command)
    if framework:
        return framework

    # Check for characteristic files
    framework = check_files(directory)
    if framework:
        return framework

    # Check file extension in the command
    framework = check_file_extension(command)
    if framework:
        return framework

    # Check package.json for more clues
    package_json_path = os.path.join(directory, 'package.json')
    if os.path.exists(package_json_path):
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
            dependencies = package_data.get('dependencies', {})
            dev_dependencies = package_data.get('devDependencies', {})
            all_dependencies = {**dependencies, **dev_dependencies}

            if 'next' in all_dependencies:
                return 'nextjs'
            elif 'react' in all_dependencies:
                return 'react'
            elif 'vue' in all_dependencies:
                return 'vue'
            elif '@angular/core' in all_dependencies:
                return 'angular'
            elif 'express' in all_dependencies:
                return 'express'

    return 'unknown'
