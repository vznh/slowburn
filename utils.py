# [START utils.py]
"""
This file creates a dependency graph that depicts the relationships between files. It will read the error stack, and attempt to parse it. Then, using the files mentioned, add everything.
If the user does not provide a flag, the graph will only create itself from the error stack.
If the user does provide "-g", the graph will contain all files from the repo, with respect to the .gitignore.
If the user does provide "-r", the graph will contain all files from the error stack, alongside all files that are imported/included in the source file, and recursively call itself until all relationships are exhausted.

@usage: "splat <?-g> <?-r> <entrypoint>"
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
@usage: call graph_related_files(pure error string, if flag is raised)
@returns: None
'''
def graph_related_files(error_info: str, global_flag_raised: bool = False) -> None:
  if global_flag_raised:
    return
  else:
    return

'''
This function runs through the entire repository, and dodges all files that do not start with .py.
@param: repo_path (str) - the path to the repository to analyze (default is current directory)
@returns: all traced files of type List[str]
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
@param: file_path (str) - the path of the source file to analyze
@returns: all files related to the parameter file to any Nth degree in type Set[str]
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
@param: import_name (str) - the name of the import to resolve.
@param: file_path (str) - the path of the source file from which the import is made.
@returns: absolute path as type str or None if the import cannot be found
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
@note: This should only be used if the -r flag is raised.
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
