from typing import Generator

from cerebras.cloud.sdk import Cerebras

from lm.base_lm_client import BaseLMClient

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())


class CerebrasLMClient(BaseLMClient):

    def __init__(self):
        super().__init__()
        self.client = Cerebras()

    def do_chat_completion(self,
                           messages: list[dict[str, str]],
                           model: str = "llama3.3-70b",
                           max_completion_tokens: int = 1024,
                           temperature: float = 1,
                           top_p: float = 1) -> str:
        response = self.client.chat.completions.create(
            messages=messages,
            model=model,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            top_p=1,
            stream=False
        )
        return response.choices[0].message.content or ""

    def do_streaming_chat_completion(self,
                                     messages: list[dict[str, str]],
                                     model: str = "llama3.3-70b",
                                     max_completion_tokens: int = 1024,
                                     temperature: float = 1,
                                     top_p: float = 1) -> Generator[str, None, None]:
        stream = self.client.chat.completions.create(
            messages=messages,
            model=model,
            max_completion_tokens=max_completion_tokens,
            temperature=temperature,
            top_p=1,
            stream=True
        )
        for chunk in stream:
            yield chunk.choices[0].delta.content or ""
