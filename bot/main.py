import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.app.handlers import router, init_model
from app.data.movielens import load_ratings, load_item_names
from app.model.item_based import build_similarity_matrix

load_dotenv()

DATA_PATH = os.getenv("DATA_PATH", "ml-100k/u.data")
ITEM_PATH = os.getenv("ITEM_PATH", "ml-100k/u.item")
BOT_KEY = os.getenv("BOT_KEY")


async def main() -> None:
    print("Загрузка данных...")
    matrix = load_ratings(DATA_PATH)
    item_names = load_item_names(ITEM_PATH)

    print("Вычисление матрицы сходства Пирсона...")
    sim_matrix = build_similarity_matrix(matrix)

    init_model(matrix, sim_matrix, item_names)

    bot = Bot(token=BOT_KEY)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("бот выключен")
