from enum import Enum, auto
from langchain.schema.language_model import BaseLanguageModel


class ModelProvider(Enum):
    OpenAI = "openai"
    ChatGlm = "chatglm"


def get_model(model_info: dict[str, str]) -> BaseLanguageModel:
    provider = model_info['_model_provider']
    if provider == ModelProvider.OpenAI.value:
        from langchain.chat_models import ChatOpenAI
        return ChatOpenAI(model_name=model_info['name'], temperature=model_info['temperature'],
                          max_tokens=model_info['max_tokens'])
    elif provider == ModelProvider.ChatGlm.value:
        from langchain.llms.chatglm import ChatGLM
        return ChatGLM(endpoint_url=model_info['url'], temperature=model_info['temperature'],
                       max_token=model_info['max_tokens'])
    else:
        raise ValueError(f"Unsupported model provider: {provider}")


def model_base_info() -> dict[str, str]:
    return {
        'provider': 'openai',
        'temperature': '0.7',
        'max_tokens': '2000',
    }
