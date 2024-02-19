def prepare_data_for_gpt(system_role: str, messages: list[tuple], content_key: str = 'content'):
    context_messages = []
    default_system_role = {
        'role': 'system',
        content_key: system_role,
    }
    context_messages.append(default_system_role)
    for question, answer in messages:
        if question and answer:  # Обратное возможно из-за ошибки при отладке
            context_messages.extend((
                {'role': 'user', content_key: question},
                {'role': 'assistant', content_key: answer}
            ))
    return context_messages
