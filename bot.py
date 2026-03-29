import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# ================= الإعدادات =================
API_TOKEN = "8628506847:AAHx55gFF83Xe3yGfYtDyl-ukET2Gb6AxXI"
ADMIN_ID = 2011675494  # أيديك ياصقر
CHANNEL_ID = "@ybpi1"  # يوزر قناتك
MY_USERNAME = "@Saqar_67"

# قائمة المجموعات المفعلة (النظام المدفوع)
AUTHORIZED_GROUPS = [] 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ================= فحص الاشتراك وفحص الإشراف =================
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except: return False

async def is_admin(chat_id, user_id):
    if user_id == ADMIN_ID: return True
    member = await bot.get_chat_member(chat_id, user_id)
    return member.status in ["administrator", "creator"]

# ================= لوحة الأزرار الكاملة =================
def full_menu():
    kb = InlineKeyboardMarkup(row_width=2)
    # أزرار الوظائف
    buttons = [
        InlineKeyboardButton("🛡️ الحماية {1}", callback_data="1"),
        InlineKeyboardButton("⚙️ التفعيل {2}", callback_data="2"),
        InlineKeyboardButton("🧹 المسح {3}", callback_data="3"),
        InlineKeyboardButton("⬆️ الرفع {4}", callback_data="4"),
        InlineKeyboardButton("👑 المالكين {5}", callback_data="5"),
        InlineKeyboardButton("👥 الأعضاء {6}", callback_data="6"),
        InlineKeyboardButton("🎮 الألعاب", callback_data="games"),
        InlineKeyboardButton("🏦 البنك", callback_data="bank"),
        InlineKeyboardButton("🔘 التفعيل / التعطيل", callback_data="onoff")
    ]
    kb.add(*buttons)
    # زر القناة وزر المطور بشكل عريض في الأسفل
    kb.row(InlineKeyboardButton("📢 قناة البوت (اشترك هنا)", url=f"https://t.me/{CHANNEL_ID[1:]}"))
    kb.row(InlineKeyboardButton("👨‍💻 أوامر المطور", callback_data="dev"))
    return kb

# ================= نظام الرقابة الصارم داخل المجموعات =================
@dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.NEW_CHAT_MEMBERS])
async def global_protector(message: types.Message):
    if message.chat.type in ['group', 'supergroup']:
        # 1. فحص الاشتراك المدفوع للمجموعة
        if message.chat.id not in AUTHORIZED_GROUPS and message.from_user.id != ADMIN_ID:
            await message.answer(f"⚠️ البوت غير مفعل هنا. للتفعيل تواصل مع المطور: {MY_USERNAME}")
            return await bot.leave_chat(message.chat.id)

        # 2. فحص الاشتراك الإجباري (حذف رسائل غير المشتركين في المجموعة)
        if message.from_user.id != ADMIN_ID:
            if not await check_sub(message.from_user.id):
                try:
                    await message.delete() # حذف رسالة غير المشترك فوراً
                    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("اضغط هنا للاشتراك 📢", url=f"https://t.me/{CHANNEL_ID[1:]}"))
                    await message.answer(f"⚠️ عذراً {message.from_user.first_name}، يمنع إرسال الرسائل قبل الاشتراك في قناة البوت: {CHANNEL_ID}", reply_markup=kb)
                    return
                except: pass

    # 3. منع الروابط لغير المشرفين
    if message.text and "http" in message.text:
        if not await is_admin(message.chat.id, message.from_user.id):
            try: await message.delete()
            except: pass

# ================= أوامر البوت =================
@dp.message_handler(commands=['start', 'menu'])
async def start_cmd(message: types.Message):
    # فحص الاشتراك للمستخدمين في الخاص قبل إظهار الأزرار
    if message.from_user.id != ADMIN_ID:
        if not await check_sub(message.from_user.id):
            kb = InlineKeyboardMarkup().add(InlineKeyboardButton("اشترك في القناة لتفعيل البوت 📢", url=f"https://t.me/{CHANNEL_ID[1:]}"))
            return await message.reply(f"❌ يجب الاشتراك في القناة أولاً لتتمكن من استخدام البوت: {CHANNEL_ID}", reply_markup=kb)

    await message.reply("⭐️ **لوحة تحكم حارس المجموعة**\nاستخدم الأزرار أدناه للتحكم في المجموعة:", reply_markup=full_menu())

@dp.message_handler(commands=['add'], chat_type=types.ChatType.PRIVATE)
async def add_group(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        try:
            gid = int(message.text.split()[1])
            AUTHORIZED_GROUPS.append(gid)
            await message.reply(f"✅ تم تفعيل المجموعة بنجاح: `{gid}`")
        except: await message.reply("أرسل: /add أيدي_المجموعة")

@dp.message_handler(commands=['id'])
async def get_id(message: types.Message):
    await message.reply(f"🆔 أيدي هذه الدردشة: `{message.chat.id}`")

# ================= معالجة الأزرار للمشرفين فقط =================
@dp.callback_query_handler(lambda c: True)
async def callback_worker(call: types.CallbackQuery):
    # التأكد أن المستخدم مشرف قبل الضغط (إذا كان في مجموعة)
    if call.message.chat.type in ['group', 'supergroup']:
        if not await is_admin(call.message.chat.id, call.from_user.id):
            return await call.answer("❌ هذا التحكم للمشرفين فقط!", show_alert=True)

    if call.data == "dev":
        if call.from_user.id == ADMIN_ID:
            await call.message.edit_text(f"👨‍💻 أهلاً مطورنا صقر\n\n- لتفعيل مجموعة: `/add [ID]`\n- لمعرفة أيدي مجموعة: `/id`", parse_mode="Markdown")
        else:
            await call.answer(f"المطور هو صقر: {MY_USERNAME}", show_alert=True)
    else:
        await call.answer("⚙️ القسم قيد التطوير ياصقر.", show_alert=True)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
