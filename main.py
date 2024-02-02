import datetime
import logging
import pytz

from telegram.ext import Updater, CommandHandler

import config
import jokes
import weather

TOKEN = config.TOKEN
CHAT_ID = config.CHAT_ID
TIME = config.TIME

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()


def start(update, context):
    """greet the user - todo"""
    context.bot.send_message(chat_id=update.message.chat_id, text="start message")


def set_timer(update, context):
    """add daily message to queue"""
    context.bot.send_message(chat_id=update.message.chat_id, text=f"🖤 таймер установлен! сообщения будут приходить в"
                                                                  f" {TIME}:00 🖤")
    job = context.job_queue.run_daily(send_daily_message, time=datetime.time(hour=TIME, minute=00,
                                                                             tzinfo=pytz.timezone('Europe/Moscow')),
                                      days=(0, 1, 2, 3, 4, 5, 6))
    context.chat_data['send_daily_message'] = job


def send_daily_message(context):
    """send daily message"""
    message = ""
    if 6 <= TIME <= 11:
        message += "☀ доброе утро! ☀\n\n"
    elif 12 <= TIME <= 17:
        message += "☀ добрый день! ☀\n\n"
    elif 18 <= TIME <= 21:
        message += "🌙 добрый вечер! 🌙\n\n"
    else:
        message += "🌙 доброй ночи! 🌙\n\n"

    message += f"сегодня {datetime.datetime.now().day} {config.MONTHS[datetime.datetime.now().month - 1]}. " \
               f"погода сейчас: {weather.get_weather()}\n\n" \
               f"анекдот дня:\n{jokes.get_joke()}\n\n" \
               f"хорошего дня! 🖤"
    context.bot.send_message(chat_id=CHAT_ID, text=message)


def send_weather(context):
    """send weather forecast"""
    message = f"погода сейчас: {weather.get_weather()}"
    context.bot.send_message(chat_id=CHAT_ID, text=message)


def stop_notify(update, context):
    """stop daily messages"""
    chat_id = update.message.chat_id
    job = context.chat_data.get('send_daily_message')
    if job:
        job.schedule_removal()
        del context.chat_data['send_daily_message']
        context.bot.send_message(chat_id=chat_id, text="🌙 автоматические сообщения остановлены 🌙")
    else:
        context.bot.send_message(chat_id=chat_id, text="автоматические сообщения не были установлены!")


def error(update, context):
    """log errors caused by updates"""
    logger.warning(f'update {update} caused error {context.error}')


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('set_timer', set_timer))
    dp.add_handler(CommandHandler('stop', stop_notify))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
