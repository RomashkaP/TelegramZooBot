import telebot
from telebot import types
from config import animals_dict, advertising_text, bot_name

class QuizObject:
    def __init__(self):
        self.count_a = 0
        self.count_b = 0
        self.count_c = 0
        self.count_d = 0
        self.user_progress = 0

    def start_quiz_button(self):
        markup = types.InlineKeyboardMarkup()
        btn_quiz = types.InlineKeyboardButton('🐾 Начать викторину 🐾', callback_data='start_quiz')
        markup.add(btn_quiz)
        return markup

    def guardianship_button(self):
        markup = types.InlineKeyboardMarkup()
        link_button = types.InlineKeyboardButton('❤️Подружиться❤️', url= 'https://moscowzoo.ru/about/guardianship')
        markup.add(link_button)
        return markup

    def url_animal_button(self, url):
        markup = types.InlineKeyboardMarkup()
        link_button = types.InlineKeyboardButton('🔍Узнать больше🔍', url= url)
        markup.add(link_button)
        return markup

    def zeroing_counter(self):
        self.count_a = 0
        self.count_b = 0
        self.count_c = 0
        self.count_d = 0
        self.user_progress = 0

    def send_question(self, call, bot, quiz_questions):#chat_id
        chat_id = call.message.chat.id
        index = self.user_progress
        if index >= len(quiz_questions):
            animal = self.scoring_point()
            markup_guardianship = self.guardianship_button()
            markup_animal_url = self.url_animal_button(animals_dict[animal]['url'])
            image_url = animals_dict[animal]['image_url']
            discription = animals_dict[animal]['discription']
            restart_button = types.InlineKeyboardButton('Попробовать ещё раз.', callback_data='start_quiz')
            markup_animal_url.add(restart_button)
            username = call.from_user.username or 'Анонимный пользователь'
            bot.send_photo(chat_id, image_url, caption=f'По результату викторины, {username}, \
твой тотемный зверь: \n{discription} - {animal}.\n\nЭто сообщение сформировано цифровым работником \
Московского Зоопарка - пингвинёнком Зу🐧\n\nЗаходи ко мне, что бы узнать своего тотемного зверя https://t.me/{bot_name}.',
reply_markup=markup_animal_url)
            bot.send_message(chat_id, advertising_text, reply_markup=markup_guardianship)
            self.user_progress += 1
            return
        question_data = quiz_questions[index]
        markup = types.InlineKeyboardMarkup()
        for answer in question_data['answers']:
            markup.add(types.InlineKeyboardButton(f'{answer}', callback_data=f'{answer[0]}'))
        bot.send_message(chat_id, question_data['question'], reply_markup=markup)

    def hendle_quiz_answers_method(self, call, bot, quiz_questions):
        bot.answer_callback_query(call.id)
        if self.user_progress > 15:
            bot.send_message(call.message.chat.id, 'Ты уже прошёл викторину, пролистай выше.')
            return
        answer = call.data
        if answer == 'A':
            self.count_a += 1
        elif answer == 'B':
            self.count_b += 1
        elif answer == 'C':
            self.count_c += 1
        elif answer == 'D':
            self.count_d += 1
        self.user_progress += 1
        self.send_question(call, bot, quiz_questions)

    def scoring_point(self):
        scoring_list = [self.count_a, self.count_b, self.count_c, self.count_d]
        if max(scoring_list) == self.count_a and self.count_a == self.count_c:
            return 'Ирбис'
        elif max(scoring_list) == self.count_b and self.count_b == self.count_d:
            return 'Ленивец'
        elif max(scoring_list) == self.count_a and self.count_a == self.count_d:
            return 'Японский макак'
        elif max(scoring_list) == self.count_c and self.count_c == self.count_d:
            return 'Лемур'
        elif max(scoring_list) == self.count_b and self.count_b == self.count_c:
            return 'Папуанский пингвин'
        elif max(scoring_list) == self.count_a and self.count_a == self.count_b:
            return 'Медоед'
        elif max(scoring_list) == self.count_a:
            return 'Амурский тигр'
        elif max(scoring_list) == self.count_b:
            return 'Капибара'
        elif max(scoring_list) == self.count_c:
            return 'Енот полоскун'
        elif max(scoring_list) == self.count_d:
            return 'Филин'
        else:
            return 'Степной сурок'







