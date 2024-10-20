from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

def process(error_message: str, context: str):
    client = Groq(api_key=os.getenv("API"))

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""Act as a software debugging expert with a strong understanding of error messages and traceback analysis. Remember these steps in detail:
                Step one, a user executes an erroneous command that give the error of type python error. 
                Step two, the user uses a "splat" command, which subsequently packages all related files to the source node where the error occurred. 
                Step three, with the packaged files, we graph all files related to the error traceback that occurred at the source node in the respository.
                Step 4, With the packaged files and now the relations, you will receive a txt file to process following the next instructions."""
            },
            {
                "role": "system",
                "content": """Provide a detailed and clear explanation of a given error traceback message in natural language. 
                Describe what the error indicates, how it occurred, and the implications it may have on the code. 
                Additionally, pinpoint the exact location in the repository (with specified file name and line number) where the error occurred.
                You are to output a JSON structure with interface: { 'where': { 'line_number': str, 'file_path': str, 'type': str }, 'what': str, 'how': str }"""
            },
            {
                "role": "user",
                "content": f"Context: {context}\n\nError message: {error_message}"
            }
        ],
        model="llama3-70b-8192",
        response_format={"type": "json_object"}
    )
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    print(process("test error message", "test context"))