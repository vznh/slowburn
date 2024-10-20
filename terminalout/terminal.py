import json
from prompt_toolkit.formatted_text import to_formatted_text, HTML
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import prompt, PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style


def terminalstep1(json_object):
    data = json.loads(json_object)
    #Print where and what
    print_formatted_text(HTML("🔎 <u><b><gray>Details about <red>error</red></gray></b></u>"))
    print_formatted_text(HTML(f"✅ We found the first instance of the <red><b>error</b></red> at <b><magenta>line {data['where']['line_number']}</magenta></b>."))
    print_formatted_text(HTML(f"✅ The owner of the <b><red>error</red></b>: <b><magenta>{data['where']['file_name']}</magenta></b>."))
    print_formatted_text(HTML(f"✅ The type of the <b><red>error</red></b>: <b><magenta>{data['what']['error_type']}</magenta></b>."))
    print_formatted_text(HTML(f"✅ Isolated <red><b>error</b></red> message: <b><cyan>{data['what']['description']}</cyan></b>"))
    #user can select if they wanna see the solution

    current_index = 0  # 0 for YES, 1 for NO
    kb = KeyBindings()

    @kb.add('left')  # Select 'YES'
    def select_yes(event):
        nonlocal current_index
        current_index = 0  # Select 'y'
        update_display(event.app)

    @kb.add('right')  # Select 'NO'
    def select_no(event):
        nonlocal current_index
        current_index = 1  # Select 'n'
        update_display(event.app)

    @kb.add('enter')  # Confirm selection
    def confirm_selection(event):
        event.app.exit()

    def format_bold(text):
        return f"<u><yellow>{text}</yellow></u>"

    def format_regular(text):
        return f"<white>{text}</white>"

    def update_display(app):
        """Update the displayed selection."""
        yes_text = format_bold("Yes") if current_index == 0 else format_regular("Yes")
        no_text = format_bold("No") if current_index == 1 else format_regular("No")

        # Clear the line and print the new options with proper formatting
        app.output.write("\r")  # Carries the cursor back to the start of the line
        print_formatted_text(HTML(f"See suggested change?: {yes_text} / {no_text}   "), end='')  # Ensure no new line is printed

    # Initial display update
    session = PromptSession(key_bindings=kb)
    update_display(session.app)  # Initial display
    session.prompt("")  # Start prompt

    if current_index == 0:  # If 'y' was selected
        print_formatted_text(HTML(f"<b><ansigreen>How to fix error:</ansigreen></b> <b>{data['how']['suggested_code_solution']}</b>"))
if __name__ == "__main__":
    step1('''{
   "where": {
      "line_number": "2",
      "file_path": "/Users/vinh/Documents/calhacks24/test.py",
      "type": "SyntaxError"
   },
   "what": "The error indicates that there is a syntax error in the code, specifically an unclosed parenthesis.",
   "how": "The error occurred because the 'print' statement on line 2 of the 'test.py' file is missing a closing parenthesis, which is causing the syntax error."
}''')
