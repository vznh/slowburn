import os
import errortrace
import click

'''
def cli():
    """A CLI that helps you squash bugs and understand what went wrong in your code. Use it as a learning tool or have it complete your code for you!"""
    pass
'''
@click.command()
@click.argument('command')
@click.option('-f','--file', is_flag=True,help='Load the current file and dependent files into LLM')
@click.option('-r','--repo', is_flag=True, help="Load the entire repository into the LLM")
def cli(command, file, repo):
    """A CLI that helps you squash bugs and understand what went wrong in your code. Use it as a learning tool or have it complete your code for you!"""
    if file:
        print("bello")
    elif repo:
        print("baibai")
    else:
        errortrace.splat_find(command)

if __name__ == '__main__':
    cli()
