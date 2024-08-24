import os
import getpass


if not os.environ['OPENAI_API_KEY']:
    os.environ['OPENAI_API_KEY'] = getpass.getpass("Paste OpenAI API key: ")