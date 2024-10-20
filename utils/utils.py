# [START utils.py]
"""
This file creates a dependency graph that depicts the relationships between files. It will read the error stack, and attempt to parse it. Then, using the files mentioned, add everything.
If the user does not provide a flag, the graph will only create itself from the error stack.
If the user does provide "-g", the graph will contain all files from the repo, with respect to the .gitignore.
If the user does provide "-r", the graph will contain all files from the error stack, alongside all files that are imported/included in the source file, and recursively call itself until all relationships are exhausted.

@usage: "splat <?-g> <?-r> <?entrypoint>"
@note: if "splat" is not called with an entrypoint, the user will provide their own entrypoint when prompted
@note: entrypoint will **always** be provided; assume there are 3 possibilities only
"""
import os
from typing import List, Set, Dict
import ast
import subprocess
import re
import json

def main(error_info: str, flag: str | None = None, project_root: str = '.'):
  error_files = parse_error_stack(error_info)

  if flag == '-g':
    return run_repopack([project_root])

  if flag == '-r':
    graph = build_adjacency_list(error_files, project_root)
    all_related_files = get_nth_related_files(error_files, graph)
    return run_repopack(list(all_related_files))

  return run_repopack(error_files)

def is_project_file(file_path: str, project_root: str) -> bool:
  return os.path.commonpath([file_path, project_root]) == project_root

'''
This function parses through a typical Python error trace stack, and returns a list of all files related.
@note: idx[0] will always be where error was caught
@note: idx[-1] will always be where error truly originated and or raised
'''
def parse_error_stack(error_info: str) -> List[str]:
    files = []
    # This regex looks for file paths in various formats, including the command output
    file_pattern = re.compile(r'(?:File "([^"]+)"|\b(\S+\.py)\b)')

    for line in error_info.split('\n'):
        matches = file_pattern.findall(line)
        for match in matches:
            # The regex returns a tuple for each match, we take the non-empty string
            file_path = next((m for m in match if m), None)
            if file_path:
                file_path = file_path.strip()
                # Remove any quotes around the file path
                file_path = file_path.strip("'\"")
                if os.path.exists(file_path):
                    files.append(file_path)

    return list(set(files))  # Remove duplicates

'''
This function calls repopack to be used with a required parameter.
'''
def run_repopack(path: List[str], style: str = 'json') -> Dict:
    """
    Run repopack on the specified path and return the results.

    Args:
        path (str): The path to analyze with repopack.
        style (str): The output style for repopack (default is 'json').
        respect_gitignore (bool): Whether to respect .gitignore files (default is True).

    Returns:
        Dict: The parsed JSON output from repopack.
    """
    cmd = ['repopack'] + path + ['--style', style, '--respect-gitignore']

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)

'''
This function runs through a source file, and grabs all files linked by any Nth degree connection.
@param: file_path (str) - the path of the source file to analyze
@returns: all files related to the parameter file to any Nth degree in type Set[str]
'''
def get_nth_related_files(start_files: List[str], graph: Dict[str, List[str]]) -> Set[str]:
  related_files = set(start_files)
  planned_visit = list(start_files)

  while (planned_visit):
    current = planned_visit.pop(0)
    for neighbor in graph.get(current, []):
      if neighbor not in related_files:
        related_files.add(neighbor)
        planned_visit.append(neighbor)

  return related_files

'''
Builds an adjacency list from a list of files.
'''
def build_adjacency_list(files: List[str], project_root: str) -> Dict[str, List[str]]:
    adjacency_list = {}
    for file in files:
        if not is_project_file(file, project_root):
            continue
        with open(file, 'r') as f:
            tree = ast.parse(f.read())
        imports = set()
        adjacency_list[file] = [
            os.path.join(project_root, imp.replace('.', os.path.sep) + '.py')
            for imp in imports
            if os.path.exists(os.path.join(project_root, imp.replace('.', os.path.sep) + '.py'))
            and is_project_file(os.path.join(project_root, imp.replace('.', os.path.sep) + '.py'), project_root)
        ]
    return adjacency_list
################################################## NOT IMPLEMENTED BELOW #####################################################################

# [END utils.py]
"""
runs repopack

@param takes in a file directory

@returns a json of all of the contents within that function
"""

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
        },
        'c': {
            'commands': ['gcc'],
            'files': [],
            'extensions':['.c','.cpp']
        },
        'java': {
            'commands': ['javac','java'],
            'files': [],
            'extensions': ['.java']
        },
        'javascript': {
            'commands': ['node'],
            'files': [],
            'extensions': ['.js','.jsx']
        },
        'typescript': {
            'commands': ['node'],
            'files': [],
            'extensions': ['.ts','.tsx']
        },
        'python': {
            'commands': ['python', 'python3'],
            'files': [],
            'extensions':['.py']
        },
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
            'extensions': ['.jsx', '.tsx', '.js','.ts']
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
    }

    def check_command(cmd):
        for framework, data in indicators.items():
            if any(c in cmd for c in data['commands']):
                return framework
        return None

    def check_files(dir):
        for framework, data in indicators.items():
            if len(data['files']) == 0:
                return None
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
        print('command found')
        return framework

    # Check for characteristic files
    framework = check_files(command)
    if framework:
        print('file found', framework)
        return framework

    # Check file extension in the command
    framework = check_file_extension(command)
    if framework:
        print('file extension found')
        return framework

    # Check package.json for more clues
    full_dir = './' + command
    package_json_path = os.path.join(full_dir, 'package.json')
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

# [END utils.py]

if __name__ == "__main__":
      # Define the entry point command
      # splat "python3 test.py"
      entrypoint = ["python3", "test.py"]

      # Run the entrypoint and capture the error output
      try:
          subprocess.run(entrypoint, check=True)
          print("Ran substance")
      except subprocess.CalledProcessError as e:
          # Capture the error output to simulate the error stack
          error_info = e.stderr if e.stderr else str(e)
          print("Error information captured from test.py:")
          print(error_info)

          # Parse the error stack to get a list of files
          # Use the parse_error_stack to get files mentioned in the error_info
          error_files = parse_error_stack(error_info)
          print("************ERROR FILES*************")
          print(error_files)
          print("************ERROR FILES*************")

      except Exception as e:
          print("An unexpected error occurred:", str(e))
