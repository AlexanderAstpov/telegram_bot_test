from aiogram import types




BTN_FEED = "🌯 Покормить"
BTN_PLAY = "🥎 Поиграть"
BTN_SLEEP = "💤 Спать"
BNT_STATUS = "📊 Статус"
BTN_EXIT = "⭕ Выход"

main_kb = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text=BTN_FEED), types.KeyboardButton(text=BTN_PLAY)],
        [types.KeyboardButton(text=BTN_SLEEP), types.KeyboardButton(text=BNT_STATUS)],
        [types.KeyboardButton(text=BTN_EXIT)]
    ],
    resize_keyboard=True
    
)

remove_kb = types.ReplyKeyboardRemove() # метод отвечающий за удаление клавиатуры

food_kb = types.InlineKeyboardMarkup(
    inline_keyboard= [
        [
            types.InlineKeyboardButton(text="🥩 Стейк", callback_data="steak"), 
            types.InlineKeyboardButton(text="🍤 Креветки", callback_data="prawns")
        ],
        [types.InlineKeyboardButton(text="🥃 Виски", callback_data="Wisky")]
    ]
)
