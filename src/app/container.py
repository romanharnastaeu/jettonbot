from dependency_injector import containers, providers
from ..infrastructure.storage.json_storage import JsonRepository
from ..infrastructure.ton_api.client import TonApiClient
from ..infrastructure.price_api.client import PriceApiClient
from ..services.user_service import UserService
from ..services.price_service import PriceService
from ..features.tracking.handlers import TrackingHandlers
from ..core.models.user import User
from .config import get_settings
from ..features.prices.handlers import PriceHandlers
from ..utils.logging import logger
from ..features.wallet_info.handlers import WalletInfoHandlers
from ..features.community.handlers import CommunityHandlers
from ..core.state_manager import StateManager
from ..infrastructure.cache.memory_cache import MemoryCache
from ..core.commands.registry import CommandRegistry

class Container(containers.DeclarativeContainer):
    config = providers.Singleton(get_settings)
    
    # Infrastructure
    user_repository = providers.Singleton(
        JsonRepository,
        file_path=config().USER_DATA_FILE,
        model_class=User
    )
    
    ton_client = providers.Singleton(TonApiClient)
    price_client = providers.Singleton(PriceApiClient)
    
    # Services
    user_service = providers.Singleton(
        UserService,
        user_repository=user_repository
    )
    
    price_service = providers.Singleton(
        PriceService,
        price_client=price_client
    )
    
    # Feature Handlers
    tracking_handlers = providers.Singleton(
        TrackingHandlers,
        user_service=user_service,
        price_service=price_service,
        ton_client=ton_client
    )
    
    logger = providers.Object(logger)
    
    price_handlers = providers.Singleton(
        PriceHandlers,
        price_service=price_service
    )
    
    wallet_info_handlers = providers.Singleton(
        WalletInfoHandlers,
        user_service=user_service,
        price_service=price_service,
        ton_client=ton_client
    )
    
    community_handlers = providers.Singleton(
        CommunityHandlers
    )
    
    # New providers
    state_manager = providers.Singleton(
        StateManager,
        expiry_minutes=config().STATE_EXPIRY_MINUTES
    )
    
    cache = providers.Singleton(MemoryCache)
    
    command_registry = providers.Singleton(CommandRegistry) 