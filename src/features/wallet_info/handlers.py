from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from ...services.user_service import UserService
from ...services.price_service import PriceService
from ...infrastructure.ton_api.client import TonApiClient
from ...utils.logging import logger

class WalletInfoHandlers:
    def __init__(
        self,
        user_service: UserService,
        price_service: PriceService,
        ton_client: TonApiClient
    ):
        self.user_service = user_service
        self.price_service = price_service
        self.ton_client = ton_client
        
    async def handle_wallet_info_menu(self, update: Update, context: CallbackContext) -> None:
        """Display wallet info menu (public queries only)"""
        query = update.callback_query
        await query.answer()
        
        await query.message.edit_text(
            "🔍 *Wallet Information*\n\n"
            "Enter a TON wallet address to get public information.\n"
            "*No personal data is stored.*",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")
            ]]),
            parse_mode='Markdown'
        )
        
    async def handle_public_wallet_query(self, update: Update, context: CallbackContext, address: str) -> None:
        """Display public wallet information without storing user data"""
        try:
            # Get wallet info
            account_info = await self.ton_client.get_account_info(address)
            if not account_info:
                raise ValueError("Could not fetch wallet data")
                
            # Build message
            message = "*Public Wallet Information*\n\n"
            
            # Add TON balance
            ton_balance = float(account_info.get('balance', 0))
            ton_price = self.price_service.get_price('TON')
            ton_value = ton_balance * ton_price if ton_price else 0
            message += f"💎 *{ton_balance:.2f} TON* (${ton_value:.2f})\n\n"
            
            # Add jettons
            jettons = await self.ton_client.get_jettons(address)
            if jettons:
                message += "*Jetton Balances:*\n"
                for token in jettons:
                    balance = float(token.get('balance', 0))
                    symbol = token.get('symbol', '').upper()
                    
                    # Add price info for known tokens
                    price = self.price_service.get_price(symbol)
                    if price:
                        value = balance * price
                        message += f"• {symbol}: *{balance:.2f}* (${value:.2f})\n"
                    else:
                        message += f"• {symbol}: *{balance:.2f}*\n"
                        
            # Add wallet address
            message += f"\n*Wallet Address:*\n`{address}`\n"
            message += f"[View on Explorer](https://tonviewer.com/{address})\n\n"
            message += "*Note: This is public blockchain data. No personal information is stored.*"
            
            keyboard = [[
                InlineKeyboardButton("⬅️ Back", callback_data="main_menu")
            ]]
            
            await update.message.reply_text(
                message,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
            
        except Exception as e:
            logger.error(f"Error in wallet query: {e}")
            await update.message.reply_text(
                "❌ Error fetching wallet information.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("⬅️ Back", callback_data="main_menu")
                ]])
            ) 