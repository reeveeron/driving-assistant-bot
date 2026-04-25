import telebot
from telebot import types

TOKEN = "8723403092:AAHt83qBCk7WavqZ4z7QaIX5Y9CKDksJsdA"

bot = telebot.TeleBot(TOKEN)

# ضع آيدي حسابك من تيليجرام كمدير
ADMIN_ID = 8130404835

# قواعد بيانات بسيطة داخل الذاكرة (لاحقًا ننقلها لقاعدة بيانات)
clients = {}
drivers = {}
subscriptions = {}


# ======================
# القائمة الرئيسية
# ======================

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    b1 = types.KeyboardButton("🚖 تسجيل مشوار")
    b2 = types.KeyboardButton("📋 بيانات مشواري")
    b3 = types.KeyboardButton("💳 اشتراك شهري")
    b4 = types.KeyboardButton("🚗 طلب سائق")
    b5 = types.KeyboardButton("☎ الدعم")

    markup.add(b1,b2)
    markup.add(b3,b4)
    markup.add(b5)

    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "أهلًا بك في Driving Assistant Bot\nاختر من القائمة:",
        reply_markup=main_menu()
    )


# ======================
# تسجيل مشوار عميل
# ======================

@bot.message_handler(func=lambda m: m.text=="🚖 تسجيل مشوار")
def register_trip(message):
    msg = bot.send_message(
        message.chat.id,
        "أرسل اسمك:"
    )
    bot.register_next_step_handler(msg, ask_home)


def ask_home(message):
    user_id=message.chat.id

    if user_id not in clients:
        clients[user_id]={}

    clients[user_id]["name"]=message.text

    msg=bot.send_message(
        user_id,
        "أرسل موقع المنزل:"
    )
    bot.register_next_step_handler(msg,ask_work)


def ask_work(message):
    user_id=message.chat.id
    clients[user_id]["home"]=message.text

    msg=bot.send_message(
        user_id,
        "أرسل موقع الدوام:"
    )
    bot.register_next_step_handler(msg,save_trip)


def save_trip(message):
    user_id=message.chat.id
    clients[user_id]["work"]=message.text

    bot.send_message(
        user_id,
        "تم تسجيل المشوار بنجاح ✅"
    )

    notify_admin_new_client(user_id)


# ======================
# عرض بيانات العميل
# ======================

@bot.message_handler(func=lambda m: m.text=="📋 بيانات مشواري")
def my_trip(message):
    uid=message.chat.id

    if uid not in clients:
        bot.send_message(uid,"لا يوجد تسجيل بعد.")
        return

    data=clients[uid]

    text=f"""
👤 الاسم: {data['name']}
🏠 المنزل: {data['home']}
🏢 الدوام: {data['work']}
"""

    if uid in subscriptions:
        text += "\n💳 الاشتراك: نشط"

    bot.send_message(uid,text)


# ======================
# اشتراك شهري
# ======================

@bot.message_handler(func=lambda m: m.text=="💳 اشتراك شهري")
def subscription(message):
    uid=message.chat.id

    subscriptions[uid]={
        "plan":"شهري",
        "status":"pending"
    }

    bot.send_message(
        uid,
        "تم إرسال طلب اشتراك شهري.\nسيتم التواصل معك للدفع."
    )

    bot.send_message(
        ADMIN_ID,
        f"طلب اشتراك جديد من {uid}"
    )


# ======================
# طلب سائق
# ======================

@bot.message_handler(func=lambda m: m.text=="🚗 طلب سائق")
def request_driver(message):

    if not drivers:
        bot.send_message(
            message.chat.id,
            "لا يوجد سائق متاح حاليًا."
        )
        return

    first_driver=list(drivers.keys())[0]

    bot.send_message(
        message.chat.id,
        f"تم تعيين السائق: {drivers[first_driver]}"
    )


# ======================
# الدعم
# ======================

@bot.message_handler(func=lambda m: m.text=="☎ الدعم")
def support(message):
    bot.send_message(
        message.chat.id,
        "للدعم تواصل مع الإدارة."
    )


# ======================
# أوامر الإدارة
# ======================

@bot.message_handler(commands=['add_driver'])
def add_driver(message):

    if message.chat.id != ADMIN_ID:
        return

    msg=bot.reply_to(
        message,
        "أرسل اسم السائق:"
    )

    bot.register_next_step_handler(msg,save_driver)


def save_driver(message):
    drivers[len(drivers)+1]=message.text

    bot.send_message(
        message.chat.id,
        "تمت إضافة السائق بنجاح ✅"
    )


@bot.message_handler(commands=['clients'])
def show_clients(message):

    if message.chat.id != ADMIN_ID:
        return

    if not clients:
        bot.send_message(
            message.chat.id,
            "لا يوجد عملاء"
        )
        return

    text="قائمة العملاء:\n\n"

    for c in clients.values():
        text += f"{c['name']} | {c['home']} -> {c['work']}\n"

    bot.send_message(
        message.chat.id,
        text
    )


def notify_admin_new_client(uid):

    data=clients[uid]

    txt=f"""
عميل جديد:

{data['name']}
{data['home']}
إلى
{data['work']}
"""

    bot.send_message(
        ADMIN_ID,
        txt
    )


# ======================
# رسائل غير مفهومة
# ======================

@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "اختر من القائمة أو اكتب /start"
    )


print("Driving Assistant Bot Running...")
bot.infinity_polling()
