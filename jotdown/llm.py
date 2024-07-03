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
from jotdown.inout import prompt, stream

GPT3 = "gpt-3.5-turbo-0125"
GPT4 = "gpt-4o"

class LLM:
    def __init__(self, model=GPT3, temperature=0.2):
        self._llm = ChatOpenAI(
            model=model,
            temperature=temperature,
        )
        self._template = ChatPromptTemplate.from_template("""{prompt}""")

    def ask(self, prompt):
        chain = self._template | self._llm
        response = chain.invole({'prompt': prompt})
        return response.content


class Cleaner(LLM):
    """
    The cleaner helps clean journal entries while keeping the original
    meaning of the notes.
    """

    def __init__(self):
        super().__init__()
        self.__system = """
        You are an advanced note-cleaning assistant. Your task is to help me clean and organize my notes while preserving the original information. Specifically:
        
        Remove any repetition or redundant information.
        Ensure clarity by rephrasing sentences if needed, while keeping the original meaning intact.
        Correct any spelling or grammatical errors.
        Maintain the original structure and context of the notes.
        Summarize long paragraphs without losing key details, if necessary.
        Highlight important points for easy reference.

        Respond in the third person, restating the content of the notes without additional commentary.
        For example, if the input is 'hello, world', the output should be similar to 'You wrote "hello, world"'. If the input is 'I went to school, shared a meal with some friends then started working', the output should be similar to 'You went to school, shared a meal with friends then started working'.
        if the input includes a question like 'who is elon musk', the output should be similar to 'you asked yourself who elon musk is'
        Do not directly quote my notes!
        """
        self.__template = ChatPromptTemplate.from_messages(
            [
                ("system", "{system}"),
                ("human", "note to clean: {text}"),
            ]
        )
    
    def clean(self, text: str) -> str:
        chain = self.__template | self._llm
        response = chain.invoke({
            'system': self.__system,
            'text': text,
        })
        return response.content


class Scribe(LLM):
    def __init__(self):
        super().__init__()
        self.__MIN_WORDS = 20

    def record(self):
        ############################################
        # Get the note
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

        # Summarize it using chatGPT

        if not note:
            return ""
        return note

class Librarian(LLM):
    """
    The Librarian stores and retrieves notes based on user needs
    """
    def __init__(self):
        super().__init__()
        self.__template = ChatPromptTemplate.from_template("""
        Answer the user's question:
        Context: {context}
        Question: {input}
        """)
        self.__vector_store = None

    def __text_to_doc(self, text):
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

    def __create_db(self, docs):
        """ Turns document into embeddings """
        embedding = OpenAIEmbeddings()
        self.__vector_store = FAISS.from_documents([docs], embedding=embedding)

    def __create_chain(self):
        # chain = self.__template | self._llm
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

    def store(self, text):
        # turn text into document
        docs = self.__text_to_doc(text)
        self.__create_db(docs)
        return docs

    def retrieve(self, question):
        chain = self.__create_chain()
        response = chain.invoke({
            "input": question
        })
        return response

if __name__ == '__main__':
    llm = LLM()
    print(llm.ask("who is Elon Musk?"))

