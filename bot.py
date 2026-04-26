import telebot

TOKEN = "8723403092:AAHt83qBCk7WavqZ4z7QaIX5Y9CKDksJsdA"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def get_group_id(message):
    print("اسم القروب:", message.chat.title)
    print("ID:", message.chat.id)
    print("----------------")

bot.infinity_polling()
