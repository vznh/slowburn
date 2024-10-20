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
                "role": "system", #what is the output displayed
                "content": """Provide a detailed and clear explanation of a given error traceback message in natural language.
                Describe what the error indicates, how it occurred, and the implications it may have on the code.
                Additionally, pinpoint the exact location in the repository (with specified file name and line number) where the error occurred.
                Finally, give suggestions for how to approach resolving the error, including debugging techniques and best practices, preventative measures or coding standards that could be adopted in the future to avoid similar mistakes. 
                Ensure that the response is structured, informative, and provides actionable advice for the user.
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

'''def explain(step1response):
    client = Groq(api_key=os.getenv("API"))
    chat_completion = client.chat.completions.create(
        messages=[
        {   "role": "system", #context, how did we get here?
            "content": f"""Act as a software debugging expert with a strong understanding of error messages and traceback analysis. Remember these steps in detail:
            Step one, a user executes an erroneous command that give the error of type python error.
            Step two, the user uses a "splat" command, which subsequently packages all related files to the source node where the error occurred.
            Step three, with the packaged files, we graph all files related to the error traceback that occurred at the source node in the respository.
            Step 4, With the packaged files and now the relations, you will receive a txt file to process following the next instructions."""
        },
        {"role": "user",
        "content": """Given the following JSON input that describes an error in code: { 'where': { 'line_number': str, 'file_path': str, 'type': str }, 'what': str, 'how': str },
        generate a detailed explanation of the error identified in the code.This explanation should include: 1.A clear identification of the error based on the 'what' field, 2.
        The significance of the error in the context of the code located at 'file_path' at the specified 'line_number', 3.A description of the type of error indicated in the 'type' field,
        4.Common causes for this type of error to help the user understand potential pitfalls, 5.Suggestions for how to approach resolving the error, including debugging techniques and best practices,
        6.Preventative measures or coding standards that could be adopted in the future to avoid similar mistakes.Ensure that the response is structured, informative, and provides actionable advice for the user."""
        }
        ],
        model="llama3-70b-8192",
        response_format={"type":"json_object"}
    )
    return chat_completion.choices[0].message.content #need a return type for function'''

if __name__ == "__main__":
   print(process(["test.py"], """File "/Users/vinh/Documents/calhacks24/test.py", line 2
          print(hello
               ^
      SyntaxError: '(' was never closed"""))
