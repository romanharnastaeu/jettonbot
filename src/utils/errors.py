from typing import Optional, Type
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from .logging import logger

class BotError(Exception):
    """Base class for bot errors"""
    def __init__(self, message: str, user_message: Optional[str] = None):
        super().__init__(message)
        self.user_message = user_message or "An error occurred. Please try again."

class ValidationError(BotError):
    """Raised when input validation fails"""
    pass

class APIError(BotError):
    """Raised when external API calls fail"""
    pass

class StorageError(BotError):
    """Raised when storage operations fail"""
    pass

async def handle_error(
    update: Update,
    context: CallbackContext,
    error: Exception,
    error_type: Optional[Type[BotError]] = None
) -> None:
    """Handle different types of errors"""
    try:
        if isinstance(error, error_type or BotError):
            user_message = error.user_message
        else:
            user_message = "An unexpected error occurred. Please try again later."
            
        logger.error(f"Error handling update: {error}", exc_info=error)
        
        if update.callback_query:
            await update.callback_query.message.edit_text(
                f"❌ {user_message}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")
                ]])
            )
        else:
            await update.message.reply_text(
                f"❌ {user_message}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")
                ]])
            )
            
    except Exception as e:
        logger.error(f"Error in error handler: {e}", exc_info=e) 