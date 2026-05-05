import pandas as pd
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot.app import keyboards as kb
from app.inference.recommend import recommend_new
from app.data.movielens import search_movie

router = Router()

matrix: pd.DataFrame | None = None
sim_matrix: pd.DataFrame | None = None
item_names: dict[int, str] | None = None

user_data: dict[int, dict] = {}


def init_model(m: pd.DataFrame, sm: pd.DataFrame, names: dict[int, str]) -> None:
    global matrix, sim_matrix, item_names
    matrix = m
    sim_matrix = sm
    item_names = names


def get_data(uid: int) -> dict:
    if uid not in user_data:
        user_data[uid] = {"ratings": {}, "pending": None, "state": "waiting_movie"}
    return user_data[uid]


@router.message(CommandStart())
async def cmd_start(message: Message):
    uid = message.from_user.id
    user_data[uid] = {"ratings": {}, "pending": None, "state": "waiting_movie"}
    await message.answer("Привет! Я рекомендую фильмы.\nВведите название фильма, который вы смотрели:")


@router.message(F.text)
async def process_text(message: Message):
    uid = message.from_user.id
    data = get_data(uid)
    text = message.text.strip()
    state = data["state"]

    if state == "waiting_movie":
        results = search_movie(text, item_names)
        if not results:
            await message.answer("Фильм не найден. Попробуйте другое название:")
            return
        item_id, title = results[0]
        data["pending"] = item_id
        data["state"] = "waiting_rating"
        await message.answer(f'Нашёл: «{title}»\nПоставьте оценку от 1 до 5:', reply_markup=kb.rating_kb)

    elif state == "waiting_rating":
        if text not in {"1", "2", "3", "4", "5"}:
            await message.answer("Поставьте оценку от 1 до 5:", reply_markup=kb.rating_kb)
            return
        data["ratings"][data["pending"]] = int(text)
        data["pending"] = None
        data["state"] = "waiting_action"
        await message.answer(
            f"Оценка {text} сохранена! Оценено фильмов: {len(data['ratings'])}.\nЧто дальше?",
            reply_markup=kb.action_kb,
        )

    elif state == "waiting_action":
        if text == "Ещё фильм":
            data["state"] = "waiting_movie"
            await message.answer("Введите название следующего фильма:")
        elif text == "Получить рекомендации":
            data["state"] = "waiting_rec_count"
            await message.answer("Сколько рекомендаций показать?", reply_markup=kb.rec_count)
        else:
            await message.answer("Выберите действие:", reply_markup=kb.action_kb)

    elif state == "waiting_rec_count":
        if text not in {"5", "10", "15"}:
            await message.answer("Выберите количество:", reply_markup=kb.rec_count)
            return
        n = int(text)
        await message.answer("Вычисляю рекомендации, подождите...")
        recs = recommend_new(data["ratings"], matrix, sim_matrix, item_names, n=n)
        if not recs:
            await message.answer("Не удалось сформировать рекомендации.")
            data["state"] = "waiting_action"
            return
        result = f"Топ-{n} рекомендованных фильмов:\n\n"
        for i, (title, score) in enumerate(recs, start=1):
            result += f"{i}. {title} — {score:.2f}\n"
        await message.answer(result)
        data["state"] = "waiting_action"
        await message.answer("Хотите ещё?", reply_markup=kb.action_kb)
