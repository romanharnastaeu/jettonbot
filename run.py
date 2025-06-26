import asyncio
from src.app.bot import BoltBot

async def main():
    bot = BoltBot()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main()) 