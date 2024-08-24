from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.document import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage

from datetime import date
from curses import wrapper

from jotdown.ui import Editor, CLI

from langchain_openai import OpenAIEmbeddings
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

    def __init__(self, model=GPT3, temperature=1) -> None:
        self._llm = ChatOpenAI(
            model = model,
            temperature = temperature,
        )
        self._template = ChatPromptTemplate.from_template("""{prompt}""")

    def ask(self, prompt: str) -> str:
        chain = self._template | self._llm
        response = chain.invoke({'prompt': prompt})
        return response.content


class Scribe(LLM, Editor):
    """
    Records and cleans notes
    """
    def __init__(self) -> None:
        LLM.__init__(self)
        Editor.__init__(self)

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

    def record(self) -> dict:
        """ Get user input in curse window """
        note: dict = wrapper(self.input)
        return note

    def __clean(self, note: str) -> str:
        """ Cleans note while maintaining original meaning """
        chain = self.__template | self._llm
        response = chain.invoke({
            "prompt": note
        })
        return response.content


class Librarian(LLM, CLI):
    """
    The Librarian stores and retrieves notes based on user needs
    """
    def __init__(self, db_name="./db") -> None:
        LLM.__init__(self)
        CLI.__init__(self)

        self.__template = ChatPromptTemplate.from_messages(
            [
                ("system", "Directly answer the user's question in a natural conversational way. Take the context into consideration: {context}"),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ]
        )

        self.__embedding_model = OpenAIEmbeddings(model='text-embedding-3-large')
        self.__db =  Chroma(
            collection_name = "daily-notes",
            embedding_function = self.__embedding_model,
            persist_directory = db_name
        )
        self._chat_history = []
    
    def chat(self):
        placeholder = "Ask anything about your notes"
        while (question := self.input(msg=">>", placeholder=placeholder)) != "exit!":
            self._chat_history.append(HumanMessage(question))
            response = self.retrieve(question)['answer']
            self._chat_history.append(AIMessage(response))
            self.stream(response)

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
        k = 4
        if (count := self.__db._collection.count()) < 4:
            k = count if count > 0 else 1
        if question == "#soft-exit#":
            return {"answer": "No question asked."}
        chain = self.__create_chain(k)
        if not chain:
            return {"answer": "There are no notes to be found.\nFirst write one."}
        return chain.invoke({
            "input": question,
            "chat_history": self._chat_history
        })

    def __create_chain(self, k):  # TODO: what return type?
        # same as: chain = template | llm
        # pass list of documents into the chain
        chain = create_stuff_documents_chain(
            llm=self._llm,
            prompt=self.__template
        )
        
        retriever = self.__db.as_retriever(search_kwargs={"k":k})
        retrieval_chain = create_retrieval_chain(
            retriever,
            chain
        )
        return retrieval_chain

def main():
    llm = LLM()
    ans = llm.ask('what is CUBA?')
    print(ans)