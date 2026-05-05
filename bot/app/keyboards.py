from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

rating_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=str(i)) for i in range(1, 6)]],
    resize_keyboard=True,
)

action_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Ещё фильм"), KeyboardButton(text="Получить рекомендации")]],
    resize_keyboard=True,
)

rec_count = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="5"), KeyboardButton(text="10"), KeyboardButton(text="15")]],
    resize_keyboard=True,
)
