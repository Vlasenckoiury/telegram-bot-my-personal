import telebot
from telebot import types


# Создаем экземпляр бота
bot = telebot.TeleBot('TOKEN')


# Описываем действие при получении команды "/start"
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}, нажми на квадратик в правом нижнем углу(возле смайликов) чтобы выбрать команды!".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "👋 Поздороваться":
        bot.send_message(message.chat.id, text="Привет 👋, Это личный бот Юры Власенко!)")
    elif message.text == "❓ Задать вопрос":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        btn3 = types.KeyboardButton("Информация обо мне")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос!", reply_markup=markup)

    elif message.text == "Как меня зовут?":
        start(message)
        bot.send_message(message.chat.id, "Меня зовут Юра,давай знакомиться?")
        start_reg(message)

    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Могу по приветствовать и познакомиться, а также можешь узнать информацию обо мне 😉")

    elif message.text == "Информация обо мне":
        bot.send_message(message.chat.id, text="Меня зовут Юра Власенко 👨"
                                               "Я живу в городе Бобруйск 🏙"
                                               "Я начинающий программист 👨‍💻")

    elif message.text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("👋 Поздороваться")
        button2 = types.KeyboardButton("❓ Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую команду я не запрограммирован..")


name = ''
surname = ''
age = 0


@bot.message_handler(content_types=['text'])
def start_reg(message):
    bot.send_message(message.chat.id, "Как тебя зовут? ")
    bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:  # проверяем что возраст изменился
        try:
            age = int(message.text)  # проверяем, что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
            return get_surname(message)
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
    keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Запомню 😊')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'К сожалению не познакомились 😔')


# Запускаем бота
bot.polling(none_stop=True, interval=0)
