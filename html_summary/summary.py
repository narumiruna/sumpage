import functools

from langchain.chains.llm import LLMChain
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_community.document_loaders.html_bs import BSHTMLLoader
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from loguru import logger

set_llm_cache(SQLiteCache())


PROMPT_TEMPLATE = """Write a concise summary in bullet points using {lang} for the following article:
{text}

Summary:"""


@functools.cache
def get_chain() -> LLMChain:
    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo")
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm
    return chain


def summarize_html(f: str, lang: str = "English") -> str:
    logger.info("summarize html: {}", f)

    loader = BSHTMLLoader(f)
    docs = loader.load()

    text = "\n".join([doc.page_content for doc in docs])

    chain = get_chain()
    ai_message: AIMessage = chain.invoke({"text": text, "lang": lang})
    return ai_message.content
