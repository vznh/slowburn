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
    print_formatted_text(HTML("🔎 <u><b><gray>Details about <red>error</red></gray></b></u>"))
    print_formatted_text(HTML(f"✅ We found the first instance of the <red><b>error</b></red> at <b><magenta>line {data['where']['line_number']}</magenta></b>."))
    print_formatted_text(HTML(f"✅ The owner of the <b><red>error</red></b>: <b><magenta>{data['where']['file_name']}</magenta></b>."))
    print_formatted_text(HTML(f"✅ The type of the <b><red>error</red></b>: <b><magenta>{data['what']['error_type']}</magenta></b>."))
    print_formatted_text(HTML(f"✅ Isolated <red><b>error</b></red> message: <b><cyan>{data['what']['description']}</cyan></b>"))
    #user can select if they wanna see the solution

    current_index = 0  # 0 for YES, 1 for NO
    kb = KeyBindings()
    options = ['y', 'n']

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

        # Clear the line and print the new options with proper formatting
        app.output.write("\r")  # Carries the cursor back to the start of the line
        print_formatted_text(HTML(f"See suggested change?: {yes_text} / {no_text}   "), end='')  # Ensure no new line is printed

    # Initial display update
    session = PromptSession(key_bindings=kb)
    update_display(session.app)  # Initial display
    session.prompt("")  # Start prompt

    if options[current_index] == 'y':
        print_formatted_text(HTML("<b><ansigreen>How to fix error:</ansigreen></b>"), data['how'])
        return True, data
    else:
        print_formatted_text(HTML("<b><ansigreen>No changes will be applied.</ansigreen></b>"))
        return False, None
