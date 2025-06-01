
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

lang_buttons = InlineKeyboardMarkup(row_width=2)
lang_buttons.add(
    InlineKeyboardButton("فارسی 🇮🇷", callback_data="lang_fa"),
    InlineKeyboardButton("English 🇺🇸", callback_data="lang_en")
)

def start_buttons(lang="fa"):
    kb = InlineKeyboardMarkup(row_width=1)
    if lang == "fa":
        kb.add(
            InlineKeyboardButton("📥 دانلود از یوتیوب", callback_data="yt"),
            InlineKeyboardButton("📸 دانلود از اینستاگرام", callback_data="ig")
        )
    else:
        kb.add(
            InlineKeyboardButton("📥 Download from YouTube", callback_data="yt"),
            InlineKeyboardButton("📸 Download from Instagram", callback_data="ig")
        )
    return kb

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("🌐 لطفاً زبان خود را انتخاب کنید:
Please select your language:", reply_markup=lang_buttons)

@dp.callback_query_handler(lambda c: c.data in ["lang_fa", "lang_en"])
async def lang_selected(callback_query: types.CallbackQuery):
    lang = "fa" if callback_query.data == "lang_fa" else "en"
    text = "✅ زبان انتخاب شد.
یکی از گزینه‌ها را انتخاب کنید:" if lang == "fa" else "✅ Language set.
Please choose an option:"
    await bot.send_message(callback_query.from_user.id, text, reply_markup=start_buttons(lang))

@dp.callback_query_handler(lambda c: c.data in ["yt", "ig"])
async def handle_download(callback_query: types.CallbackQuery):
    if callback_query.data == "yt":
        await bot.send_message(callback_query.from_user.id, "🎬 لطفاً لینک ویدیوی یوتیوب را ارسال کنید:")
    else:
        await bot.send_message(callback_query.from_user.id, "📸 لطفاً لینک پست اینستاگرام را ارسال کنید:")

@dp.message_handler()
async def handle_links(message: types.Message):
    if "instagram.com" in message.text:
        await message.reply("✅ لینک اینستاگرام دریافت شد. پردازش آغاز شد...")
        # کد دانلود اینستاگرام در اینجا قرار می‌گیرد
    elif "youtube.com" in message.text or "youtu.be" in message.text:
        await message.reply("✅ لینک یوتیوب دریافت شد. پردازش آغاز شد...")
        # کد دانلود یوتیوب در اینجا قرار می‌گیرد
    else:
        await message.reply("❗ لطفاً یک لینک معتبر از یوتیوب یا اینستاگرام ارسال کنید.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
