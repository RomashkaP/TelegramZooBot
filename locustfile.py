from locust import HttpUser, task, between
import random
import time

# Имитационные данные
MESSAGES = [
    "/start",
    "/help",
    "/contacts",
    "/social",
    "/feedback",
    "Когда следующая викторина?",
    "Хочу узнать больше о жирафах",
    "Как мне попасть в зоопарк?",
]


class TelegramBotUser(HttpUser):
    host = ""  # Обязательно для Locust
    wait_time = between(0.5, 2)  # Пауза между действиями

    def on_start(self):
        """Имитируем начало сессии пользователя"""
        self.chat_id = random.randint(100000000, 999999999)
        self.message_id = 1
        self.user_data = {}  # Имитируем user_data для каждого пользователя
        print(f"[{self.chat_id}] Пользователь начал сессию")

    @task(3)  # Чаще выполняется
    def simulate_message_handling(self):
        """Имитируем обработку входящего сообщения"""
        message = random.choice(MESSAGES)
        print(f"[{self.chat_id}] Получено сообщение: {message}")

        # Имитируем время обработки
        time.sleep(random.uniform(0.01, 0.1))

        # Имитируем логику бота
        if message == "/start":
            self.handle_start()
        elif message == "/help":
            self.handle_help()
        elif "викторин" in message.lower():
            self.handle_quiz()
        elif "отзыв" in message.lower():
            self.handle_feedback()
        else:
            self.handle_default()

    @task(1)  # Реже выполняется
    def simulate_callback_handling(self):
        """Имитируем обработку callback-кнопки"""
        callback_data = random.choice([
            "start_quiz",
        ])
        print(f"[{self.chat_id}] Нажата кнопка: {callback_data}")

        # Имитируем время обработки
        time.sleep(random.uniform(0.01, 0.1))

        # Имитируем логику
        if callback_data == "start_quiz":
            self.start_quiz_logic()
        elif callback_data == "show_result":
            self.show_result_logic()

    def handle_start(self):
        self.user_data[self.chat_id] = {
            'name': f"User_{self.chat_id}",
            'score': 0,
            'answers': []
        }
        print(f"[{self.chat_id}] Обработан /start")

    def handle_help(self):
        print(f"[{self.chat_id}] Обработан /help")

    def handle_quiz(self):
        print(f"[{self.chat_id}] Начата викторина")

    def handle_feedback(self):
        print(f"[{self.chat_id}] Запрошен отзыв")

    def handle_default(self):
        print(f"[{self.chat_id}] Обработано стандартное сообщение")

    def start_quiz_logic(self):
        print(f"[{self.chat_id}] Логика начала викторины")

    def show_result_logic(self):
        print(f"[{self.chat_id}] Логика показа результата")

    def on_stop(self):
        """Выполняется при завершении сессии"""
        print(f"[{self.chat_id}] Пользователь завершил сессию")