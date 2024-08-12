import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.document import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from datetime import date
from curses import wrapper

from jotdown.ui import Editor, CLI

from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
from langchain_core.documents import Document


GPT3 = "gpt-3.5-turbo-0125"
GPT4 = "gpt-4o"


class LLM:
    """
    Parent class of every more specialized LLM classes
    - Scribe
    - Librarian
    """
    tokens_count = 0
    openai_calls = 0

    def __init__(self, model=GPT3, temperature=0.2) -> None:
        self._llm = ChatOpenAI(
            model=model,
            temperature=temperature,
        )
        self._template = ChatPromptTemplate.from_template("""{prompt}""")

    def ask(self, question: str) -> str:
        chain = self._template | self._llm
        response = chain.invole({'prompt': question})
        return response.content


class Scribe(LLM, Editor):
    """
    Records and cleans notes
    """
    def __init__(self) -> None:
        LLM.__init__(self)
        Editor.__init__(self)
        self.__MIN_WORDS = 20
        self.__system_msg = """\
        You are a note-cleaning assistant. Your goal is to clean the text below delimited by triple backticks.
        By cleaning I specifically mean:\
        - Correct any spelling or grammatical errors.\
        - Ensure clarity by rephrasing sentences if needed, while keeping the original meaning intact.\
        - Maintain the original structure and context of the notes.\

        The note: ```{context}```
        """
        self.__template = ChatPromptTemplate.from_messages(
            [
                ("system", self.__system_msg),
                ("human", "{prompt}")
            ]
        )

    def take_notes(self) -> dict:
        """ Get user input in curse window """
        note: dict = wrapper(self.input)
        return note

    def __clean(self, note: str) -> str:
        """ Cleans note while maintaining original meaning """
        chain = self.__template | self._llm
        response = chain.invoke({"prompt": note})
        return response.content


class Librarian(LLM, CLI):
    """
    The Librarian stores and retrieves notes based on user needs
    """
    def __init__(self, db_name="./db/notes") -> None:
        LLM.__init__(self)
        CLI.__init__(self)
        self.__template = ChatPromptTemplate.from_template("""
        Answer the user's question in a concise and confident way, based on the context given below and your knowledge.
        Context: ```{context}```
        Question: {input}
        """)
        self.__embedding_model = OllamaEmbeddings(model='mxbai-embed-large')
        self.__db =  Chroma(
            collection_name="daily-notes",
            embedding_function=self.__embedding_model,
            persist_directory= db_name
        )
        self.__docs_count = self.__db._collection.count()
    
    def chat(self):
        placeholder = "Ask anything about your notes"
        if (count := self.__docs_count) < 4:
            print(f"Not enough documents writtent ({count})")
            return
        while (question := self.input(msg=">>", placeholder=placeholder)) != "exit!":
            response = self.retrieve(question)            
            self.stream(response['answer'])

    def store(self, newnote: dict) -> None:
        # turn text into document
        if newnote['words_count'] == 0:
            return
        
        doc = Document(
            page_content = newnote['content'],
            metadata = {
                "date" : str(date.today()),
                "words_count": newnote['words_count'],
            },
            id = str(uuid4())
        )
        self.__db.add_documents(documents=[doc])

    def retrieve(self, question: str) -> str:
        if question == "#soft-exit#":
            return {"answer": "No question asked."}
        chain = self.__create_chain()
        if not chain:
            return {"answer": "There are no notes to be found.\nFirst write one."}
        response = chain.invoke({
            "input": question
        })
        return response


    def __create_chain(self):  # TODO: what return type?
        # same as: chain = template | llm
        # pass list of documents into the chain
        chain = create_stuff_documents_chain(
            llm=self._llm,
            prompt=self.__template
        )
        # retrieve the most relevant documents in vector store
        
        retriever = self.__db.as_retriever()
        retrieval_chain = create_retrieval_chain(
            retriever,
            chain
        )
        return retrieval_chain


if __name__ == '__main__':
    llm = LLM()
    print(llm.ask("who is Elon Musk?"))
