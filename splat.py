import os
import subprocess
import time
import click
import requests
import errortrace
from handlers import fastapi_handlers
from process.process import process
from utils.utils import detect_framework_or_language, extract_filename_with_extension
import subprocess
import requests
import time
from terminalout.terminal import terminalstep1
from utils.utils import detect_framework_or_language, extract_filename_with_extension

@click.command()
@click.argument('command', required=False)
@click.option('-r', '--related', is_flag=True, help='Load the file and imported files to load into the LLM')
@click.option('-g', '--is_global', is_flag=True, help="Load the entire repository into the LLM using repopack")
def cli(command, related, is_global):
    """A CLI that helps you squash bugs and understand what went wrong in your code."""
    if not command:
        click.echo("""
            /\\_/\\
           ( o.o )
            > ^ <
            Please provide a command or file to analyze.""")
        return

    project_type = detect_framework_or_language(command)
    click.echo("""
        /\\_/\\
       ( o.o )
        > ^ <
        welcome to splat...
        """)
    click.echo(f"Detected project type: {project_type}")
    '''
    if project_type == 'fastapi':
        handle_fastapi_project(command)
    elif project_type in ['javascript', 'typescript', 'java', 'c']:
        handle_generic_project(command, project_type, related, is_global)
    else:
        click.echo(f"Unsupported project type: {project_type}")
    '''
    if project_type == "python" and "main.py" in command:
        handle_fastapi_project(command)
    else:
        error_trace = errortrace.splat_find(command)
        if error_trace:
            step1 = process(command, error_trace)
            user_response = terminalstep1(step1)
        else:
            click.echo("There was an issue running your code")
def handle_fastapi_project(command):
    click.echo("Analyzing FastAPI project...")

    if os.path.isfile(command):
        project_dir = os.path.dirname(command)
        main_file = os.path.basename(command)
    else:
        project_dir = command
        main_file = 'main.py'

    server_process = subprocess.Popen(
        ["python", os.path.join(project_dir, main_file)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(5)

    errors = []

    endpoints = ["/users", "/items", "/process", "/user/1", "/item/1", "/error"]
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=2)
            if response.status_code >= 400:
                errors.append(f"Error in endpoint {endpoint}: {response.status_code} {response.text}")
        except requests.RequestException as e:
            errors.append(f"Error accessing endpoint {endpoint}: {str(e)}")

    server_process.terminate()
    _, stderr = server_process.communicate(timeout=5)

    if stderr:
        errors.append(f"Server error: {stderr}")

    if errors:
        error_message = "\n".join(errors)
        explanation = fastapi_handlers.process_error(error_message)
        print(explanation)  # This will print only the GROQ API response
    else:
        click.echo("No errors found during the analysis.")

def handle_generic_project(command, language, related, is_global):
    click.echo(f"Analyzing {language.capitalize()} project...")
    if related:
        click.echo("Related files analysis not implemented yet.")
    elif is_global:
        click.echo("Global repository analysis not implemented yet.")
    else:
        compilation_error = check_compilation(command)
        if compilation_error:
            click.echo("Compilation error found:")
            click.echo(compilation_error)
            llm_response = process(command, compilation_error)
            click.echo(llm_response)
        else:
            error_trace = errortrace.splat_find(command)
            if error_trace:
                llm_response = process(command, error_trace)
                click.echo(llm_response)
            else:
                click.echo("No errors found in your code.")

def check_compilation(command):
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, check=True)
        return None  # No compilation error
    except subprocess.CalledProcessError as e:
        return e.stderr

if __name__ == '__main__':
    cli()
