import telebot
import math
from telebot import types

token = ''

bot = telebot.TeleBot(token)

a = ''
b = ''
c = ''
d = ''
x1 = ''
x2 = ''
x = ''

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    markup = types.ReplyKeyboardRemove(selective = False)

    msg = bot.send_message(message.chat.id, "Привет " + message.from_user.first_name + ", я бот-калькулятор\nВведите /calculator , если нужен калькулятор\nВведите /equation2 ,если нужно решить квадратное уравнение  ", reply_markup=markup)

@bot.message_handler(commands=["equation2"])
def start(message):
    msg = bot.send_message(message.chat.id, 'Введите коэффициенты для уравнения\nax^2 + bx + c = 0:\nВведите чему равно а:')
    bot.register_next_step_handler(msg, start_a)


def start_a(message):
    try:
        global a

        a = int(message.text)

        bot.send_message(message.chat.id, 'a = {}'.format(a))
        msg = bot.send_message(message.chat.id,'Введите чему равно b:')
        bot.register_next_step_handler(msg, start_b)
    except Exception as e:
        bot.reply_to(message, 'Error\nВведите /start')

def start_b(message):
    try:
        global b

        b = int(message.text)

        bot.send_message(message.chat.id, 'b = {}'.format(b))
        msg = bot.send_message(message.chat.id,'Введите чему равно c:')
        bot.register_next_step_handler(msg, start_c)
    except Exception as e:
        bot.reply_to(message, 'Error\nВведите /start')

def start_c(message):
    try:
        global c
        c = int(message.text)

        bot.send_message(message.chat.id, 'c = {}'.format(c))
        d = b ** 2 - 4 * a * c
        bot.send_message(message.chat.id,'Дискриминант = b^2 - 4 * a * c = {}'.format(d) + ' = ({})^2'.format((math.sqrt(d))) )

        if d > 0:
            x1 = (-b + math.sqrt(d)) / (2 * a)
            x2 = (-b - math.sqrt(d)) / (2 * a)
            bot.send_message(message.chat.id,"x1 = %.2f \nx2 = %.2f" % (x1, x2) + "\nВведите /equation2 ,если нужно решить еще квадратное уравнение" ) #'x1 = %.2f{}'.format(x1) + '\nx2 = {}'.format(x2))
        elif d == 0:
            x = -b / (2 * a)
            bot.send_message(message.chat.id,"x = %.2f" % x ) # 'x = {}'.format(x))
        # else:
        #     bot.send_message(message.chat.id, 'Корней нет')
    except Exception as e:
        bot.reply_to(message, 'Error\nВведите /start')

user_num1 = ''
user_num1 = ''
user_proc = ''
user_result = None

@bot.message_handler(commands=['calculator'])
def send_welcome(message):
    markup = types.ReplyKeyboardRemove(selective = False)

    msg = bot.send_message(message.chat.id, "\nВведите число ", reply_markup=markup)
    bot.register_next_step_handler(msg, process_num1_step)

def process_num1_step(message, user_result = None):
    try:
        global user_num1

        if user_result == None:
            user_num1 = int(message.text)
        else:
            user_num1 = str(user_result)

        markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
        itembtn1 = types.KeyboardButton('+')
        itembtn2 = types.KeyboardButton('-')
        itembtn3 = types.KeyboardButton('*')
        itembtn4 = types.KeyboardButton('/')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

        msg = bot.send_message(message.chat.id, "Выберите операцию", reply_markup=markup)
        bot.register_next_step_handler(msg, process_proc_step)
    except Exception as e:
        bot.reply_to(message, 'Error...')


def process_proc_step(message):
    try:
        global user_proc

        user_proc = message.text


        markup = types.ReplyKeyboardMarkup(selective=False)

        msg = bot.send_message(message.chat.id, "Введите еще число", reply_markup=markup)
        bot.register_next_step_handler(msg, process_num2_step)
    except Exception as e:
        bot.reply_to(message, 'Error...')


def process_num2_step(message, user_result = None):
    try:
        global user_num2

        user_num2 = int(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2)
        itembtn1 = types.KeyboardButton('Результат')
        # itembtn2 = types.KeyboardButton('Продолжить вычисления')
        markup.add(itembtn1)#, itembtn2)

        msg = bot.send_message(message.chat.id, "Показать результат?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_alternative_step)
    except Exception as e:
        bot.reply_to(message, 'Error...')


def process_alternative_step(message):
    try:
        calc()

        markup = types.ReplyKeyboardMarkup(selective=False)

        if message.text.lower() == 'результат':
            bot.send_message(message.chat.id, calcResultPrint(), reply_markup=markup)
        elif message.text.lower() == 'продолжить вычисление':
            process_num1_step(message, user_result)

    except Exception as e:
        bot.reply_to(message, 'Error...')

def calcResultPrint():
    global user_num1, user_num2, user_proc, user_result
    return "Результат: " + (str(user_num1) + ' ' + user_proc + ' ' + str(user_num2)) + ' = ' + str(user_result)

def calc():
    global user_num1, user_num2, user_proc, user_result

    user_result = eval(str(user_num1) + user_proc + str(user_num2))

    return user_result
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling(none_stop=True)
