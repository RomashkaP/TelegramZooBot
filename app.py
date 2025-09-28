import telebot
from telebot import types
from config import quiz_questions
from quiz_class import QuizObject
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
user_data = {}
user_feedback_state = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    user_data[message.chat.id] = QuizObject()
    markup = user_data[message.chat.id].start_quiz_button()
    bot.send_message(message.chat.id, 'Привет, меня зовут Зу!🐧 \n\
Я цифровой работник Московского Зоопарка.\nНажми 👉 /help \
и я расскажу тебе о своей задаче.')
    bot.send_message(message.chat.id, 'А если кто-то тебе уже рассказал \
что я делаю, то\nНажми 👉«Начать викторину»❄️', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'start_quiz')
def handle_start_quiz(call):
    bot.answer_callback_query(call.id)
    user_data[call.message.chat.id].zeroing_counter()
    user_data[call.message.chat.id].send_question(call, bot, quiz_questions)

@bot.callback_query_handler(func=lambda call: True)
def hendle_quiz_answers(call):
    chat_id = call.message.chat.id
    # if chat_id not in user_data:
    #     user_data[chat_id] = QuizObject()
    user_data[chat_id].hendle_quiz_answers_method(call, bot, quiz_questions)

@bot.message_handler(commands=['contacts'])
def show_contacts(message):
    markup = types.InlineKeyboardMarkup()
    contact_button = types.InlineKeyboardButton(text='📞 Контакты 📞', url='https://moscowzoo.ru/contacts')
    markup.add(contact_button)
    bot.send_message(message.chat.id, '🐧Нажмите на кнопки ниже, что бы перейти на страницу с контактами.',
reply_markup=markup)

@bot.message_handler(commands=['social'])
def show_social(message):
    markup = types.InlineKeyboardMarkup()
    ok_button = types.InlineKeyboardButton(text='🟠 Одноклассники', url='https://ok.ru/moscowzoo')
    tg_button = types.InlineKeyboardButton(text='🟢 Telegram', url='https://t.me/Moscowzoo_official')
    vk_button = types.InlineKeyboardButton(text='🔵 ВКонтакте', url='https://vk.com/moscow_zoo')
    youtube_button = types.InlineKeyboardButton(text='🔴 YouTube', url='https://www.youtube.com/@Moscowzooofficial')
    markup.add(ok_button)
    markup.add(tg_button)
    markup.add(vk_button)
    markup.add(youtube_button)
    bot.send_message(message.chat.id, '🐧Вот социальные сети нашего зоопарка:',
reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_message(message):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = QuizObject()

    markup = user_data[message.chat.id].start_quiz_button()
    bot.send_message(message.chat.id, f' Привет, меня зовут Зу!🐧\n\
Я — цифровой сотрудник Московского зоопарка , маленький пингвинёнок, который любит приключения \
и помогает находить друзей❄️🌟\n\
Моя задача — помочь тебе узнать, какое животное ближе тебе по духу. \
Пройди короткую викторину из 15 вопросов, и на основе твоих ответов я определю твоё тотемное животное. \n\
Каждый вопрос поможет мне понять твой характер, предпочтения и образ мышления.\n\
По окончании ты узнаешь, кем ты являешься в мире природы.\n\n\
Нажми 👉«Начать викторину», чтобы отправиться в увлекательное путешествие❄️', reply_markup= markup)

@bot.message_handler(commands=['feedback'])
def feedback_message(message):
    chat_id = message.chat.id
    user_feedback_state[chat_id] = True
    bot.send_message(chat_id, "Напишите ваш отзыв — мы ценим каждое слово! 🙏\n\n\
(Просто отправьте сообщение, а я его сохраню.)")

@bot.message_handler(func=lambda message: user_feedback_state.get(message.chat.id) is True)
def save_feedback(message):
    chat_id = message.chat.id
    feedback_text = message.text.strip()

    with open('feedback.txt', 'a', encoding='utf-8') as f:
        username = message.from_user.username or 'Аноним'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'[{timestamp}] @{username} ({chat_id}) : {feedback_text}\n' + '-' * 50 + '\n')

    del user_feedback_state[chat_id]
    bot.send_message(chat_id, '✅ Спасибо за ваш отзыв! Он очень важен для нас.')



@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, '🐧Меня пока не научили отвечать на такие сообщения.\n\n\
Вот список моих основных команд:\n1. /start - Начнём знакомство заново 🔄\n\
2. /help - Расскажу в чём моя задача 📋\n3. /contacts - Покажу контакты нашего зоопарка 📞\n\
4. /social - Покажу наши социальные сети 🌐\n\n❄️ Я всегда рядом, чтобы помочь тебе узнать больше!')


bot.infinity_polling()
