from abc import ABC, abstractmethod
from typing import Optional, List
from telegram import Update
from telegram.ext import CallbackContext

class Command(ABC):
    def __init__(self):
        self.name: str = ""
        self.description: str = ""
        self.aliases: List[str] = []
        
    @abstractmethod
    async def execute(self, update: Update, context: CallbackContext) -> None:
        """Execute the command"""
        pass
        
    def matches(self, text: str) -> bool:
        """Check if text matches command or its aliases"""
        text = text.lower()
        return text == self.name or text in self.aliases 