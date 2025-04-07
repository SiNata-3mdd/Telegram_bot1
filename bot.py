
import telebot
from telebot import types
import requests

# Токен твоего бота
TOKEN = '7353039668:AAFA0ioznY6-iNdH7R70d9m0SFS4iVw8SHw'
CHANNEL_USERNAME = '@NATALYA_PRO_TG'

bot = telebot.TeleBot(TOKEN)

# Проверка подписки
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"Получено сообщение от {message.from_user.id} - {message.from_user.first_name}")
    if is_subscribed(message.from_user.id):
        send_guide(message)
    else:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("🔔 Подписаться на канал", url=f'https://t.me/{CHANNEL_USERNAME.strip("@")}')
        check_btn = types.InlineKeyboardButton("✅ Я подписался", callback_data='check_sub')
        markup.add(btn)
        markup.add(check_btn)
        bot.send_message(message.chat.id, "Привет! Чтобы получить гайд, подпишись на мой канал и нажми кнопку ниже 👇", reply_markup=markup)

# Обработка кнопки "Я подписался"
@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
def check_subscription(call):
    if is_subscribed(call.from_user.id):
        send_guide(call.message)
    else:
        bot.answer_callback_query(call.id, "❗ Ты ещё не подписался на канал.", show_alert=True)

# Отправка PDF-файла
def send_guide(message):
    with open('guide_gift.pdf', 'rb') as file:
        bot.send_document(message.chat.id, file, caption="🎁 Лови обещанный гайд!\n\nЕсли хочешь индивидуальный разбор контента — пиши в личку 💌")

# Запуск бота
bot.polling(none_stop=True)
