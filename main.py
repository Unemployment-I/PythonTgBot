import logging
from telegram.ext import Application, ApplicationBuilder, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup
from random import randrange


BOT_TOKEN = "6932663581:AAEYHy1nX__cQTiPy_bhngU4QqKe_6-RFtk"
TIMER = 5
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)
reply_keyboard_0 = [['/start']]
markup_0 = ReplyKeyboardMarkup(reply_keyboard_0, resize_keyboard=True)
reply_keyboard_1 = [['/help']]
markup_1 = ReplyKeyboardMarkup(reply_keyboard_1, resize_keyboard=True)
reply_keyboard_2 = [['Какие вопросы можно задать?', 'Сделай фонтанчик!!!', 'До свидания!'], ['/help']]
markup_2 = ReplyKeyboardMarkup(reply_keyboard_2, one_time_keyboard=False, resize_keyboard=True)
reply_keyboard_3 = [['Где ты сейчас?', 'Сколько ты живёшь?', 'Бывал ли ты в космосе?'], ['/help']]
markup_3 = ReplyKeyboardMarkup(reply_keyboard_3, one_time_keyboard=False, resize_keyboard=True)
reply_keyboard_4 = [['/fountains', '/no_fountains'], ['/help']]
markup_4 = ReplyKeyboardMarkup(reply_keyboard_4, one_time_keyboard=False, resize_keyboard=True)


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    print(user.mention_html())
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я счастливый кит, что плавает всегда и везде.", reply_markup=markup_1)


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    t = open('text.txt', 'r', encoding="utf-8").read()
    print(t)
    await update.message.reply_text(t, reply_markup=markup_2)


async def echo(update, context):
    t = update.message.text.lower()
    if 'какие вопросы можно задать' in t:
        await update.message.reply_text('Мне можно задать следующие вопросы:', reply_markup=markup_3)
    elif 'где ты сейчас' in t:
        n = randrange(0, 6)
        d = {0: ['Атлантическом', '-23.412101%2C-37.618230', '50,50'],
            1: ['Атлантическом', '-33.693802%2C23.218821', '40,40'],
            2: ['Тихом', '-156.351156%2C-0.498715', '80,80'],
            3: ['Индийском', '70.624346%2C-24.028618', '50,50'],
            4: ['Южном', '-159.823463%2C-69.439980', '15,15'],
            5: ['Северном Ледовитом', '-154.399270%2C72.573089', '25,25'],
            }
        ocean = d[n]
        static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ocean[1]}&spn={ocean[2]}&l=map"
        await context.bot.send_photo(
            update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
            # Ссылка на static API, по сути, ссылка на картинку.
            # Телеграму можно передать прямо её, не скачивая предварительно карту.
            static_api_request,
            caption=f"Сейчас я в {ocean[0]} океане"
            )
    elif 'сколько ты живёшь' in t:
        await update.message.reply_text('''ОООООООО мой дорогой друг! Живу я очень и очень долго...
Настолько долго что сам сбился со счёту...''')
    elif 'бывал ли ты в космосе' in t:
        await update.message.reply_text('''Бывал! Ещё как бывал!!! Где же толко я не был...''')
    elif 'сделай фонтан' in t:
        await update.message.reply_text('''Ты решил посмотреть на мой фонтанчик?
Ну что ж, теперь фонтанчик будет каждые 10 минут, если ты меня не остановишь''', reply_markup=markup_4)
    elif 'до свидания' in t or 'пока' in t and len(t) <= 10:
        await update.message.reply_text('''До свидания мой дорогой друг!''', reply_markup=markup_0)
    else:
        await update.message.reply_text(update.message.text)


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# Обычный обработчик, как и те, которыми мы пользовались раньше.
async def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_repeating(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

    text = '🐳'
    if job_removed:
        text = 'Фонтаны уже запущены'
    await update.effective_message.reply_text(text)


async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text='🐳')


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Фонтаны остановлены' if job_removed else 'Фонтаны не были запущены!'
    await update.message.reply_text(text)


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("fountains", set_timer))
    application.add_handler(CommandHandler("no_fountains", unset))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()


if __name__ == '__main__':
    main()
