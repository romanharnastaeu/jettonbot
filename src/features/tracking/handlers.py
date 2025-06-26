from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from ...services.user_service import UserService
from ...services.price_service import PriceService
from ...infrastructure.ton_api.client import TonApiClient

class TrackingHandlers:
    def __init__(
        self,
        user_service: UserService,
        price_service: PriceService,
        ton_client: TonApiClient
    ):
        self.user_service = user_service
        self.price_service = price_service
        self.ton_client = ton_client
        
    async def handle_wallet_query_menu(self, update: Update, context: CallbackContext) -> None:
        """Display wallet query menu (no tracking, just queries)"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [
            [InlineKeyboardButton("🔍 Query Wallet", callback_data="query_wallet")],
            [InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")]
        ]
        
        await query.message.edit_text(
            "🔍 *Wallet Query*\n\n"
            "Query wallet information without tracking:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
    async def handle_wallet_query(self, update: Update, context: CallbackContext) -> None:
        """Handle wallet query (temporary, no storage)"""
        address = update.message.text.strip()
        
        # Validate address exists
        account_info = await self.ton_client.get_account_info(address)
        if not account_info:
            await update.message.reply_text(
                "❌ Invalid address or account not found."
            )
            return
            
        # Show wallet info without storing
        balance = float(account_info.get('balance', 0))
        await update.message.reply_text(
            f"✅ Wallet Query Result:\n"
            f"💎 Balance: {balance:.2f} TON\n"
            f"📍 Address: `{address}`\n\n"
            f"*Note: This is a temporary query. No data is stored.*",
            parse_mode='Markdown'
        ) 