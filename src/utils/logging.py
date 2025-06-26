import logging
from pathlib import Path
from ..app.config import get_settings

class BotLogger:
    def __init__(self):
        self.settings = get_settings()
        self.logger = logging.getLogger('bolt_bot')
        self._setup_logger()
        
    def _setup_logger(self):
        """Setup logger configuration"""
        # Create logs directory
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Set logging level
        level = logging.DEBUG if self.settings.DEBUG else logging.INFO
        self.logger.setLevel(level)
        
        # Create handlers
        file_handler = logging.FileHandler(
            log_dir / 'bot.log',
            encoding='utf-8'
        )
        console_handler = logging.StreamHandler()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def debug(self, msg: str):
        self.logger.debug(msg)
        
    def info(self, msg: str):
        self.logger.info(msg)
        
    def warning(self, msg: str):
        self.logger.warning(msg)
        
    def error(self, msg: str, exc_info=True):
        self.logger.error(msg, exc_info=exc_info)

# Create global logger instance
logger = BotLogger() 