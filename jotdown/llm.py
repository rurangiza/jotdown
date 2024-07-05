import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from datetime import datetime
from typing import List
import curses

from jotdown.inout import prompt, stream, TextArea, WordCounter

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


class Scribe(LLM):
    """
    Records and cleans notes
    """
    def __init__(self) -> None:
        super().__init__()
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

    def record(self, stdscr, target_words=10):
        """ Get user input in curse window """
        stdscr.clear()

        wc = WordCounter(target_words)
        area = TextArea()

        stdscr.nodelay(True)

        text = ""

        while wc <= target_words:
            wc.display()
            character = area.get()
            text += character
            area.print(character)
            if character.isspace():
                wc += 1
        stdscr.getch()
        return text

    def record_old(self) -> str:
        """ Get user input """
        user_input: List[str] = []
        word_count: int = 0
        try:
            while True:
                ans: str = prompt("...")
                if ans == "#soft-exit#":
                    if word_count >= self.__MIN_WORDS:
                        break
                    stream(f"{self.__MIN_WORDS - word_count} more words to write")
                    continue
                user_input.append(ans)
                word_count += len(ans.split())
        except EOFError as _:
            pass
        except KeyboardInterrupt as _:
            pass
        note: str = "\n".join(user_input)
        stream(f"You've written {word_count} words")

        # do something: clean, summarize or other
        if not note:
            return ""
        return self.__clean(note)

    def __clean(self, note: str) -> str:
        """ Cleans note while maintaining original meaning """
        chain = self.__template | self._llm
        response = chain.invoke({"prompt": note})
        return response.content


class Librarian(LLM):
    """
    The Librarian stores and retrieves notes based on user needs
    """
    def __init__(self) -> None:
        super().__init__()
        self.__template = ChatPromptTemplate.from_template("""
        Answer the user's question in a concise and confident way, based on the context given below and your knowledge.
        Context: ```{context}```
        Question: {input}
        """)
        self.__vector_store = None

    def __text_to_doc(self, text: str) -> Document:
        """ Turns text into a document """
        # Metadata: date, time, tags, category
        document = Document(
            page_content=text,
            metadata={
                'datetime': str(datetime.now()),
                'category': ['thoughts', 'ideas'], # TODO: should be dynamic
            }
        )
        return document

    def __create_db(self, docs: Document) -> None:
        """ Turns document into embeddings """
        embedding = OpenAIEmbeddings()
        self.__vector_store = FAISS.from_documents([docs], embedding=embedding)

    def __create_chain(self):  # TODO: what return type?
        # same as: chain = template | llm
        # pass list of documents into the chain
        chain = create_stuff_documents_chain(
            llm=self._llm,
            prompt=self.__template
        )
        # retrieve must relevant document in vector store
        retriever = self.__vector_store.as_retriever()
        retrieval_chain = create_retrieval_chain(
            retriever,
            chain
        )
        return retrieval_chain

    def store(self, text: str) -> None:
        # turn text into document
        docs = self.__text_to_doc(text)
        self.__create_db(docs)
        print("Finished storing the note.")

    def retrieve(self, question: str) -> str:
        chain = self.__create_chain()
        response = chain.invoke({
            "input": question
        })
        return response


if __name__ == '__main__':
    llm = LLM()
    print(llm.ask("who is Elon Musk?"))

