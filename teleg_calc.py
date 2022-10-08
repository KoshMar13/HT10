from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from random import randint
import logging
from config import TOKEN

logging.basicConfig(filename='telegbot_log', filemode='s',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
                    )
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text(
        'Шалом! Я умею считать. Что посчитаем? \n'
        'Команда /stop, чтобы прекратить разговор.\n\n')
    update.message.reply_text(
        '1 - рациональные числа: \n2 - комплесные числа: \n')
    return 1


def choice(update, context):
    user = update.message.from_user
    logger.info("Выбор операции: %s: %s", user.first_name, update.message.text)
    user_choice = update.message.text
    if user_choice in '12':
        if user_choice == '1':
            update.message.reply_text(
                'Введите первое рациональное число')
            return 2
        if user_choice == '2':
            context.bot.send_message(
                update.effective_chat.id, 'Введите вещ. и мним. первого числа через ПРОБЕЛ: ')
            return 3
    else:
        update.message.reply_text(
            'Это не то.\n 1 - рациональные числа: 2 - комплесные числа: \n')


def rational_one(update, context):
    user = update.message.from_user
    logger.info("Пользователь ввел число: %s: %s",
                user.first_name, update.message.text)
    get_rational = update.message.text
    if get_rational.isdigit():
        get_rational = float(get_rational)
        context.user_data['rational_one'] = get_rational
        update.message.reply_text(
            'Введите второе рациональное')
        return 4

    else:
        update.message.reply_text(
            'Нужно ввести число')


def rational_two(update, context):
    user = update.message.from_user
    logger.info("Пользователь ввел число: %s: %s",
                user.first_name, update.message.text)
    get_rational = update.message.text
    if get_rational.isdigit():
        get_rational = float(get_rational)
        context.user_data['rational_two'] = get_rational
        update.message.reply_text(
            'Что мутим: \n\n+ - для сложения: \n- - для вычитания: \n* - для умножения: \n/ - для деления: \n')
        return 5


def operatons_rational(update, context):
    user = update.message.from_user
    logger.info(
        "Пользователь выбрал операцию %s: %s", user.first_name, update.message.text)
    rational_one = context.user_data.get('rational_one')
    rational_two = context.user_data.get('rational_two')
    user_choice = update.message.text
    if user_choice in '+-/*':
        if user_choice == '+':
            result = rational_one + rational_two
        if user_choice == '-':
            result = rational_one - rational_two
        if user_choice == '*':
            result = rational_one * rational_two
        if user_choice == '/':
            try:
                result = rational_one / rational_two
            except:
                update.message.reply_text('Деление на ноль запрещено законом')
        update.message.reply_text(
            f'Результат: {rational_one}{user_choice}{rational_two} = {result}')
        return ConversationHandler.END
    else:
        update.message.reply_text('Это не то.Введите +-*/')


def complex_one(update, context):
    user = update.message.from_user
    logger.info(
        "Пользователь ввел число %s: %s", user.first_name, update.message.text)
    user_choice = update.message.text
    test = user_choice.replace('-', '')
    if ' ' in test and (test.replace(' ', '')).isdigit():
        user_choice = user_choice.split(' ')
        complex_one = complex(int(user_choice[0]), int(user_choice[1]))
        context.user_data['complex_one'] = complex_one
        update.message.reply_text(
            f'Первое число {complex_one},  Введите вещ. и мним. второго числа через ПРОБЕЛ: ')
        return 6
    else:
        update.message.reply_text(
            'Это не то. Введите вещ. и мним. второго числа через ПРОБЕЛ')


def complex_two(update, context):
    user = update.message.from_user
    logger.info(
        "Пользователь ввел число %s: %s", user.first_name, update.message.text)
    user_choice = update.message.text
    test = user_choice.replace('-', '')
    if ' ' in test and (test.replace(' ', '')).isdigit():
        user_choice = user_choice.split(' ')
        complex_two = complex(int(user_choice[0]), int(user_choice[1]))
        context.user_data['complex_two'] = complex_two
        update.message.reply_text(
            f'Второе число {complex_two}, Выберите операцию с числами: \n\n+ - для сложения: \n- - для вычетания: \n* - для умножения: \n/ - для деления: \n')
        return 7
    else:
        update.message.reply_text(
            'Это не то. Введите +-*/')


def operatons_complex(update, context):
    user = update.message.from_user
    logger.info(
        "Пользователь выбрал операцию %s: %s", user.first_name, update.message.text)
    complex_one = context.user_data.get('complex_one')
    complex_two = context.user_data.get('complex_two')
    user_choice = update.message.text
    if user_choice in '+-/*':
        if user_choice == '+':
            result = complex_one + complex_two
        if user_choice == '-':
            result = complex_one - complex_two
        if user_choice == '*':
            result = complex_one * complex_two
        if user_choice == '/':
            try:
                result = complex_one / complex_two
            except:
                update.message.reply_text('Деление на ноль запрещено законом')
        update.message.reply_text(
            f'Результат: {complex_one} {user_choice} {complex_two} = {result}')
        return ConversationHandler.END
    else:
        update.message.reply_text('Это не то.Введите +-*/')


def stop(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    update.message.reply_text(
        'Ну и ладно, не больно-то и хотелось.\n'
        'Когда захочешь посчитать, заходи'
    )
    return ConversationHandler.END


bot_token = TOKEN
bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher
conversation_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
                                           states={
    1: [MessageHandler(Filters.text & ~Filters.command, choice)],
    2: [MessageHandler(Filters.text & ~Filters.command, rational_one)],
    4: [MessageHandler(Filters.text & ~Filters.command, rational_two)],
    5: [MessageHandler(Filters.text & ~Filters.command, operatons_rational)],
    7: [MessageHandler(Filters.text & ~Filters.command, operatons_complex)],
    3: [MessageHandler(Filters.text & ~Filters.command, complex_one)],
    6: [MessageHandler(Filters.text & ~Filters.command, complex_two)],
},
    fallbacks=[CommandHandler('stop', stop)]
)

dispatcher.add_handler(conversation_handler)

updater.start_polling()
updater.idle()
