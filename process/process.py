from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

def process(repo: list[str], traceback: str):
    client = Groq(api_key=os.getenv("API"))

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system", #context, how did we get here?
                "content": f"""Act as a software debugging expert with a strong understanding of error messages and traceback analysis. Remember these steps in detail:
                Step one, a user executes an erroneous command that give the error of type python error. 
                Step two, the user uses a "splat" command, which subsequently packages all related files to the source node where the error occurred. 
                Step three, with the packaged files, we graph all files related to the error traceback that occurred at the source node in the respository.
                Step 4, With the packaged files and now the relations, you will receive a txt file to process following the next instructions."""
                #Taken out: 
                #If the user calls 'splat -r', all parent and child files connected to src will be packaged. OR 'splat -r' packages all parent and child files connected to [src]
                #If the user calls 'splat -g', all files in the repository will be packaged. OR 'splat -g' operates to package all files in the specified the repository.
            },
            {
                "role": "system", #what is the output displayed
                "content": """Provide a detailed and clear explanation of a given error traceback message in natural language. 
                Describe what the error indicates, how it occurred, and the implications it may have on the code. 
                Additionally, pinpoint the exact location in the repository (with specified file name and line number) where the error occurred.
                You are to output a JSON structure with interface: { 'where': { 'line_number': str, 'file_path': str, 'type': str }, 'what': str, 'how': str }"""
            },
            {
                "role": "user", #this is the real question, solve this question
                "content": f"Use {traceback} for the error message, and {repo} for the list of repositories."
            }
        ],
        model="llama3-70b-8192",  # Choose your model
        response_format={"type": "json_object"}
    )
    return chat_completion.choices[0].message.content #need a return type for function

if __name__ == "__main__":
   print(process(["test.py"], """File "/Users/vinh/Documents/calhacks24/test.py", line 2
          print(hello
               ^
      SyntaxError: '(' was never closed"""))