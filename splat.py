import os
import click
import errortrace
from handlers import fastapi_handlers
import errortrace
import click
from process.process import groq_process

from utils.utils import build_dependency_graph, detect_framework_or_language, extract_filename_with_extension, get_related_details

'''
@click.command()
@click.option('--project-dir', default='.', help='Path to the project directory')
@click.option('--framework', type=click.Choice(['fastapi', 'django', 'flask']), default='fastapi', help='Web framework used in the project')
def find(project_dir, framework):
    """Find and analyze bugs in your web project."""
    print(f"DEBUG: Starting find command with project_dir: {project_dir} and framework: {framework}")
    project_dir = os.path.abspath(project_dir)
    click.echo(f"Analyzing {framework.capitalize()} project in {project_dir}...")

    if framework == 'fastapi':
        handle_fastapi_project(project_dir)
    elif framework == 'django':
        click.echo("Django support not yet implemented.")
    elif framework == 'flask':
        click.echo("Flask support not yet implemented.")
    else:
        click.echo(f"Unsupported framework: {framework}")

def handle_fastapi_project(project_dir):
    click.echo("Starting the FastAPI server. Please interact with the application to trigger errors.")
    click.echo("The tool will capture any errors that occur during the next 30 seconds.")
    click.echo("You can access the application at http://localhost:8000")
    click.echo("Try accessing endpoints like /users, /items, or /process to trigger errors.")

    error_message = fastapi_handlers.compile_project(project_dir)

    print(f"DEBUG: Checking for errors in output")
    if "error" not in error_message.lower() and "exception" not in error_message.lower():
        click.echo("No errors found during the capture period.")
        return

    click.echo("Errors found. Analyzing...")
    fastapi_handlers.process_error(error_message)
    """A CLI that helps you squash bugs and understand what went wrong in your code. Use it as a learning tool or have it complete your code for you!"""
    pass
'''

languages_supported = ['go', 'rust','kotlin','scala','swift','r','perl','lua','julia','c','java','typescript','python']

@click.command()
@click.argument('command')
@click.option('-r','--related', is_flag=True,help='Load the file and imported files to load into the LLM')
@click.option('-g','--is_global', is_flag=True, help="Load the entire repository into the LLM using repopack")
def cli(command, related, is_global):
    """A CLI that helps you squash bugs and understand what went wrong in your code. Use it as a learning tool or have it complete your code for you!"""
    project_type = detect_framework_or_language(command)
    if project_type in languages_supported:
        language = project_type
        cwd = extract_filename_with_extension(command)
    else:
        cwd = os.getcwd()
    if related:
        '''
        print("bello")
        files = []
        files.append(cwd)
        file_and_dependencies = build_dependency_graph(files)
        print('file and dependencies', file_and_dependencies)
        '''
    elif is_global:
        print("baibai")

    else:
        error_trace = errortrace.splat_find(command)
        if error_trace:
            llm_response = groq_process(command, error_trace)
            click.echo(llm_response)
        else:
            click.echo("There was an issue running your code")
if __name__ == '__main__':
    print("DEBUG: Starting SPLAT CLI")
    cli()
