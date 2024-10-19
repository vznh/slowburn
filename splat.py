import os
import errortrace

@click.group()
def cli():
    """A CLI that helps you squash bugs and understand what went wrong in your code. Use it as a learning tool or have it complete your code for you!"""
    pass

@click.command(name="find")
@click.option('-f','--file', is_flag=True,help='Load the current file and dependent files into LLM')
@click.option('-r','--repo', is_flag=True, help="Load the entire repository into the LLM")
def bug_splat(file, repo):
    if file:
        print("bello")
    elif repo:
        print("baibai")
    else:
        errortrace.splat_find()

if __name__ == '__main__':
    cli()
