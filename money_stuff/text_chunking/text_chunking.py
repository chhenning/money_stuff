import os
import json

import requests

from pydantic import BaseModel, Field
from typing import Literal, List

from dotenv import load_dotenv

load_dotenv()


class TextChunk(BaseModel):
    id: int = Field(..., description="The chunk ID assigned by LLM.")
    chunk: str = Field(..., description="The text chunk.")


class TextChunks(BaseModel):
    chunks: List[TextChunk] = Field(..., description="List of text chunks.")


def chunk_text(text: str) -> TextChunks:
    try:
        system_prompt = os.getenv("TEXT_CHUNKING_SYSTEM_PROMPT", "")
        user_prompt = os.getenv("TEXT_CHUNKING_USER_PROMPT", "")
        if not system_prompt or not user_prompt:
            raise ValueError(
                "TEXT_CHUNKING_SYSTEM_PROMPT and TEXT_CHUNKING_USER_PROMPT must be set in the environment variables"
            )

        llama_server = os.getenv("LLAMA_SERVER_URL", "")
        if not llama_server:
            raise ValueError(
                "LLAMA_SERVER_URL must be set in the environment variables"
            )

        schema = TextChunks.model_json_schema()

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_prompt + "\n\n" + text,
            },
        ]

        payload = {
            "messages": messages,
            "temperature": 0,
            "response_format": {
                "type": "json_object",
                "schema": schema,  # schema-constrained JSON
            },
        }

        response = requests.post(
            url=f"{llama_server}/v1/chat/completions",
            data=json.dumps(payload),
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        return TextChunks.model_validate_json(content)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
