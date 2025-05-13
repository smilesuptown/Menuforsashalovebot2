from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

cart = {}

menu = {
    "Омлет": {"image": "https://i.imgur.com/V4jIu5g.jpg", "price": "2 объятия"},
    "Кофе": {"image": "https://i.imgur.com/ypz8cT2.jpg", "price": "1 поцелуй"},
    "Паста": {"image": "https://i.imgur.com/x1WyDCV.jpg", "price": "3 объятия"},
    "Тосты": {"image": "https://i.imgur.com/3yNfD9j.jpg", "price": "1 объятие"},
    "Чай": {"image": "https://i.imgur.com/x3uKMze.jpg", "price": "1 поцелуй"},
    "Стейк": {"image": "https://i.imgur.com/EEMjTI3.jpg", "price": "4 объятия"},
    "Буррито": {"image": "https://i.imgur.com/sbhD9Ab.jpg", "price": "3 поцелуя"},
    "Шаурма": {"image": "https://i.imgur.com/5YQKboK.jpg", "price": "2 поцелуя"},
    "Тако": {"image": "https://i.imgur.com/1iSG77E.jpg", "price": "2 объятия"},
}

@dp.message_handler(commands=['start', 'menu'])
async def show_menu(message: types.Message):
    for item, data in menu.items():
        photo = data["image"]
        price = data["price"]
        keyboard = InlineKeyboardMarkup().add(
            InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add:{item}")
        )
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f"{item} — {price}",
            reply_markup=keyboard
        )

@dp.callback_query_handler(lambda c: c.data.startswith("add:"))
async def add_to_cart(callback_query: types.CallbackQuery):
    item = callback_query.data.split(":")[1]
    user_id = callback_query.from_user.id
    cart.setdefault(user_id, [])
    cart[user_id].append(item)
    await callback_query.answer(f"{item} добавлено в корзину!")

@dp.message_handler(commands=['cart'])
async def show_cart(message: types.Message):
    user_id = message.from_user.id
    items = cart.get(user_id, [])
    if not items:
        await message.reply("Ваша корзина пуста.")
    else:
        text = "Ваша корзина:
"
        summary = {}
        for item in items:
            summary[item] = summary.get(item, 0) + 1
        for name, count in summary.items():
            text += f"• {name} x{count}
"
        await message.reply(text)

if __name__ == '__main__':
    executor.start_polling(dp)
