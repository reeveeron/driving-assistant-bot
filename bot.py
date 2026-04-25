import telebot

TOKEN = "8723403092:AAHt83qBCk7WavqZ4z7QaIX5Y9CKDksJsdA"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"البوت يعمل بنجاح 🚖")

bot.infinity_polling()
