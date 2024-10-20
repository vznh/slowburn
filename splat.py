import json
import os
import subprocess
import sys
import threading
import time
import click
import requests
from uagents import Context
import errortrace
from handlers import fastapi_handlers
from process.process import process
from relational import relational_error_parsing_function
from utils.utils import detect_framework_or_language, extract_filename_with_extension
import subprocess
from utils.utils import detect_framework_or_language, extract_filename_with_extension, kill_process_on_port
from terminalout.terminal import terminalstep1, file_writer_agent
import shlex
from agents.file_writer_agent import ErrorCorrectionRequest, file_writer, FileWriteResponse
import asyncio


@click.group()
def cli():
    pass

@cli.command
@click.argument('command', required=False)
@click.pass_context
@click.option('-r', '--related', is_flag=True, help='Load the file and imported files to load into the LLM')
@click.option('-g', '--is_global', is_flag=True, help="Load the entire repository into the LLM using repopack")
def squash(ctx, command, related, is_global):
    """A CLI that helps you squash bugs and understand what went wrong in your code."""
    #start_file_writer_agent()
    
    if not command:
        click.echo("""
            /\\_/\\
           ( >:< )
            > - <\
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
    entrypoint = command.split(" ")
    kill_process_on_port(8000)
    if project_type == "python" and "main.py" in command:
        handle_fastapi_project(command)
    #****** RELATED  *****
    elif related:
        click.echo("""
            /\\_/\\
           ( O.O )
            > o <\
            grabbing the current file and all related files""")
        traceback, error_information, repopack = relational_error_parsing_function(entrypoint, "-r")
        if len(traceback) > 0 and len(error_information) > 0 and len(repopack) > 0:
            context = error_information + repopack
            step1 = process(command, traceback, context)
            user_response, error_data = terminalstep1(step1)
            if user_response and error_data:
            # User clicked Yes, prompt the agent to change the files
                await asyncio.run(start_file_writer_agent())
                await asyncio.run(apply_changes(error_data))
    elif is_global:
        click.echo("""
            \
            /\\_/\\
           ( O.O )
            > o <\
            this feature is not implemented yet. exiting now""")
        return
    elif project_type == "python" and "main.py" in command:
        handle_fastapi_project(command)
        if user_response:
                # User clicked Yes, prompt the agent to change the files
                asyncio.run(apply_changes(json.loads(step1)))
        else:
            click.echo("There was an issue running your code")
    else:
        traceback, error_information, repopack = relational_error_parsing_function(entrypoint)
        
        if len(traceback) > 0 and len(error_information) > 0 and len(repopack) > 0:
            context = error_information + repopack
            step1 = process(command, traceback, context)
            user_response, error_data = terminalstep1(step1)
            if error_data and user_response:
                # User clicked Yes, prompt the agent to change the files
                asyncio.run(start_file_writer_agent())
                asyncio.run(apply_changes(error_data))
        else:
            click.echo("""
                /\\_/\\
               ( >:< )
                > - <\
                there was an issue running your code (check if that file exists) or there were no issues :)""")
            return

    kill_process_on_port(8000)

@cli.command()
def init():
    click.echo(f'Init command executed')
    return

async def apply_changes(error_data):
    request = ErrorCorrectionRequest(response=error_data)
    try:
        response = requests.post(
            "http://localhost:8000/apply_correction",
            json=request.json(),
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                click.echo("Changes have been applied successfully.")
            else:
                click.echo(f"Failed to apply changes: {result.get('message', 'Unknown error')}")
        else:
            click.echo(f"Failed to apply changes: HTTP {response.status_code}")
    except requests.RequestException as e:
        click.echo(f"Error applying changes: {str(e)}")

def handle_fastapi_project(command):
    click.echo("Analyzing FastAPI project...")

    if os.path.isfile(command):
        project_dir = os.path.dirname(command)
        main_file = os.path.basename(command)
    else:
        project_dir = command
        main_file = 'main.py'
    server_process = subprocess.Popen(
        shlex.split(command),
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
        user_response = terminalstep1(explanation)# This will print only the GROQ API response
        if user_response:
            # User clicked Yes, prompt the agent to change the files
            asyncio.run(apply_changes(json.loads(explanation)))
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

async def start_file_writer_agent():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    agent_path = os.path.join(script_dir, 'agents', 'file_writer_agent.py')

    def run_agent():
        subprocess.run([sys.executable, agent_path])

    thread = threading.Thread(target=run_agent)
    thread.daemon = True
    thread.start()

    # Wait for the server to start
    for _ in range(10):  # Try for 10 seconds
        try:
            requests.get("http://localhost:8000")
            print("File writer agent server is running.")
            return
        except requests.ConnectionError:
            time.sleep(1)

    print("Failed to start file writer agent server.")

if __name__ == '__main__':
    cli()
