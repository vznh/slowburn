import json

def terminal(json_object):
    data = json.loads(json_object)
    #Print where and what
    print("Where error occurs:", data["where"])
    print("What error is:", data["what"])
    #user can select if they wanna see the solution
    show_solution = input("Do you want to see the solution? (y/n): ").strip().lower()
    if show_solution == 'y':
        # If the user chooses "yes", print the "how" key
        print("How to fix error:", data["how"])

#{ 'where': { 'line_number': str, 'file_path': str, 'type': str }, 'what': str, 'how': str }"""

if __name__ == "__main__":
    terminal('''{
   "where": {
      "line_number": "2",
      "file_path": "/Users/vinh/Documents/calhacks24/test.py",
      "type": "SyntaxError"
   },
   "what": "The error indicates that there is a syntax error in the code, specifically an unclosed parenthesis.",
   "how": "The error occurred because the 'print' statement on line 2 of the 'test.py' file is missing a closing parenthesis, which is causing the syntax error."
}''')