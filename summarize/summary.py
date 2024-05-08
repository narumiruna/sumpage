import functools

from langchain.cache import SQLiteCache
from langchain.chains.llm import LLMChain
from langchain.globals import set_llm_cache
from langchain_community.document_loaders.html_bs import BSHTMLLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from loguru import logger

set_llm_cache(SQLiteCache())


PROMPT_TEMPLATE = """使用台灣用語的繁體中文，幫以下的文章以條列的方式，寫簡潔的摘要：
{text}

摘要："""


@functools.cache
def get_chain() -> LLMChain:
    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo")
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain


def summarize_html(f: str) -> str:
    logger.info("summarize html: {}", f)

    loader = BSHTMLLoader(f)
    docs: list[Document] = loader.load()

    text = "\n".join([doc.page_content for doc in docs])

    chain = get_chain()
    return chain.invoke({"text": text})["text"]
