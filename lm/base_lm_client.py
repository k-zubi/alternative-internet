from abc import ABC, abstractmethod


class BaseLMClient(ABC):

    @abstractmethod
    def do_chat_completion(self,
                           messages: list[dict[str, str]],
                           model: str = None,
                           max_completion_tokens: int = None,
                           temperature: float = None,
                           top_p: float = None) -> str:
        pass

    @abstractmethod
    def do_streaming_chat_completion(self,
                                     messages: list[dict[str, str]],
                                     model: str = None,
                                     max_completion_tokens: int = None,
                                     temperature: float = None,
                                     top_p: float = None) -> str:
        pass
