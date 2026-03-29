import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = "8628506847:AAHx55gFF83Xe3yGfYtDyl-ukET2Gb6AxXI"
ADMIN_ID = 000000000  # حط ايديك الرقمي
CHANNEL = "@ybpi1"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ================= تحقق الاشتراك =================
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# ================= واجهة الأزرار =================
def main_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(" {1} ", callback_data="1"),
        InlineKeyboardButton(" {2} ", callback_data="2"),
        InlineKeyboardButton(" {3} ", callback_data="3"),
        InlineKeyboardButton(" {4} ", callback_data="4"),
        InlineKeyboardButton(" {5} ", callback_data="5"),
        InlineKeyboardButton(" {6} ", callback_data="6"),
        InlineKeyboardButton(" أوامر المطور ", callback_data="dev"),
        InlineKeyboardButton(" الألعاب ", callback_data="games"),
        InlineKeyboardButton(" البنك ", callback_data="bank"),
        InlineKeyboardButton(" التفعيل / التعطيل ", callback_data="onoff"),
    ]
    kb.add(*buttons)
    return kb

# ================= /start =================
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not await check_sub(message.from_user.id):
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("اشترك بالقناة", url="https://t.me/ybpi1"))
        await message.reply("❌ لازم تشترك بالقناة أولاً", reply_markup=kb)
        return

    text = """
⭐️ أوامر البوت الرئيسية ⭐️

{1} الحماية
{2} التفعيل
{3} المسح
{4} الرفع
{5} المالكين
{6} الأعضاء
"""
    await message.reply(text, reply_markup=main_menu())

# ================= الأزرار =================
@dp.callback_query_handler(lambda c: True)
async def buttons(call: types.CallbackQuery):

    if call.data == "1":
        await call.message.edit_text("🛡️ أوامر الحماية:\n- منع روابط\n- مكافحة سبام")

    elif call.data == "2":
        await call.message.edit_text("⚙️ أوامر التفعيل:\n- تفعيل\n- تعطيل")

    elif call.data == "3":
        await call.message.edit_text("🧹 أوامر المسح")

    elif call.data == "4":
        await call.message.edit_text("⬆️ أوامر الرفع")

    elif call.data == "5":
        await call.message.edit_text("👑 أوامر المالكين")

    elif call.data == "6":
        await call.message.edit_text("👥 أوامر الأعضاء")

    elif call.data == "dev":
        if call.from_user.id == ADMIN_ID:
            await call.message.edit_text("👨‍💻 أوامر المطور:\n/ban\n/unban\n/stats")
        else:
            await call.answer("❌ هذا القسم للمطور فقط", show_alert=True)

    elif call.data == "games":
        await call.message.edit_text("🎮 قسم الألعاب قريباً")

    elif call.data == "bank":
        await call.message.edit_text("🏦 نظام البنك قريباً")

    elif call.data == "onoff":
        await call.message.edit_text("🔘 التحكم بالتفعيل والتعطيل")

# ================= حماية روابط =================
@dp.message_handler()
async def protect(message: types.Message):
    if "http" in message.text:
        await message.delete()
        await message.answer("🚫 يمنع نشر الروابط هنا")

# ================= تشغيل =================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
