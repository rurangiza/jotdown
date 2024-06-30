from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

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


class Librarian(LLM):
    """
    The Librarian stores and retrieves notes based on user needs
    """
    pass


if __name__ == '__main__':
    llm = LLM()
    print(llm.ask("who is Elon Musk?"))

