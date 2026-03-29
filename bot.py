import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ================= الإعدادات =================
API_TOKEN = "8628506847:AAHx55gFF83Xe3yGfYtDyl-ukET2Gb6AxXI"
ADMIN_ID = 2011675494  # أيدي صقر
CHANNEL_ID = "@ybpi1"  # قناة الاشتراك الإجباري
MY_USERNAME = "@Saqar_67" # يوزرك للتواصل

AUTHORIZED_GROUPS = [] # أضف الأيدي هنا أو عبر /add في الخاص

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ================= فحص الاشتراك وفحص الإشراف =================
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except: return False

async def is_admin(message: types.Message):
    # المطور دائماً يعتبر مسؤول
    if message.from_user.id == ADMIN_ID: return True
    # فحص إذا كان المستخدم مسؤول في المجموعة
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ["administrator", "creator"]

# ================= لوحة الأزرار =================
def full_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🛡️ الحماية {1}", callback_data="1"),
        InlineKeyboardButton("⚙️ التفعيل {2}", callback_data="2"),
        InlineKeyboardButton("🧹 المسح {3}", callback_data="3"),
        InlineKeyboardButton("⬆️ الرفع {4}", callback_data="4"),
        InlineKeyboardButton("👑 المالكين {5}", callback_data="5"),
        InlineKeyboardButton("👥 الأعضاء {6}", callback_data="6"),
        InlineKeyboardButton("👨‍💻 أوامر المطور", callback_data="dev"),
        InlineKeyboardButton("🎮 الألعاب", callback_data="games"),
        InlineKeyboardButton("🏦 البنك", callback_data="bank"),
        InlineKeyboardButton("🔘 التفعيل / التعطيل", callback_data="onoff")
    )
    return kb

# ================= الأوامر العامة =================
@dp.message_handler(commands=['start', 'menu', 'settings'])
async def show_menu(message: types.Message):
    # 1. فحص الاشتراك الإجباري
    if not await check_sub(message.from_user.id) and message.from_user.id != ADMIN_ID:
        kb_sub = InlineKeyboardMarkup().add(InlineKeyboardButton("اشترك هنا 📢", url=f"https://t.me/{CHANNEL_ID[1:]}"))
        return await message.reply(f"❌ اشترك في {CHANNEL_ID} أولاً لتفعيل الأوامر.", reply_markup=kb_sub)

    # 2. إذا كان في مجموعة، يجب أن يكون مشرفاً
    if message.chat.type in ['group', 'supergroup']:
        if not await is_admin(message):
            return await message.reply("⚠️ عذراً، هذه الأوامر مخصصة للمشرفين فقط داخل المجموعة.")
    
    await message.reply("⭐️ **لوحة تحكم حارس المجموعة**\nتحكم في إعدادات المجموعة من الأزرار أدناه:", reply_markup=full_menu())

# ================= حماية المجموعات (الاشتراك المدفوع) =================
@dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.NEW_CHAT_MEMBERS])
async def group_filter(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        # مغادرة المجموعات غير المفعلة
        if message.chat.id not in AUTHORIZED_GROUPS and message.from_user.id != ADMIN_ID:
            await message.answer(f"⚠️ البوت غير مفعل في هذه المجموعة. للتفعيل تواصل مع المطور: {MY_USERNAME}")
            return await bot.leave_chat(message.chat.id)

    # منع الروابط لغير المشرفين والمطور
    if message.text and "http" in message.text:
        if not await is_admin(message):
            try: await message.delete()
            except: pass

# ================= أوامر المطور في الخاص =================
@dp.message_handler(commands=['add'], chat_type=types.ChatType.PRIVATE)
async def add_group(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        try:
            gid = int(message.text.split()[1])
            AUTHORIZED_GROUPS.append(gid)
            await message.reply(f"✅ تم تفعيل المجموعة: `{gid}`", parse_mode="Markdown")
        except: await message.reply("أرسل: /add أيدي_المجموعة")

@dp.message_handler(commands=['id'])
async def get_id(message: types.Message):
    await message.reply(f"🆔 أيدي الدردشة: `{message.chat.id}`", parse_mode="Markdown")

# ================= تفاعل الأزرار =================
@dp.callback_query_handler(lambda c: True)
async def callback_handler(call: types.CallbackQuery):
    # فحص إذا كان المستخدم مشرفاً عند الضغط على الزر داخل المجموعة
    if call.message.chat.type in ['group', 'supergroup']:
        member = await bot.get_chat_member(call.message.chat.id, call.from_user.id)
        if member.status not in ["administrator", "creator"] and call.from_user.id != ADMIN_ID:
            return await call.answer("❌ أنت لست مشرفاً للتحكم في الإعدادات!", show_alert=True)

    if call.data == "1":
        await call.message.edit_text("🛡️ **قسم الحماية:** تم تفعيل منع الروابط والسبام للمشرفين.")
    elif call.data == "dev":
        await call.answer(f"المطور: {MY_USERNAME}", show_alert=True)
    else:
        await call.answer("⚙️ جاري العمل على هذا القسم..", show_alert=True)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
