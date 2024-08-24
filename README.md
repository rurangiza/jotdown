# Jotdown
### Your CLI note-taking companion
Jotdown is a note-taking app for devs. Everything is done in the terminal, during the week you can only take notes, and on sundays you can ask questions about your notes for review.

![](./assets/walkthrough.gif)

## How it works
Jotdown is basically 2 features, taking notes and asking questions about the notes. Here is how both are implemented:

1. __Taking notes__
    
    I used the [ncurses](https://docs.python.org/3/howto/curses.html) library to provide a better user experience. It allowed me to do the following which is not possible with the standard input function.
   - multi-line writing and editing like in normal text editors
   - show word count, to know when you hit your daily words goal
   - show custom messages while writing
   - custom actions based on key-press (press ESC to exit)

    Once you finish taking notes, it is saved in a vector database so that when I want to review my week, I can retrieve relevent notes to answer my questions.


2. __Asking questions about the notes__

    After retrieving notes that are relevant to my question, I add them as context to the API call to OpenAI.
    I used Langchain as framework to interact with OpenAI and format my prompt templates.

## Improvements
- [ ] use ncurses editor => text editing
- [ ] add more tests
- [ ] use github actions for automated testing
- [ ] add real token streaming
- [ ] publish as a pip package
