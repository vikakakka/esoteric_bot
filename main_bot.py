import telebot
import os
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

CHANNEL_ID = -1003369934081

def get_all_cards():
    folder = "images/"
    cards = []
    for file in os.listdir(folder):
        if file.endswith((".jpg", ".png", ".jpeg")):
            cards.append(file)
    return cards

def get_random_card():
    card_number = random.randint(0, 69)
    return f"card_{card_number}.jpg"

def send_card (chat_id, card_name, reply_to_message):
    try:
        with open(f"images/{card_name}", "rb") as photo:
            bot.send_photo(chat_id, photo, reply_to_message_id = reply_to_message)
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка, не удалось отправить картинку!")

@bot.message_handler(func = lambda message: True)
def handle_message(message):

    if message.chat.id != CHANNEL_ID:
        return
    if not message.reply_to_message:
        return
    allowed_words = ["карта", "таро", "карту"]
    if message.text.lower().strip() in allowed_words:
        card = get_random_card()
        if card:
            send_card(message.chat.id, card, message.message_id)
        else:
            bot.send_message(message.chat.id, "Нет карт в библиотеке")


print("Эзотерический бот запущен!")
print("Жду комментарий со словом карта в канале")

bot.infinity_polling()
