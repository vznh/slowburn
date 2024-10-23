"""
TODO
* swap mock repopack func --> actual repopack func
* deprecate project root var --> actual repo root
* smarter prompt engineering
"""
# [START relational.py]
import os
import json
import subprocess
from typing import Tuple, List, Optional
from utilities.exception import (
  build_adjacency_list,
  parse_error_stack,
  run_mock_repopack,
  get_nth_related_files
)

def capture_relational_error_parsing(entrypoint: List[str], flag: str = "", debug: Optional[bool] = False) -> Tuple[str, str, str]:
  try:
    subprocess.run(entrypoint, capture_output=True, check=True, text=True)
    return "", "", "" # If no error occurs, return empty strings
  except subprocess.CalledProcessError as error:
    # Capture the error output to simulate error stack
    traceback: str = error.stderr if error.stderr else str(error)
    error_information = str(error)
    collected_traceback_files = parse_error_stack(traceback)

    # Deprecated
    project_root = os.getcwd()

    return traceback, error_information, (run_mock_repopack(collected_traceback_files) if flag == "-g" or flag == None else run_mock_repopack(collected_traceback_files))


def relational_error_parsing_function(entrypoint, flag: str = "") -> Tuple[str, str, str]:
  try:
    subprocess.run(entrypoint, capture_output=True, check=True, text=True)
    return "", "", ""  # Return empty strings if no error occurs
  except subprocess.CalledProcessError as error: # This will always run, on purpose.
    # Capture the error output to simulate the error stack
    traceback: str = error.stderr if error.stderr else str(error)
    error_information: str = str(error)
    collected_traceback_files = parse_error_stack(traceback)
    project_root = os.getcwd()
    #collected_traceback_files = [os.path.join(project_root, file) for file in parse_error_stack(error_information)]
    #print(collected_traceback_files)
    if flag == '-r':
      graph = build_adjacency_list(collected_traceback_files, project_root)
      all_related_files = get_nth_related_files(collected_traceback_files, graph)
      return traceback, error_information, run_mock_repopack(list(all_related_files))
    else:
      return traceback, error_information, run_mock_repopack(collected_traceback_files)

if __name__ == "__main__":
  relational_error_parsing_function(['python3', 'test.py'], '-r')

# [END relational.py]
