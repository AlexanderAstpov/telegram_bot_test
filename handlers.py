from db import get_pet, update_pet, create_pet
from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from keyboards import (
    main_kb, 
    food_kb,
    # activity_kb,
    BNT_STATUS, 
    BTN_EXIT, 
    BTN_FEED, 
    BTN_PLAY, 
    BTN_SLEEP,
    BTN_FRIEND
    )



def progress_bar(value: int, length: int):
    filled = int(value/100 * 10)
    return "🟩" * filled + "⬛" * (length - filled)


async def register_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command("start"))
    dp.message.register(play_pet, F.text == BTN_PLAY)
    dp.message.register(feed_pet, F.text == BTN_FEED)
    dp.message.register(status_pet, F.text == BNT_STATUS)
    # dp.message.register(friend_pet, F.text == BTN_FRIEND)
    dp.callback_query.register(food_callback_handler, lambda c: c.data.startswith("feed_"))
   



async def start_handler(message: types.Message):
    user_id = message.from_user.id
    pet = await get_pet(user_id)
    
    if not pet:
        await create_pet(user_id, "Wisky 🥃")
        pet = await get_pet(user_id)

    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        f"Познакомься со своим питомцем: {pet['name']}!\n"
        f"Позаботься о нём!",
        reply_markup=main_kb
    )


# async def friend_pet(message: types.Message):
#     user_id = message.from_user.id
#     pet = await get_pet(user_id)
#     if not pet:
#         await message.answer("Сначала запусти бота с помощью команды /start")
#         return
#     pet["friendliness"] = min(pet["friendliness"] + 10, 100)
#     await update_pet(
#         user_id=user_id,
#         name=pet["name"],
#         hunger=pet["hunger"],
#         happiness=pet["happiness"],
#         energy=pet["energy"]   
#     )
#     await message.answer(f"{pet['name']} принес вам игрушку 🦴😀!")



async def play_pet(message: types.Message):
    user_id = message.from_user.id
    pet = await get_pet(user_id)
    if not pet:
        await message.answer("Сначала запусти бота с помощью команды /start")
        return
    pet["happiness"] = min(pet["happiness"] + 10, 100)
    pet["energy"] = max(pet["energy"] - 15, 0)

    await update_pet(
        user_id=user_id,
        name=pet["name"],
        hunger=pet["hunger"],
        happiness=pet["happiness"],
        energy=pet["energy"]
    )
    await message.answer(f"{pet['name']} весело поиграл!")


async def feed_pet(message: types.Message):
    user_id = message.from_user.id
    pet = await get_pet(user_id)
    if not pet:
        await message.answer("Сначала запусти бота с помощью команды /start")
        return
    
    await message.answer(
        f"Чем вы хотите покормить {pet['name']}?", 
        reply_markup=food_kb
        )
    

async def status_pet(message: types.Message):
    user_id = message.from_user.id
    pet = await get_pet(user_id)
    if  not pet:
        await message.answer("Сначала запусти бота с помощью команды /start")
        return

    hun = pet['hunger']
    en = pet['energy']
    hap = pet['happiness']
    # fre = pet['friendliness']
    
    status = (
        f"Статус вашего питомца {pet['name']}:\n"
        f"Сытость: {hun}% {progress_bar(hun, 10)}\n"
        f"Энергия: {en}% {progress_bar(en, 10)}\n"
        f"Счастье: {hap}% {progress_bar(hap, 10)}\n"
        # f"Дружелюбие: {fre}% {progress_bar(fre, 10)}\n"
    )
    await message.answer(status)


async def food_callback_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    pet = await get_pet(user_id)
    if not pet:
        await callback.message.edit_text("Сначала запусти бота с помощью команды /start")
        return
    food = callback.data
    message = ""
    h = pet["hunger"]

    if food == "feed_steak":
        h = pet["hunger"] + 20
        pet["energy"] = max(pet["energy"] + 15, 0)
        message = f"вы покормили {pet['name']} вкусным стейком"

    elif food == "feed_prawns":
        h = pet["hunger"] + 10
        message = f"вы покормили {pet['name']} вкусными креветками"

    elif food == "feed_Wisky":
        h = pet["hunger"] + 1
        message = f"вы напоили {pet['name']} 12-и летним Виски"

    pet["hunger"] = min(100, h)

    await update_pet(
        user_id=user_id,
        name=pet["name"],
        hunger=pet["hunger"],
        happiness=pet["happiness"],
        energy=pet["energy"]
    )

    await callback.message.edit_text(message)
    await callback.answer(
        f"Ссытость {pet['name']} -- {pet['hunger']}/100 \n"
        f"{progress_bar(pet['hunger'], 10)}"
        )

