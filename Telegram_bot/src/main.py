import asyncio

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Update, Bot,
)
from telegram.constants import ParseMode
from telegram.error import Forbidden
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import broker
import settings
import text
from api import (
    delete_context,
    delete_message,
    get_all_chat_id,
    get_last_context_user,
    get_list_messages,
    get_or_create_user,
    is_admin_user,
    recover_message,
    save_question,
    yandex_off,
    yandex_on,
)

from broker import publish
from enums import ModelGPTEnum, ModelGPTEnumForBD
from helpers import prepare_data_for_gpt
from logger import logger


about_button = KeyboardButton(text.ABOUT_BUTTON)
news_button = KeyboardButton(text.NEWS_BUTTON)
delete_context_button = KeyboardButton(text.DELETE_CONTEXT_BUTTON)

reply_markup = ReplyKeyboardMarkup(
    [
        [delete_context_button],
        [about_button, news_button]
    ],
    resize_keyboard=True,
)

send_all_button = KeyboardButton(text.SEND_ALL)
admin_exit_button = KeyboardButton(text.EXIT)
admin_markup = ReplyKeyboardMarkup(
    [
        [send_all_button],
        [admin_exit_button]
    ],
    resize_keyboard=True,
)


delete_message_button = InlineKeyboardButton(
    text.DELETE_MESSAGE_BUTTON,
    callback_data="delete_from_context",
)
delete_reply_markup = InlineKeyboardMarkup.from_button(delete_message_button)

recover_message_button = InlineKeyboardButton(
    text.RECOVER_MESSAGE_BUTTON,
    callback_data="recover_from_context",
)
recover_reply_markup = InlineKeyboardMarkup.from_button(recover_message_button)

ADMIN_MENU, MAILING_SUBMENU = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.WELCOME_TEXT,
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.HELP_TEXT,
        reply_markup=reply_markup,
    )


async def yandex_on_command(update: Update, context: ContextTypes.DEFAULT_TYPE, cache_time=10) -> None:
    chat_id = update.effective_chat.id
    try:
        yandex_on(chat_id)
    except Exception as e:
        await context.bot.send_message(
            chat_id=settings.ADMIN_CHAT_ID,
            text=text.ERROR_MESSAGE_FOR_ADMIN.format(
                error_name=e.__class__.__name__,
                chat_id=chat_id,
                text_error=str(e),
            ),
            parse_mode='HTML',
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text=text.ERROR_MESSAGE_FOR_USER,
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.YANDEX_ON,
        reply_markup=reply_markup,
    )


async def yandex_off_command(update: Update, context: ContextTypes.DEFAULT_TYPE, cache_time=10) -> None:
    chat_id = update.effective_chat.id
    try:
        yandex_off(chat_id)
    except Exception as e:
        await context.bot.send_message(
            chat_id=settings.ADMIN_CHAT_ID,
            text=text.ERROR_MESSAGE_FOR_ADMIN.format(
                error_name=e.__class__.__name__,
                chat_id=chat_id,
                text_error=str(e),
            ),
            parse_mode='HTML',
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text=text.ERROR_MESSAGE_FOR_USER,
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.YANDEX_OFF,
        reply_markup=reply_markup,
    )


async def question_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id
    logger.info(f'Question from: {update.effective_user.first_name}:{chat_id}')

    try:
        question = update.message.text

        user = get_or_create_user(chat_id=chat_id)
        context_ = get_last_context_user(user=user)  # имя схоже с аргументом
        messages = get_list_messages(context=context_)
        users_model = user.model.value
        content_key = ModelGPTEnum.CONTENT_KEY.value[users_model]
        data_for_gpt = prepare_data_for_gpt(
            system_role=(context_.system_role
                         if context_
                         else ModelGPTEnum.DEFAULT_SYSTEM_ROLE.value[users_model]),
            messages=messages,
            content_key=content_key,
        )
        # Добавим в контекст текущий вопрос
        data_for_gpt.append({'role': 'user', content_key: question})

        queue = {
            ModelGPTEnumForBD.CHATGPT.value: settings.TO_CHAT_GPT_QUEUE,
            ModelGPTEnumForBD.YANDEXGPT.value: settings.TO_YANDEX_GPT_QUEUE,
        }
        message = save_question(
            user=user,
            question=question,
        )

        await publish(queue_name=queue.get(users_model), data=data_for_gpt, message_id=message.id)

    except Exception as error:
        await context.bot.send_message(
            chat_id=settings.ADMIN_CHAT_ID,
            text=text.ERROR_MESSAGE_FOR_ADMIN.format(
                error_name=error.__class__.__name__,
                chat_id=chat_id,
                text_error=str(error),
            ),
        )

        logger.error(f"{error.__class__.__name__}: {str(error)}")

        await context.bot.send_message(
            chat_id=chat_id,
            text=text.ERROR_MESSAGE_FOR_USER,
        )


async def about_button(update: Update, context: ContextTypes.DEFAULT_TYPE, cache_time=10) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.HELP_TEXT,
        reply_markup=reply_markup,
    )


async def new_button(update: Update, context: ContextTypes.DEFAULT_TYPE, cache_time=10) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.NEW_TEXT,
        reply_markup=reply_markup,
    )


async def delete_context_user(update: Update, context: ContextTypes.DEFAULT_TYPE, cache_time=10) -> None:
    """Удалить контекст."""
    chat_id = update.effective_chat.id

    result = delete_context(chat_id)

    if result:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text.DELETE_CONTEXT_SUCCESS,
            reply_markup=reply_markup,
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=text.DELETE_CONTEXT_FAILURE,
            reply_markup=reply_markup,
        )


async def delete_from_context(update: Update, context: ContextTypes.DEFAULT_TYPE, cache_time=10) -> None:

    query = update.callback_query

    result = delete_message(
        chat_id=query.message.chat_id,
        message_id=query.message.id,
    )
    if result:
        await query.edit_message_text(
            text=text.DELETE_MESSAGE_SUCCESS,
            reply_markup=recover_reply_markup,
        )
    else:
        await query.edit_message_text(
            text=text.DELETE_MESSAGE_FAILURE,
        )


async def recover_from_context(update: Update, context: ContextTypes.DEFAULT_TYPE, cache_time=10) -> None:

    query = update.callback_query

    result, answer = recover_message(
        chat_id=query.message.chat_id,
        message_id=query.message.id,
    )

    if result:
        await query.edit_message_text(
            text=answer,
            reply_markup=delete_reply_markup,
        )
    else:
        await query.edit_message_text(
            text=answer,
            reply_markup=recover_reply_markup,
        )


async def update_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.UPDATE_KEYBOARD,
        reply_markup=reply_markup,
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin_user(update.effective_chat.id):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text.WELCOME_ADMIN_TEXT,
            reply_markup=admin_markup,
        )
        return ADMIN_MENU
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text.NOT_ADMIN,
            reply_markup=reply_markup,
        )
        return ConversationHandler.END


async def input_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin_user(update.effective_chat.id):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text.WRITE_MESSAGE,
            reply_markup=admin_markup,
        )
    return MAILING_SUBMENU


async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_admin_user(update.effective_chat.id):
        admin_message = update.message.text
        if admin_message.split()[0] == settings.SAFEGUARD_PHRASE:
            users = get_all_chat_id()
            for user in users:
                try:
                    await context.bot.send_message(
                        chat_id=user.chat_id,
                        text=admin_message.lstrip(settings.SAFEGUARD_PHRASE).lstrip(),
                        reply_markup=reply_markup,
                    )
                except Forbidden:
                    # пользователь заблокировал бот или проблемы с ним самим
                    pass

                # Limit: 30 messages per second
                await asyncio.sleep(settings.SENDING_INTERVAL)

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text.ADMIN_MAILING_COMPLETED,
                reply_markup=reply_markup,
            )

            return ConversationHandler.END

        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text.ERROR_ADMIN_MESSAGE,
                reply_markup=admin_markup,
            )

            return MAILING_SUBMENU


async def admin_exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text.EXIT_ADMIN,
        reply_markup=reply_markup,
    )
    return ConversationHandler.END


async def send_message_by_chat_id(message, chat_id, model):
    await Bot(settings.BOT_TOKEN).send_message(
        chat_id=chat_id,
        text=text.ANSWER_MESSAGE.format(answer=message, model=model),
        reply_markup=delete_reply_markup,
        parse_mode=ParseMode.MARKDOWN,
    )


application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
if __name__ == '__main__':
    try:
        # Commands
        start_handler = CommandHandler('start', start)
        help_handler = CommandHandler("help", help_command)
        yandex_on_handler = CommandHandler("yandex_test_on", yandex_on_command)
        yandex_off_handler = CommandHandler("yandex_test_off", yandex_off_command)
        # Костыль, что бы у старых пользователей обновилась клавиатура
        old_command = CommandHandler(["about", "news", "delete_context"], update_keyboard)

        # Message
        question_answer_handler = MessageHandler(
            filters.TEXT & ~filters.Text(text.ALL_BUTTONS) & ~filters.COMMAND, question_answer)
        about_handler = MessageHandler(filters.Text([text.ABOUT_BUTTON]), about_button)
        new_handler = MessageHandler(filters.Text([text.NEWS_BUTTON]), new_button)
        del_context_handler = MessageHandler(filters.Text([text.DELETE_CONTEXT_BUTTON]), delete_context_user)

        # Callback
        delete_from_context = CallbackQueryHandler(callback=delete_from_context, pattern="^delete_from_context$")
        recover_from_context = CallbackQueryHandler(callback=recover_from_context, pattern="^recover_from_context$")

        # Admin
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('admin', admin)],
            states={
                ADMIN_MENU: [
                    MessageHandler(filters.Text([text.SEND_ALL]), input_message),
                    MessageHandler(filters.ALL & ~filters.Text([text.EXIT]), admin)
                ],
                MAILING_SUBMENU: [
                    MessageHandler(filters.TEXT & ~filters.Text([text.EXIT, text.SEND_ALL]), send_all),
                    MessageHandler(filters.ALL & ~filters.Text([text.EXIT]), input_message)
                ],
            },
            fallbacks=[MessageHandler(filters.Text([text.EXIT]), admin_exit)],
        )

        application.add_handler(start_handler)
        application.add_handler(help_handler)
        application.add_handler(yandex_on_handler)
        application.add_handler(yandex_off_handler)
        application.add_handler(old_command)
        application.add_handler(about_handler)
        application.add_handler(new_handler)
        application.add_handler(del_context_handler)
        application.add_handler(delete_from_context)
        application.add_handler(recover_from_context)
        application.add_handler(conv_handler)
        application.add_handler(question_answer_handler)

        loop = asyncio.get_event_loop()
        loop.create_task(broker.consume(settings.FROM_CHAT_GPT_QUEUE))
        loop.create_task(broker.consume(settings.FROM_YANDEX_GPT_QUEUE))

        application.run_polling()

    except Exception as global_error:
        logger.error(f"Error: {str(global_error)}")
        raise global_error
