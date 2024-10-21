# 🔥 slowburn

slowburn is based off of splat, our CalHacks 2024 entry. I, and all my teammates were a big fan of what we made, so I wanted to make changes to eventually use it in my own program. You may see some initial contributions from my initial teammates.

## Inspiration 
~~splat~~ slowburn is a tool that combines your compile/runtime errors and grabs context from every crevice to deliver a highly educated, concise debug response. This is perfect for whenever you have an error that you can't find, there is a need for more contextual error response, or component errors are plaguing your program -- which provides an option to be quickly fixed, understood, and prevented for later in the future. 

The name was inspired by the way I felt while programming this app.

## Features
- **AI-Optimized**: We use an extremely fast inference model [Groq](https://groq.com/) in order to produce an instant debug error, with a large amount of context
- **Simple to Use**: <ins>splat</ins> can be used out-of-the-box and globally in any project without any configuration.
- **Git Aware**: <ins>splat</ins> takes into consideration your .gitignore files so that we won't use any sensitive info.
- **Highly Contextual**: You can use <ins>splat</ins> with a `-r` flag, grabbing all nodes to the Nth degree related to all error stack files in order to grab the most related content, delivering a highly accurate, optimized, and contextual debug response.

## Known Bugs
- <ins>splat</ins> will not conform to any formatting configurations when inserting code
- <ins>splat</ins> does not do well with running sub-module entrypoints that do not originate in the root directory
  
## Quick Start
You can use <ins>splat</ins> out of the box:  

`splat squash <?-r> <!entrypoint>`.

Example:
Just like you would enter your app, do so with <ins>splat</ins>.  

`splat squash "python3 foo.py"`

`splat squash -r "python3 main.py"`

And that's it!
