# agent_handler.py
from agents.file_writer_agent import FileWriteRequest, FileWriteResponse, file_writer

async def apply_changes(file_path: str, proposed_changes: str) -> bool:
    file_write_request = FileWriteRequest(
        file_path=file_path,
        content=proposed_changes
    )
    
    # Send the request to the file writer agent
    result = await file_writer.send(file_write_request)
    
    if isinstance(result, FileWriteResponse):
        if result.success:
            print("Changes have been applied to the file by the agent.")
            return True
        else:
            print("Failed to apply changes. Error:", result.message)
            return False
    else:
        print("Unexpected response from file writer agent.")
        return False

def run_file_writer_agent():
    file_writer.run()