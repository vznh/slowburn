import astor
from uagents import Agent, Context, Model
from pathlib import Path
import ast

class CodeModificationRequest(Model):
    directory: str
    modification_type: str
    details: dict

code_modifier = Agent(name="code_modifier", seed="code_modifier_seed")

@code_modifier.on_message(model=CodeModificationRequest)
async def modify_code(ctx: Context, sender: str, msg: CodeModificationRequest):
    directory = Path(msg.directory)

    if not directory.is_dir():
        await ctx.send(sender, f"Error: {directory} is not a valid directory.")
        return

    for file_path in directory.glob('**/*.py'):
        try:
            with open(file_path, 'r') as file:
                tree = ast.parse(file.read())

            modified = False

            if msg.modification_type == "add_function":
                modified = add_function(tree, msg.details)
            elif msg.modification_type == "modify_function":
                modified = modify_function(tree, msg.details)
            elif msg.modification_type == "add_import":
                modified = add_import(tree, msg.details)

            if modified:
                with open(file_path, 'w') as file:
                    file.write(astor.to_source(tree))
                ctx.logger.info(f"Modified {file_path}")

        except Exception as e:
            ctx.logger.error(f"Error processing {file_path}: {str(e)}")

    await ctx.send(sender, "Code modification completed.")

def add_function(tree, details):
    function_def = ast.parse(details['function_code']).body[0]
    tree.body.append(function_def)
    return True

def modify_function(tree, details):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == details['function_name']:
            new_function = ast.parse(details['new_function_code']).body[0]
            node.body = new_function.body
            return True
    return False

def add_import(tree, details):
    import_stmt = ast.Import(names=[ast.alias(name=details['module_name'], asname=details['alias'])])
    tree.body.insert(0, import_stmt)
    return True

if __name__ == "__main__":
    code_modifier.run()
