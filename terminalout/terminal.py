import json
from prompt_toolkit.formatted_text import to_formatted_text, HTML
from prompt_toolkit import print_formatted_text, HTML
from prompt_toolkit.shortcuts import prompt, PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from agents.file_writer_agent import file_writer, ErrorCorrectionRequest, FileWriteResponse 


# Initialize the file_writer agent
file_writer_agent = file_writer


def terminalstep1(json_object):
    data = json.loads(json_object)
    #Print where and what
    print_formatted_text(HTML("<b><skyblue>Where error occurs:</skyblue></b>"))
    print_formatted_text(HTML("<b><blue>Line Number:</blue></b>"), data['where']["line_number"])
    print_formatted_text(HTML("<b><blue>File Path:</blue></b>"), data['where']["file_name"])
    print_formatted_text(HTML("<b><blue>Error Type:</blue></b>"), data['what']["error_type"])
    print_formatted_text(HTML("<b><skyblue>What error is:</skyblue></b>"), data["what"]["description"])
    #user can select if they wanna see the solution

    options = ['y', 'n']
    current_index = 0
    kb = KeyBindings()

    @kb.add('left')
    def select_yes(event):
        nonlocal current_index
        current_index = 0  # Select 'y'
        update_display(event.app)

    @kb.add('right')
    def select_no(event):
        nonlocal current_index
        current_index = 1  # Select 'n'
        update_display(event.app)

    @kb.add('enter')
    def confirm_selection(event):
        event.app.exit()

    def update_display(app):
        """Update the displayed selection."""
        display_string = (
            f"\rDo you want to see the solution?: "
            f"YES/no" if current_index == 0 else
            f""
            f"\rDo you want to see the solution and apply changes?: "
            f"yes/NO" if current_index == 1 else
            f""
        )
        app.output.write(display_string)
        app.output.flush()

    # Prompt the user to make a selection
    session = PromptSession(key_bindings=kb)
    update_display(session.app)  # Initial display
    session.prompt("")  # Start prompt

    if options[current_index] == 'y':
        print_formatted_text(HTML("<b><ansigreen>How to fix error:</ansigreen></b>"), data['how'])
        return True
    else:
        print_formatted_text(HTML("<b><ansigreen>No changes will be applied.</ansigreen></b>"))
        return False
