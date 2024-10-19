import subprocess
import os
import sys

def get_last_command(file_path):
    try:
        with open(file_path,'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        return None

def run_command(command):
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process.stdout, process.stderr, process.returncode

def splat_find(command ):
    if command:
        print(f"Last command was: {command}")
        # Add specific logic to process this command
        stdout, stderr, returncode = run_command(command)
        print(f"hello{stdout} bye{stderr} goodbye{returncode}")
    else:
        print("No last command found.")
