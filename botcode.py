import asyncio
from aiogram import Bot, Dispatcher
from HIDden import TOKEN
from bot.Handlers import router

bot = Bot(token = TOKEN)
dp = Dispatcher()

async def main():#Запуск бота
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__": #Запуск бота
    #logging.basicConfig(level=logging.INFO)
    asyncio.run(main())