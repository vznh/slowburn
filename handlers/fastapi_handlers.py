import os
import subprocess
import time
import select
import re
from typing import Dict, List
import click
from process.process import process

def parse_fastapi_error(error_info: str) -> Dict[str, List[str]]:
    endpoints = []
    error_types = []
    
    # Pattern for connection errors
    error_pattern = r'Error accessing endpoint (/\w+): (.+)'
    
    matches = re.findall(error_pattern, error_info)
    
    for match in matches:
        endpoint, error_type = match
        endpoints.append(endpoint)
        error_types.append(error_type)

    # If no matches found, check for server startup error
    if not matches:
        server_error_match = re.search(r'Server error: (.+)', error_info)
        if server_error_match:
            endpoints.append("Server Startup")
            error_types.append(server_error_match.group(1))

    return {
        "endpoints": list(dict.fromkeys(endpoints)),
        "error_types": list(dict.fromkeys(error_types))
    }

def compile_project(project_dir):
    """Run the FastAPI project in the specified directory and capture any errors."""
    os.chdir(project_dir)
    process = subprocess.Popen(
        ["python", "src/app/main.py", "--log-level", "error"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    output = []
    error_detected = False
    start_time = time.time()
    
    while True:
        reads = [process.stdout.fileno(), process.stderr.fileno()]
        ret = select.select(reads, [], [], 0.5)

        for fd in ret[0]:
            if fd == process.stdout.fileno():
                line = process.stdout.readline()
                output.append(line)
            if fd == process.stderr.fileno():
                line = process.stderr.readline()
                output.append(line)

        full_output = "".join(output)
        if "ERROR:" in full_output and not error_detected:
            error_detected = True

        # Stop capturing after 30 seconds or if an error is detected
        if error_detected or (time.time() - start_time > 30):
            break

        if process.poll() is not None:
            break
        
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    
    # Capture any remaining output
    stdout, stderr = process.communicate()
    output.extend([stdout, stderr])
    
    full_output = "".join(output)
    return full_output

def process_error(error_message):
    """Process the error message and generate human-readable explanation."""
    error_data = parse_fastapi_error(error_message)
    
    if not error_data['endpoints'] and not error_data['error_types']:
        return "Couldn't extract error information from the error message."

    # Construct context for explanation
    context = f"FastAPI server errors:\n"
    for endpoint, error_type in zip(error_data['endpoints'], error_data['error_types']):
        context += f"Endpoint {endpoint} encountered error: {error_type}\n"

    explanation = process(error_message, context)
    return explanation