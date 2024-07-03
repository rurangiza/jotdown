# Jotdown
### Your CLI note-taking companion

> [!Important]
> This README is not finished and the app is not ready for use. Check the to-do list [below](#to-dos-v1) for current features.

Jotdown is a note-taking app for devs that live in the terminal. With the added bonus that you can ask questions about all the notes you've taken. 

### How it works
- RAG

### Try it
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

If you pick `chat`. Ask away! The LLM will answer based on your previous notes and its own knowledge.
```bash
: what were my notes about last week?
```

### To-do's (v1)
Features
- [x] take user input and output in streams (chunks of text)
- [x] add minimum word requirements
- [x] convert note to document, with metadata like daytime, content tags,..
- [x] store document in vector store (FAISS or Pinecone)
- [x] retrieve relevant notes to answer a question (similarity search, hybrid search)
- [ ] add chat history
- [ ] support additional context (ex: notion pages)

Improvements
- [ ] use function calling
- [ ] use local db instead of in-memory db

User Experience
- [ ] use curses for better UX


#### Useful Links
- Terms: [LLM](https://youtu.be/zjkBMFhNj_g?si=9AeYiS8D-dtSxyjK), system message, prompt, context window, [embeddings](https://platform.openai.com/docs/guides/embeddings?lang=python), vector database ([1](https://www.pinecone.io/learn/vector-database/), [2](https://python.langchain.com/v0.2/docs/integrations/vectorstores/pinecone/)), search (similarity, hybrid...)
- Function calling: [Langchain](https://python.langchain.com/v0.1/docs/modules/model_io/chat/function_calling/)
- Conversational Memory: [Doc](https://python.langchain.com/v0.1/docs/use_cases/chatbots/memory_management/), [video](https://www.youtube.com/watch?v=X05uK0TZozM)