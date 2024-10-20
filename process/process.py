# [START process/process.py]
from groq import Groq
import os
import json
from dotenv import load_dotenv
from terminalout.terminal import terminalstep1

load_dotenv()

def process(traceback_message: str, original_error_information: str, context: str) -> object:
  client = Groq(api_key=os.getenv("API"))

  chat_completion = client.chat.completions.create(
    messages=[
        {
          "role": "system",
          "content": "You are an expert software debugging assistant specializing in Python error analysis. Your task is to analyze error tracebacks and provide structured, actionable advice. Follow these steps precisely:"
        },
        {
          "role": "system",
          "content": "1. Analyze the provided error traceback and original error message.\n2. Identify the source of the error within the repository structure.\n3. Explain the error concisely in natural language.\n4. Provide specific, actionable suggestions for resolving the error.\n5. Format your response as a JSON object with the exact structure specified below."
        },
        {
          "role": "system",
          "content": "Your response MUST be a valid JSON object with this exact structure:\n{\n  \"where\": {\n    \"repository_path\": \"<absolute path to repository>\",\n    \"file_name\": \"<name of file containing error>\",\n    \"line_number\": \"<line number where error occurred>\"\n  },\n  \"what\": {\n    \"error_type\": \"<specific Python error type>\",\n    \"description\": \"<concise explanation of error>\"\n  },\n  \"how\": {\n    \"error_origination\": \"<line number where error originated>\",\n    \"suggested_code_solution\": \"<code snippet to fix the error>\"\n  }\n}"
        },
        {
          "role": "system",
          "content": "Constraints:\n- Provide ONLY the JSON object as your response. Do not include any other text.\n- Ensure all JSON keys are exactly as specified.\n- The 'suggested_code_solution' should be a valid Python code snippet without explanation.\n- If multiple errors exist, focus on the most critical one that likely caused the others.\n- Do not use placeholders in your response. Provide specific, contextual information based on the given error."
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

if __name__ == "__main__":
   print(process(["test.py"], """File "/Users/vinh/Documents/calhacks24/test.py", line 2
          print(hello
               ^
      SyntaxError: '(' was never closed"""))
