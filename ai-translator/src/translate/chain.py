from typing import Dict, Any, Optional, List

from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.chains.base import Chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, \
    HumanMessagePromptTemplate
from langchain.schema.language_model import BaseLanguageModel

from translate.prompt import SYSTEM_PROMPT_TEMPLATE
from translate.prompt import HUMAN_PROMPT_TEMPLATE
from utils import logger


class TranslationChain(Chain):
    """A chain that translates text from one language to another."""
    llm: BaseLanguageModel
    """The language model used for translation. It should be a language model that supports translation."""
    return_final_only: bool = True
    output_key: str = "text"
    """The key of the output in the return value."""

    # prompt
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT_TEMPLATE),
        HumanMessagePromptTemplate.from_template(HUMAN_PROMPT_TEMPLATE)
    ])

    @property
    def _chain_type(self) -> str:
        return "translation"

    @property
    def input_keys(self) -> List[str]:
        return self.prompt.input_variables

    @property
    def output_keys(self) -> List[str]:
        if self.return_final_only:
            return [self.output_key]
        else:
            return [self.output_key, "final"]

    def _call(self, inputs: Dict[str, Any],
              run_manager: Optional[CallbackManagerForChainRun] = None) -> Dict[str, Any]:
        logger.debug(f"TranslationChain: inputs: {inputs}")
        prompt_value = self.prompt.format_prompt(**inputs)
        resp = self.llm.generate_prompt([prompt_value], callbacks=run_manager.get_child() if run_manager else None)
        return {self.output_key: resp.generations[0][0].text}


if __name__ == "__main__":
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    chain = TranslationChain(llm=llm, verbose=True)
    response = chain.run(source_language="English", target_language="Chinese", text="Hello, world!")
    logger.debug(f"response: {response}")
