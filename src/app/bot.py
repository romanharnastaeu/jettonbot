import asyncio
from pathlib import Path
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)
from .container import Container
from .config import get_settings

class BoltBot:
    def __init__(self):
        self.settings = get_settings()
        self.container = Container()
        self.app = ApplicationBuilder().token(self.settings.BOT_TOKEN).build()
        
    def register_handlers(self):
        """Register all bot handlers"""
        # Get handler instances
        tracking = self.container.tracking_handlers()
        prices = self.container.price_handlers()
        community = self.container.community_handlers()
        
        # Command handlers
        self.app.add_handler(CommandHandler('start', tracking.handle_tracking_menu))
        
        # Callback query handlers
        self.app.add_handler(CallbackQueryHandler(
            tracking.handle_tracking_menu, 
            pattern='^menu_tracking$'
        ))
        self.app.add_handler(CallbackQueryHandler(
            prices.handle_price_menu,
            pattern='^price_menu$'
        ))
        
        # Message handlers
        self.app.add_handler(MessageHandler(
            filters.Regex(r'^!(болт|тон)$'),
            prices.handle_price_command
        ))
        
        # Add community handlers
        self.app.add_handler(CallbackQueryHandler(
            community.handle_community_menu,
            pattern='^community_menu$'
        ))
        self.app.add_handler(CallbackQueryHandler(
            community.handle_social_media,
            pattern='^social_media$'
        ))
        
    async def start(self):
        """Start the bot"""
        try:
            # Initialize services
            await self.container.ton_client().initialize()
            await self.container.price_client().initialize()
            await self.container.price_service().start()
            
            # Register handlers
            self.register_handlers()
            
            # Start bot
            await self.app.initialize()
            await self.app.start()
            await self.app.updater.start_polling()
            
            # Keep running
            await asyncio.Event().wait()
            
        except Exception as e:
            print(f"Error starting bot: {e}")
            
        finally:
            await self.shutdown()
            
    async def shutdown(self):
        """Shutdown the bot and cleanup"""
        try:
            # Stop services
            await self.container.price_service().stop()
            await self.container.ton_client().close()
            await self.container.price_client().close()
            
            # Stop bot
            if self.app.running:
                await self.app.updater.stop()
                await self.app.stop()
                await self.app.shutdown()
                
        except Exception as e:
            print(f"Error during shutdown: {e}") 