import os
import subprocess
import time
import select
import re
from typing import Dict, List
import click
from generator import generate_explanation

def parse_fastapi_error(error_info: str) -> Dict[str, List[str]]:
    """
    Parse through a FastAPI error log and return a dictionary of endpoints and their error types.
    """
    print("DEBUG: Entering parse_fastapi_error function")
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

def compile_project(project_dir):
    """Run the FastAPI project in the specified directory and capture any errors."""
    print(f"DEBUG: Changing directory to {project_dir}")
    os.chdir(project_dir)
    print("DEBUG: Starting FastAPI server")
    process = subprocess.Popen(
        ["python", "src/app/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    output = []
    error_detected = False
    print("DEBUG: Entering main loop to read process output")
    start_time = time.time()
    
    while True:
        reads = [process.stdout.fileno(), process.stderr.fileno()]
        ret = select.select(reads, [], [], 0.5)

        for fd in ret[0]:
            if fd == process.stdout.fileno():
                line = process.stdout.readline()
                print(f"STDOUT: {line.strip()}")
                output.append(line)
            if fd == process.stderr.fileno():
                line = process.stderr.readline()
                print(f"STDERR: {line.strip()}")
                output.append(line)

        full_output = "".join(output)
        if "ERROR:" in full_output and not error_detected:
            print("DEBUG: Error detected in output")
            error_detected = True

        # Stop capturing after 30 seconds or if an error is detected
        if error_detected or (time.time() - start_time > 30):
            print("DEBUG: Finished capturing output")
            break

        if process.poll() is not None:
            print("DEBUG: Process has terminated")
            break

    print("DEBUG: Terminating the process")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("DEBUG: Process did not terminate, forcing kill")
        process.kill()
    
    # Capture any remaining output
    stdout, stderr = process.communicate()
    output.extend([stdout, stderr])
    
    print("DEBUG: Returning collected output")
    full_output = "".join(output)
    print("DEBUG: Full output:")
    print(full_output)
    return full_output

def process_error(error_message):
    """Process the error message and generate human-readable explanation."""
    print("DEBUG: Entering process_error function")
    print("DEBUG: Full error message:")
    print(error_message)
    
    error_data = parse_fastapi_error(error_message)
    
    print(f"DEBUG: Extracted error data: {error_data}")
    
    if not error_data['endpoints'] and not error_data['error_types']:
        click.echo("Couldn't extract error information from the error message.")
        click.echo("Please check the parse_fastapi_error function in fastapi_handler.py")
        return

    click.echo("Errors found:")
    for endpoint, error_type in zip(error_data['endpoints'], error_data['error_types']):
        click.echo(f"  Endpoint: {endpoint}, Error: {error_type}")

    # Construct context for explanation
    context = f"FastAPI server errors:\n"
    for endpoint, error_type in zip(error_data['endpoints'], error_data['error_types']):
        context += f"Endpoint {endpoint} encountered error: {error_type}\n"

    explanation = generate_explanation(error_message, context)
    click.echo("Human-readable explanation:")
    click.echo(explanation)