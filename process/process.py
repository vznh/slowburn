# [START process/process.py]
from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

def process(traceback_message: str, original_error_information: str, context: str) -> object:
  client = Groq(api_key=os.getenv("API"))

  chat_completion = client.chat.completions.create(
    messages=[
      {
        "role": "system",
        "content": f"""Act as a software debugging expert with a strong understanding of error messages and traceback analysis. Remember these steps in detail:
        Step one, a user executes an erroneous command that give a Python error.
        Step two, the user uses a "splat" command, which subsequently packages all related files to the source node where the error occurred.
        Step three, with the packaged files, we graph all files related to the error traceback that occurred at the source node in the respository.
        Step 4, With the packaged files and now the relations, you will receive a txt file relating to all files in the error trace to process following the next instructions."""
      },
      {
        "role": "system", #what is the output displayed
        "content": """Provide a concise and clear kind of nonchalant explanation of a given error traceback message in natural language.
        Describe what the error indicates, how it occurred, and the implications it may have on the code.
        Additionally, pinpoint the exact location in the repository (with specified file name and line number) where the error occurred.
        Finally, give suggestions for how to approach resolving the error, including debugging techniques and best practices, preventative measures or coding standards that could be adopted in the future to avoid similar mistakes.
        Ensure that the response is structured, informative, and provides actionable advice for the user. There also could be multiple errors.
        You are to output a JSON object with interface: { 'where': { "repository_path": str, "file_name": str, "line_number": str }, 'what': { "error_type": str, "description": str }, 'how': { "error_origination": line_number, "suggested_code_solution": str } }; where: Where are the files did we detect the error to be mostly originate in? Their paths as an absolute string? what: In the context of the given code, what was the reasoning behind the error? how: What code segment needs to be replaced, and what is the suggested way to fix it? Provide an object that contains a key value pair, where the key will be the error origination, and the value is the suggested code solution with no explanation, just code. """
      },
      {
        "role": "user",
        "content": f"Context: {context}\n\nTraceback message: {traceback_message}\n\nOriginal error message: {original_error_information}"
      }
    ],
    model="llama3-70b-8192",
    response_format={"type": "json_object"}
  )
  return chat_completion.choices[0].message.content

# [END process/process.py]
