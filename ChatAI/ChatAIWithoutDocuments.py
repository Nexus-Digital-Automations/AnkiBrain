import json
from os import path
from typing import Tuple

from langchain import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

from .ChatInterface import ChatInterface
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

user_data_dir = path.join(path.abspath(path.dirname(__file__)), "..", "user_files")

settings_path = path.join(user_data_dir, "settings.json")


class ChatAIWithoutDocuments(ChatInterface):
    def __init__(self, verbose=False):
        # Import here to avoid linting issues with imports
        import sys
        import os

        sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
        from model_compatibility import get_compatible_model_name, log_model_usage

        temperature = 0
        model_name = "gpt-3.5-turbo"
        with open(settings_path, "r") as f:
            data = json.load(f)
            temperature = data["temperature"]
            model_name = data["llmModel"]

        # Apply model compatibility mapping for unsupported models (e.g., GPT-5)
        compatible_model = get_compatible_model_name(model_name)
        log_model_usage(model_name, compatible_model)

        self.llm = ChatOpenAI(temperature=temperature, model_name=compatible_model)
        self.memory = ConversationBufferMemory()
        self.conversationChain = ConversationChain(
            llm=self.llm, memory=self.memory, verbose=verbose
        )

    def human_message(self, query: str) -> Tuple[str, None]:
        return self.conversationChain.predict(input=query), None

    def clear_memory(self):
        self.memory.clear()
