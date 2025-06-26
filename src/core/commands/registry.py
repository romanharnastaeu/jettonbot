from typing import Dict, Type, List, Optional
from .base import Command
from ...utils.logging import logger

class CommandRegistry:
    def __init__(self):
        self.commands: Dict[str, Command] = {}
        
    def register(self, command: Command) -> None:
        """Register a command"""
        self.commands[command.name] = command
        logger.info(f"Registered command: {command.name}")
        
    def get_command(self, text: str) -> Optional[Command]:
        """Get command that matches text"""
        text = text.lower()
        for command in self.commands.values():
            if command.matches(text):
                return command
        return None
        
    def get_all_commands(self) -> List[Command]:
        """Get all registered commands"""
        return list(self.commands.values()) 