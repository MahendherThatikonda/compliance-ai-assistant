# rag_chroma/generation_chroma/llm_client_chroma.py

from openai import OpenAI
from ..utils_chroma.config_chroma import CHAT_MODEL_NAME, OPENAI_API_KEY
from ..utils_chroma.logging_utils_chroma import get_logger

logger = get_logger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)


def call_llm(messages, temperature=0.2):
    """Send messages to GPT and return the assistant reply."""

    logger.info(f"Calling LLM model: {CHAT_MODEL_NAME}")

    response = client.chat.completions.create(
        model=CHAT_MODEL_NAME,
        messages=messages,
        temperature=temperature,
    )

    return response.choices[0].message.content
