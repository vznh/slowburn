import os
import errortrace
import subprocess
import click
import time
import select
import requests
from utils import parse_error_stack, run_repopack

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
import os
import subprocess
import time
import select

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
    
    error_data = parse_error_stack(error_message)
    
    print(f"DEBUG: Extracted error data: {error_data}")
    
    if not error_data['endpoints'] and not error_data['error_types']:
        click.echo("Couldn't extract error information from the error message.")
        click.echo("Please check the parse_error_stack function in utils.py")
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
        
def trigger_errors():
    """Trigger the error endpoints to generate errors."""
    endpoints = ["/process", "/items", "/users"]
    for endpoint in endpoints:
        try:
            requests.get(f"http://localhost:8000{endpoint}")
        except requests.RequestException:
            pass

def generate_explanation(error_message, context):
    """Generate a human-readable explanation using Groq API."""
    if not GROQ_API_KEY:
        click.echo("GROQ_API_KEY is not set. Please set it as an environment variable.")
        return "Unable to generate explanation due to missing API key."

    #not implemented yet :3 this will NOT WORK 

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        return f"Error generating explanation: {str(e)}"

@click.group()
def cli():
   """A CLI that helps you squash bugs and understand what went wrong in your code. Use it as a learning tool or have it complete your code for you!"""
    pass

@cli.command()
@click.option('--project-dir', default='./test-nextjs-project', help='Path to the FastAPI project directory')
def find(project_dir):
    """Find and analyze bugs in your FastAPI project."""
    print(f"DEBUG: Starting find command with project_dir: {project_dir}")
    project_dir = os.path.abspath(project_dir)
    click.echo(f"Analyzing FastAPI project in {project_dir}...")
    
    click.echo("Starting the FastAPI server. Please interact with the application to trigger errors.")
    click.echo("The tool will capture any errors that occur during the next 30 seconds.")
    click.echo("You can access the application at http://localhost:8000")
    click.echo("Try accessing endpoints like /users, /items, or /process to trigger errors.")
    
    error_message = compile_project(project_dir)
    
    print(f"DEBUG: Checking for errors in output")
    if "error" not in error_message.lower() and "exception" not in error_message.lower():
        click.echo("No errors found during the capture period.")
        return

    click.echo("Errors found. Analyzing...")
    process_error(error_message)

if __name__ == '__main__':
    print("DEBUG: Starting SPLAT CLI")
    cli()
