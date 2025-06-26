# 🤖 BOLT Telegram Bot Framework

A professional, modular Telegram bot framework built for the TON blockchain ecosystem. This bot provides real-time cryptocurrency data, wallet analysis, and community features with a clean, scalable architecture.

## 🚀 Features

### 💰 Cryptocurrency Integration
- **Real-time Price Tracking**: Live TON and BOLT token prices with automatic updates
- **Multi-API Support**: Integrated with CoinGecko and TON API for reliable data
- **Price Caching**: Intelligent caching system to minimize API calls and improve performance

### 🔍 Blockchain Analysis
- **Wallet Information Queries**: Retrieve detailed wallet information including:
  - TON balance with USD valuation
  - Jetton holdings and balances
  - Transaction history analysis
  - Direct blockchain explorer integration
- **Smart Contract Integration**: Pre-configured with BOLT token contract addresses

### 🌐 Community Features
- **Curated Links**: Access to official channels, community chats, and resources
- **Social Media Integration**: Direct links to Twitter, Medium, and GitHub
- **Trading Platform Integration**: Quick access to DeDust and other DEX platforms

### 🏗️ Technical Architecture
- **Modular Design**: Clean separation of concerns with feature-based modules
- **Dependency Injection**: Professional IoC container for service management
- **Async/Await**: Full asynchronous architecture for optimal performance
- **Type Safety**: Complete type annotations with Pydantic models
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Caching Layer**: Built-in memory caching with TTL support
- **State Management**: Session-based conversation state handling

## 🛠️ Technical Stack

- **Python 3.11+**: Modern Python with latest features
- **python-telegram-bot 20.7**: Latest Telegram Bot API wrapper
- **Pydantic**: Data validation and settings management
- **aiohttp**: Asynchronous HTTP client for API calls
- **dependency-injector**: Professional dependency injection framework

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed
- **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)
- **TON API Key** from [TON API](https://tonapi.io/) (optional but recommended)

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/bolt-telegram-bot.git
cd bolt-telegram-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Required: Get from @BotFather
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Optional: Get from https://tonapi.io/
TON_API_KEY=your_ton_api_key_here

# Optional: Enable debug logging
DEBUG=true
```

### 4. Run the Bot
```bash
python run.py
```

## 🏗️ Architecture Overview

```
src/
├── app/                    # Application Core
│   ├── bot.py             # Main bot application
│   ├── config.py          # Configuration management
│   └── container.py       # Dependency injection setup
├── core/                   # Business Logic
│   ├── commands/          # Command system
│   ├── models/            # Data models
│   └── state_manager.py   # Conversation state
├── features/              # Feature Modules
│   ├── community/         # Community links & info
│   ├── prices/            # Price tracking & display
│   ├── tracking/          # Wallet queries
│   └── wallet_info/       # Detailed wallet analysis
├── infrastructure/        # External Services
│   ├── cache/             # Caching implementations
│   ├── price_api/         # Price data providers
│   ├── storage/           # Data persistence
│   └── ton_api/           # TON blockchain API
├── services/              # Business Services
│   ├── price_service.py   # Price management
│   └── user_service.py    # Session management
└── utils/                 # Utilities
    ├── errors.py          # Custom exceptions
    ├── logging.py         # Logging configuration
    └── middleware.py      # Request middleware
```

## 🔧 Configuration Options

All configuration is handled through environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BOT_TOKEN` | Telegram bot token from BotFather | - | ✅ |
| `TON_API_KEY` | TON API key for blockchain queries | - | ❌ |
| `DEBUG` | Enable debug logging | `true` | ❌ |
| `PRICE_UPDATE_INTERVAL` | Price update frequency (seconds) | `60` | ❌ |
| `CACHE_TTL` | Default cache TTL (seconds) | `300` | ❌ |
| `MAX_RETRIES` | API request retry limit | `3` | ❌ |

## 🧩 Extending the Bot

### Adding New Features

1. **Create Feature Module**:
```python
# src/features/my_feature/handlers.py
from telegram import Update
from telegram.ext import CallbackContext

class MyFeatureHandlers:
    async def handle_my_command(self, update: Update, context: CallbackContext):
        await update.message.reply_text("Hello from my feature!")
```

2. **Register in Container**:
```python
# src/app/container.py
my_feature_handlers = providers.Singleton(MyFeatureHandlers)
```

3. **Add to Bot**:
```python
# src/app/bot.py
self.app.add_handler(CommandHandler('mycommand', my_feature.handle_my_command))
```

### Custom API Integration

```python
# src/infrastructure/my_api/client.py
class MyApiClient:
    async def get_data(self) -> dict:
        async with self.session.get(f"{self.base_url}/data") as response:
            return await response.json()
```

### Adding New Commands

```python
# src/core/commands/my_command.py
from .base import Command

class MyCommand(Command):
    def __init__(self):
        super().__init__()
        self.name = "mycommand"
        self.description = "My custom command"
    
    async def execute(self, update: Update, context: CallbackContext):
        await update.message.reply_text("Command executed!")
```

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src
```

## 📊 Performance Features

- **Async Architecture**: Full async/await for concurrent request handling
- **Connection Pooling**: Reused HTTP connections for API calls
- **Smart Caching**: Multi-level caching with different TTL strategies
- **Rate Limiting**: Built-in protection against API rate limits
- **Error Recovery**: Automatic retry logic with exponential backoff

## 🔐 Security Features

- **Environment Variables**: No hardcoded secrets in source code
- **Input Validation**: Pydantic models for all data validation
- **Error Sanitization**: Safe error messages without sensitive data exposure
- **Session Isolation**: Proper session management without data leakage

## 🚀 Deployment Options

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/
CMD ["python", "run.py"]
```

### Systemd Service
```ini
[Unit]
Description=BOLT Telegram Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 run.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 🤝 Contributing

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Follow Code Style**: Use type hints and docstrings
4. **Add Tests**: Ensure new features have test coverage
5. **Update Documentation**: Keep README and docstrings current
6. **Submit Pull Request**

### Code Style Guidelines

- Use type hints for all functions and methods
- Follow PEP 8 naming conventions
- Add docstrings for all public methods
- Keep functions focused and single-purpose
- Use dependency injection for service dependencies

## 📝 API Reference

### Core Services

#### PriceService
```python
class PriceService:
    async def get_price(self, symbol: str) -> Optional[float]
    async def start_tracking(self) -> None
    async def stop_tracking(self) -> None
```

#### TonApiClient
```python
class TonApiClient:
    async def get_account_info(self, address: str) -> Optional[Dict]
    async def get_jettons(self, address: str) -> Optional[Dict]
```

## 🐛 Troubleshooting

### Common Issues

**Bot doesn't respond**:
- Check bot token validity
- Ensure bot is started with `/start` in Telegram
- Verify network connectivity

**API errors**:
- Check API key configuration
- Verify rate limits aren't exceeded
- Check API service status

**Performance issues**:
- Monitor cache hit rates
- Check database connection pooling
- Review async/await usage

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [TON API Documentation](https://tonapi.io/docs)
- [Python Telegram Bot Library](https://python-telegram-bot.readthedocs.io/)
- [TON Blockchain Documentation](https://ton.org/docs/)

---

**Built with ❤️ for the TON ecosystem** 