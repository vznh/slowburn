"""
This implementation is a pipeline that is a readable version of splat, where the pipeline can be easily seen here.
@note: Splat only currently supports files that can be launched from root directory.
@note: You are NOT to run this file.
"""
# [START module.py]
import os
import json
from typing import List
from relational import relational_error_parsing_function
from process.process import process

def main():
  """
  Running "splat <?-r> '<python3 filename.py>' will compile the Python file in a contained environment.

  If splat is called with no flag, then the error traces will only be scanned.
  If splat is called with a -r flag, then the error traces and its Nth degree connections will be scanned.

  If splat is not called with an entrypoint <python3 ?.py> then splat will prompt the user for an entrypoint.
  """

  '''CLI NEEDS TO PROMPT USER HERE + CLI NEEDS TO RETURN BACK FLAG & ENTRYPOINT'''

  # Handle relational adjacency list, and feed this to LLM
  entrypoint: List[str] = ['python3', 'foo.py'] # <-- will be filled in by CLI
  flag: str = "-r"
  traceback, error_info, repopack = relational_error_parsing_function(entrypoint, flag)

  # LLM now takes the data (all file context as type str, error message as type str)
  response: object = process(traceback, error_info, repopack)
  '''NOW WE NEED TO SPIT THIS BACK INTO THE CLI SEQUENTIALLY'''

# [END module.py]
