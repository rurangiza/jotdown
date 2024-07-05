# Jotdown
### Your CLI note-taking companion

> [!Important]
> This README is not finished and the app is not ready for use. Check the to-do list [below](#to-dos-v1) for current features.

Jotdown is a note-taking app for devs that live in the terminal. With the added bonus that you can ask questions about all the notes you've taken.

## Features
- take notes in your terminal
- ask questions about your notes with LLM+RAG

## Try it
> [!Warning]
> Not working yet. This serves as the usage goal while building.

1. install: `pip install jotdown-tool`
2. write `jotdown` in your terminal

```bash
$ jotdown
>> Want to write or chat? (SELECT)
>> - write
>> - chat
```

If you pick `write`. Start writing:

```bash
... your text goes here
...
```

If you pick `chat`. Ask a question about your notes:
```bash
: what were my notes about last week?
```

## How it works
- RAG

## To-do's (v1)
Fixes
- [ ] vdb: add notes instead of replacing

Features
- [x] take user input and output in streams (chunks of text)
- [x] add minimum word requirements
- [x] convert note to document, with metadata like daytime, content tags,..
- [x] store document in vector store (FAISS or Pinecone)
- [x] retrieve relevant notes to answer a question (similarity search, hybrid search)
- [ ] add chat history
- [ ] word countdown while typing (curses)

Enhancements
- [ ] use function calling
- [ ] use local db instead of in-memory db
- [ ] add automated testing (pytest, mypy, github actions)
- [ ] add class attributes to monitor token usage and api calls to openai
- [ ] support additional context (ex: notion pages, personal files)

User Experience
- [ ] use curses for better UX
