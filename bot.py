import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ================= الإعدادات الأساسية =================
API_TOKEN = "8628506847:AAHx55gFF83Xe3yGfYtDyl-ukET2Gb6AxXI"
ADMIN_ID = 2011675494  # أيدي صقر (للتحكم)
MY_USERNAME = "@Saqar_67"  # <--- حط يوزرك هنا (بدون @ إذا أردت)
CHANNEL = "@ybpi1"

# قائمة المجموعات المفعلة (اشتراك مدفوع)
AUTHORIZED_GROUPS = [] 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ================= فحص الاشتراك =================
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except: return False

# ================= أمر إضافة مجموعة (للمطور فقط) =================
@dp.message_handler(commands=['add'])
async def add_group(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        try:
            gid = int(message.text.split()[1])
            AUTHORIZED_GROUPS.append(gid)
            await message.reply(f"✅ تم تفعيل المجموعة: {gid}")
        except:
            await message.reply("❌ أرسل: /add ثم أيدي المجموعة")

# ================= أمر /id (لمعرفة أيدي المجموعة) =================
@dp.message_handler(commands=['id'])
async def get_id(message: types.Message):
    await message.reply(f"🆔 أيدي الدردشة: `{message.chat.id}`\n👤 أيديك: `{message.from_user.id}`", parse_mode="Markdown")

# ================= أمر /start =================
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        if not await check_sub(message.from_user.id):
            kb = InlineKeyboardMarkup().add(InlineKeyboardButton("اشترك هنا", url=f"https://t.me/{CHANNEL[1:]}"))
            await message.reply(f"❌ اشترك في {CHANNEL} أولاً.", reply_markup=kb)
            return

    text = f"⭐️ **أهلاً بك في بوت حارس المجموعة**\n\nللاشتراك وتفعيل البوت لمجموعتك، تواصل مع المطور: {MY_USERNAME}"
    
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🛡️ الحماية", callback_data="1"),
        InlineKeyboardButton("👨‍💻 المطور", url=f"https://t.me/{MY_USERNAME.replace('@','')}")
    )
    await message.reply(text, reply_markup=kb)

# ================= حماية المجموعات (النظام المدفوع) =================
@dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.NEW_CHAT_MEMBERS])
async def group_guard(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        # إذا كانت المجموعة غير مفعلة والمستخدم ليس المطور
        if message.chat.id not in AUTHORIZED_GROUPS and message.from_user.id != ADMIN_ID:
            await message.answer(f"⚠️ هذا البوت مدفوع. لتفعيله تواصل مع: {MY_USERNAME}")
            await bot.leave_chat(message.chat.id)
            return

    # منع الروابط لغير المطور
    if "http" in message.text and message.from_user.id != ADMIN_ID:
        try: await message.delete()
        except: pass

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
