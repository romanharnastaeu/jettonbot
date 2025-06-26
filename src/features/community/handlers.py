from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from ...utils.middleware import error_handler
from ...utils.logging import logger

class CommunityHandlers:
    @error_handler
    async def handle_community_menu(self, update: Update, context: CallbackContext) -> None:
        """Display community menu with links"""
        query = update.callback_query
        await query.answer()
        
        message = "*🌐 BOLT Community Links*\n\n"
        
        # Official Channels
        message += "*📢 Official Channels:*\n"
        message += "• [BOLT Foundation](https://t.me/boltfoundation)\n"
        message += "• [Daite BOLT](https://t.me/daitebolt)\n"
        message += "• [Boltoshi](https://t.me/boltoshi)\n\n"
        
        # Community Chats
        message += "*💬 Community Chats:*\n"
        message += "• [Daite BOLT Chat](https://t.me/daiteboltchat)\n"
        message += "• [This is BOLT](https://t.me/this_is_bolt)\n\n"
        
        # Trading & Analytics
        message += "*📊 Trading & Analytics:*\n"
        message += "• [DeDust](https://dedust.io/swap/TON/BOLT)\n"
        message += "• [TON Whales](https://tonwhales.com/explorer/token/BOLT)\n"
        
        keyboard = [
            [InlineKeyboardButton("📱 Social Media", callback_data="social_media")],
            [InlineKeyboardButton("📊 Analytics", callback_data="analytics")],
            [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]
        ]
        
        await query.message.edit_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        
    @error_handler
    async def handle_social_media(self, update: Update, context: CallbackContext) -> None:
        """Display social media links"""
        query = update.callback_query
        await query.answer()
        
        message = "*📱 BOLT Social Media*\n\n"
        message += "• [Twitter](https://twitter.com/bolt_ton)\n"
        message += "• [Medium](https://medium.com/@bolt_ton)\n"
        message += "• [GitHub](https://github.com/bolt-ton)\n"
        
        keyboard = [[
            InlineKeyboardButton("⬅️ Back", callback_data="community_menu")
        ]]
        
        await query.message.edit_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown',
            disable_web_page_preview=True
        ) 