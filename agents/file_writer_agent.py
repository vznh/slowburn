# file_writer_agent.py
from uagents import Agent, Context, Model
import os
import json

class FileWriteRequest(Model):
    file_path: str
    content: str

class FileWriteResponse(Model):
    success: bool
    message: str

class ErrorCorrectionRequest(Model):
    response: dict

class ErrorCorrectionResponse(Model):
    success: bool
    message: str

file_writer = Agent(name="file_writer", seed="file_writer_seed", port=8000, endpoint="http://localhost:8000/submit")


@file_writer.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {file_writer.name} agent @ {file_writer.address}")

@file_writer.on_message(model=FileWriteRequest)
async def write_to_file(ctx: Context, sender: str, msg: FileWriteRequest):
    try:
        with open(msg.file_path, 'w') as file:
            file.write(msg.content)
        ctx.logger.info(f"Successfully wrote to file: {msg.file_path}")
        await ctx.send(sender, FileWriteResponse(success=True, message=f"File {msg.file_path} updated successfully"))
    except Exception as e:
        error_message = f"Error writing to file {msg.file_path}: {str(e)}"
        ctx.logger.error(error_message)
        await ctx.send(sender, FileWriteResponse(success=False, message=error_message))

@file_writer.on_message(model=ErrorCorrectionRequest)
async def apply_error_correction(ctx: Context, sender: str, msg: ErrorCorrectionRequest):
    try:
        response = msg.response
        file_path = os.path.join(response['where']['repository_path'], response['where']['file_name'])
        line_number = response['where']['line_number']
        suggested_code = response['how'][0]['suggested_code_solution']

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        if 0 < line_number <= len(lines):
            lines[line_number - 1] = suggested_code + '\n'

            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)
        else:
            raise IndexError("Line number out of range")

        ctx.logger.info(f"Successfully applied correction to file: {file_path}")
        await ctx.send(sender, FileWriteResponse(success=True, message=f"File {file_path} updated successfully"))
    except Exception as e:
        error_message = f"Error applying correction: {str(e)}"
        ctx.logger.error(error_message)
        await ctx.send(sender, FileWriteResponse(success=False, message=error_message))

@file_writer.on_rest_post("/apply_correction", ErrorCorrectionRequest, ErrorCorrectionResponse)
async def handle_error_correction(ctx: Context, request: ErrorCorrectionRequest) -> ErrorCorrectionResponse:
    try:
        await apply_error_correction(ctx, file_writer.address, request)
        return ErrorCorrectionResponse(success=True, message="Error correction applied successfully")
    except Exception as e:
        print(str(e))
        return ErrorCorrectionResponse(success=False, message=f"Error applying correction: {str(e)}")


if __name__ == "__main__":
    print("Starting file writer agent server on http://localhost:8000")
    file_writer.run()
