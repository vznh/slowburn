import subprocess
import os

def get_last_command(file_path):
    try:
        with open(file_path,'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        return None

def run_command(command):
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process.stdout, process.stderr, process.returncode

def splat_find():
    last_command_path = os.path.expanduser("~/.last_command")
    last_command = get_last_command(last_command_path)

    if last_command:
        print(f"Last command was: {last_command}")
        # Add specific logic to process this command
        stdout, stderr, returncode = run_command(last_command)
        print(f"{stdout} {stderr} {returncode}")
    else:
        print("No last command found.")
