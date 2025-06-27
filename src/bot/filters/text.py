from aiogram.filters import BaseFilter
from aiogram.types import Message


class Text(BaseFilter):
    def __init__(self, text: str | list[str]):
        if isinstance(text, str):
            text = [text]
        self.text = text

    async def __call__(self, message: Message) -> bool:
        return message.text in self.text if message.text else False
