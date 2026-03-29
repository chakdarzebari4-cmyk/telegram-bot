import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ================= الإعدادات =================
API_TOKEN = "8628506847:AAHx55gFF83Xe3yGfYtDyl-ukET2Gb6AxXI"
ADMIN_ID = 2011675494  # تم إضافة الأيدي الخاص بك هنا
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
        InlineKeyboardButton("🛡️ الحماية {1}", callback_data="1"),
        InlineKeyboardButton("⚙️ التفعيل {2}", callback_data="2"),
        InlineKeyboardButton("🧹 المسح {3}", callback_data="3"),
        InlineKeyboardButton("⬆️ الرفع {4}", callback_data="4"),
        InlineKeyboardButton("👑 المالكين {5}", callback_data="5"),
        InlineKeyboardButton("👥 الأعضاء {6}", callback_data="6"),
        InlineKeyboardButton("👨‍💻 أوامر المطور", callback_data="dev"),
        InlineKeyboardButton("🎮 الألعاب", callback_data="games"),
        InlineKeyboardButton("🏦 البنك", callback_data="bank"),
        InlineKeyboardButton("🔘 التفعيل / التعطيل", callback_data="onoff"),
    ]
    kb.add(*buttons)
    return kb

# ================= /start =================
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # المطور (أنت) يتخطى فحص الاشتراك
    if message.from_user.id != ADMIN_ID:
        if not await check_sub(message.from_user.id):
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("اشترك بالقناة أولاً", url=f"https://t.me/{CHANNEL.replace('@', '')}"))
            await message.reply(f"❌ عذراً عزيزي، يجب عليك الاشتراك في قناة البوت {CHANNEL} أولاً.", reply_markup=kb)
            return

    text = "⭐️ **أهلاً بك في لوحة تحكم البوت** ⭐️\n\nاستخدم الأزرار أدناه للتحكم:"
    await message.reply(text, reply_markup=main_menu())

# ================= معالجة الأزرار =================
@dp.callback_query_handler(lambda c: True)
async def buttons(call: types.CallbackQuery):
    if call.data == "1":
        await call.message.edit_text("🛡️ **أوامر الحماية:**\n- منع الروابط (تلقائي)\n- مكافحة السبام")
    elif call.data == "dev":
        if call.from_user.id == ADMIN_ID:
            await call.message.edit_text("👨‍💻 **أهلاً مطورنا صقر:**\n/ban - حظر\n/unban - فك حظر\n/stats - الإحصائيات")
        else:
            await call.answer("❌ هذا القسم للمطور فقط!", show_alert=True)
    else:
        await call.message.edit_text("⚠️ هذا القسم قيد التطوير.")

# ================= حماية الروابط =================
@dp.message_handler(content_types=['text'])
async def protect(message: types.Message):
    if message.from_user.id != ADMIN_ID and "http" in message.text:
        try:
            await message.delete()
            await message.answer(f"⚠️ {message.from_user.first_name}، الروابط ممنوعة!")
        except:
            pass

# ================= تشغيل =================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
