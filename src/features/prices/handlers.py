from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from ...services.price_service import PriceService

class PriceHandlers:
    def __init__(self, price_service: PriceService):
        self.price_service = price_service
        
    async def handle_price_menu(self, update: Update, context: CallbackContext) -> None:
        """Display price menu"""
        query = update.callback_query
        await query.answer()
        
        message = "*💰 Current Token Prices*\n\n"
        
        # Get prices
        ton_price = self.price_service.get_price('TON')
        bolt_price = self.price_service.get_price('BOLT')
        
        if ton_price:
            message += f"💎 *TON*: ${ton_price:.3f}\n"
        if bolt_price:
            message += f"🔩 *BOLT*: ${bolt_price:.6f}\n"
            
        keyboard = [[
            InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")
        ]]
        
        await query.message.edit_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
    async def handle_price_command(self, update: Update, context: CallbackContext) -> None:
        """Handle !price commands"""
        command = update.message.text.lower()
        message = ""
        trade_url = ""
        
        if command == "!болт":
            price = self.price_service.get_price('BOLT')
            message = f"🔩 BOLT: *${price:.4f}*"
            trade_url = "https://dedust.io/swap/TON/BOLT"
        elif command == "!тон":
            price = self.price_service.get_price('TON')
            message = f"💎 TON: *${price:.4f}*"
            trade_url = "https://dedust.io/swap/USDT/TON"
            
        if message:
            keyboard = [[InlineKeyboardButton("💱 TRADE", url=trade_url)]]
            await update.message.reply_text(
                message,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            ) 