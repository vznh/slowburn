import json
import os
import subprocess
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
import requests
import time
from utils.utils import detect_framework_or_language, extract_filename_with_extension
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
    if not command:
        click.echo("""
            /\\_/\\
           ( >:< )
            > - <\
            please provide a command or file to analyze""")
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
            user_response = terminalstep1(step1)
    elif is_global:
        click.echo("""
            \
            /\\_/\\
           ( O.O )
            > o <\
            this feature is not implemented yet. exiting now""")
        return ("""
            ( o.o )
            > ^ <
            welcome to splat...
            """)
        click.echo(f"Detected project type: {project_type}")

        if project_type == "python" and "main.py" in command:
            handle_fastapi_project(command)
        else:
            error_trace = errortrace.splat_find(command)
            if error_trace:
                step1 = process(command, error_trace)
                user_response = terminalstep1(step1)
                if user_response:
                    # User clicked Yes, prompt the agent to change the files
                    asyncio.run(apply_changes(json.loads(step1)))
            else:
                click.echo("There was an issue running your code")
    else:
        #error_trace = errortrace.splat_find(command)
        traceback, error_information, repopack = relational_error_parsing_function(entrypoint)
        if len(traceback) > 0 and len(error_information) > 0 and len(repopack) > 0:
            context = error_information + repopack
            step1 = process(command, traceback, context)
            user_response = terminalstep1(step1)
        else:
            click.echo("""
                /\\_/\\
               ( >:< )
                > - <\
                there was an issue running your code or there were no issues :)""")
            return

@cli.command()
def init():
    click.echo(f'Init command executed')
    return

async def apply_changes(error_response):
    request = ErrorCorrectionRequest(response=error_response)

    # Create a context for the file writer agent
    ctx = file_writer._build_context()
    print(ctx)

    # Create a future to wait for the response
    response_future = asyncio.Future()
    print(response_future)

    # Define a callback to handle the response
    async def response_handler(ctx: Context, sender: str, msg: FileWriteResponse):
        response_future.set_result(msg)

    # Register the temporary response handler
    handler_key = file_writer.on_message(FileWriteResponse)(response_handler)
    print(handler_key)

    try:
        # Send the ErrorCorrectionRequest to the agent
        await ctx.send(file_writer.address, request)

        # Wait for the response
        response = await asyncio.wait_for(response_future, timeout=10.0)
        print(response)

        if response.success:
            click.echo("Changes have been applied successfully.")
        else:
            click.echo(f"Failed to apply changes: {response.message}")
    except asyncio.TimeoutError:
        click.echo("Timeout waiting for response from file writer agent")
    except Exception as e:
        click.echo(f"Error applying changes: {str(e)}")
    finally:
        # Remove the temporary response handler
        if handler_key in file_writer._signed_message_handlers:
            file_writer._signed_message_handlers.pop(handler_key)
        elif handler_key in file_writer._unsigned_message_handlers:
            file_writer._unsigned_message_handlers.pop(handler_key)


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

if __name__ == '__main__':
    asyncio.run(file_writer.setup())
    cli()
