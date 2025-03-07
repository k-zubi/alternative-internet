from typing import Generator, Literal
from openai import OpenAI
from lm.base_lm_client import BaseLMClient
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

class OpenAILMClient(BaseLMClient):
    def __init__(self):
        super().__init__()
        self.client = OpenAI()

    def do_chat_completion(self,
                           messages: list[dict[str, str]],
                           model: str = "o3-mini-2025-01-31",
                           max_completion_tokens: int = 32768,
                           temperature: float = 1,
                           top_p: float = 1,
                           reasoning_effort: Literal["low", "medium", "high"] = "low") -> str:
        for message in messages:
            if message.get("role") == "system":
                message["role"] = "developer"
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            top_p=top_p,
            stream=False,
            reasoning_effort=reasoning_effort
        )
        return response.choices[0].message.content or ""

    def do_streaming_chat_completion(self,
                                     messages: list[dict[str, str]],
                                     model: str = "o3-mini-2025-01-31",
                                     max_completion_tokens: int = 1024,
                                     temperature: float = 1,
                                     top_p: float = 1) -> Generator[str, None, None]:
        pass
