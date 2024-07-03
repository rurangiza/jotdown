import pinecone
from dotenv import load_dotenv, find_dotenv

from pinecone import Pinecone, ServerlessSpec

import os
import uuid


load_dotenv(find_dotenv())
# pc = Pinecone(api_key='PINECONE_API_KEY')
# INDEX_NAME = ""


class VectorDB:

    def __init__(self, index_name):
        self.__pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.INDEX_NAME = self.__create_index_name(index_name)

        if self.INDEX_NAME in [index.name for index in pinecone.list_indexes()]:
            pinecone.delete_index(self.INDEX_NAME)
        pinecone.create_index(
            name=self.INDEX_NAME,
            dimension=None # TODO: get embedding model (OpenAI)
        )

    def __create_index_name(self, index_name):
        openai_key = os.getenv("OPENAI_API_KEY") or uuid.uuid4()
        return f'{index_name}-{openai_key[-36].lower().replace("_", "-")}'

    def __repr__(self):
        return f'VectorDB({self.INDEX_NAME})'

    def __str__(self):
        return f"""Vector Database:
        - index_name: {self.INDEX_NAME}
        - api: {self.api[:3]}...{self.api[-3:]}
        """


if __name__ == "__main__":
    vdb = VectorDB("jotdown")
    print(vdb)

