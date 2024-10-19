import os
import click
import errortrace
from handlers import fastapi_handlers

@click.group()
def cli():
   """A CLI that helps you squash bugs and understand what went wrong in your code. Use it as a learning tool or have it complete your code for you!"""
   pass

@cli.command()
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

if __name__ == '__main__':
    print("DEBUG: Starting SPLAT CLI")
    cli()
