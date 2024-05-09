import os
from tempfile import gettempdir

import click
import httpx
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger

from .summary import summarize_html


@click.command()
@click.argument("url", type=click.STRING)
@click.option("-l", "--lang", type=click.STRING, default="English")
def main(url: str, lang: str) -> None:
    load_dotenv(find_dotenv())

    lang = os.getenv("HTML_SUMMARY_LANG", lang)

    resp = httpx.get(url=url)
    resp.raise_for_status()

    f = os.path.join(gettempdir(), "temp.html")
    with open(f, "wb") as fp:
        fp.write(resp.content)

    s = summarize_html(f, lang)
    logger.info("summarization:\n{}", s)
