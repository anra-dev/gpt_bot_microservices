from sqlalchemy.exc import NoResultFound

from database import session
from enums import ModelGPTEnum, ModelGPTEnumForBD
from models import Context, User, Message


def get_context_messages(system_role, messages):

    context_messages = []
    default_system_role = {
        'role': 'system',
        'text': system_role,
    }
    context_messages.append(default_system_role)
    for question, answer in messages:
        context_messages.extend((
            {'role': 'user', 'text': question},
            {'role': 'assistant', 'text': answer}
        ))
    return context_messages


def get_last_context_user(user):

    try:
        context = session.query(Context).filter_by(
            user=user,
            is_active=True,
        ).one()
    except NoResultFound:
        context = None

    return context


def get_list_messages(context):
    list_messages = []
    if context is not None:
        messages = session.query(Message).filter_by(
            context=context,
            is_active=True,
        ).all()

        for message in messages:
            list_messages.append((message.question, message.answer))

    return list_messages


def get_or_create_user(chat_id):

    try:
        user = session.query(User).filter_by(
            chat_id=chat_id,
        ).one()
    except NoResultFound:
        user = User(
            chat_id=chat_id,
            is_admin=False,
        )
        session.add(user)
        session.commit()

    return user


def save_question(user, question):

    try:
        context = session.query(Context).filter_by(
            user=user,
            is_active=True,
        ).one()
    except NoResultFound:
        context = Context(
            user=user,
            is_active=True,
            system_role=ModelGPTEnum.DEFAULT_SYSTEM_ROLE.value[user.model.value],
        )
        session.add(context)

    message = Message(
        context=context,
        question=question,
        is_active=True,
    )
    session.add(message)
    session.commit()

    return message


def save_answer(message_id, answer):

    try:
        message = session.query(Message).filter_by(
            id=message_id
        ).one()
    except NoResultFound:
        pass
    else:
        message.answer = answer
        session.add(message)
        session.commit()

        return message


def delete_context(chat_id):
    """Мягкое удаление контекста.

    Если запись существует, то помечаем ее неактивной
    и возвращает True, иначе False"""
    try:
        user = session.query(User).filter_by(
            chat_id=chat_id,
        ).one()
    except NoResultFound:
        return False

    try:
        context = session.query(Context).filter_by(
            user=user,
            is_active=True,
        ).one()
    except NoResultFound:
        return False

    context.is_active = False
    session.commit()
    return True


def delete_message(chat_id, message_id):
    """Мягкое удаление сообщения.

    Если запись существует, то помечаем ее неактивной и возвращает True, иначе False"""
    try:
        user = session.query(User).filter_by(
            chat_id=chat_id,
        ).one()
    except NoResultFound:
        return False

    try:
        context = session.query(Context).filter_by(
            user=user,
            is_active=True,
        ).one()
    except NoResultFound:
        return False

    try:
        messages = session.query(Message).filter_by(
            context=context,
            message_id=message_id,
            is_active=True,
        ).one()
    except NoResultFound:
        return False

    messages.is_active = False
    session.commit()
    return True


def recover_message(chat_id, message_id):
    """Восстановление сообщения.

    Если запись существует, то помечаем ее неактивной и возвращает True, иначе False"""
    fail_message = 'Не удалось восстановить сообщение.'

    try:
        user = session.query(User).filter_by(
            chat_id=chat_id,
        ).one()
    except NoResultFound:
        return False, fail_message

    try:
        context = session.query(Context).filter_by(
            user=user,
            is_active=True,
        ).one()
    except NoResultFound:
        return False, fail_message

    try:
        messages = session.query(Message).filter_by(
            context=context,
            message_id=message_id,
            is_active=False,
        ).one()
    except NoResultFound:
        return False, fail_message

    messages.is_active = True
    session.commit()
    return True, messages.answer


def is_admin_user(chat_id):
    """Проверка - является ли пользователь с указанным chat_id администратором."""

    user = session.query(User).filter_by(
        chat_id=chat_id,
    ).one()

    return user.is_admin


def get_all_chat_id():
    """Получает всех пользователей."""
    return session.query(User).all()


def define_model(chat_id, model):
    try:
        user = session.query(User).filter_by(
            chat_id=chat_id,
        ).one()
    except NoResultFound:
        user = User(
            chat_id=chat_id,
            is_admin=False,
        )
        session.add(user)
    user.model = model
    session.commit()


def yandex_on(chat_id):
    define_model(chat_id, ModelGPTEnumForBD.YANDEXGPT)


def yandex_off(chat_id):
    define_model(chat_id, ModelGPTEnumForBD.CHATGPT)
