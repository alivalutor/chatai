from config_data.config import MAX_HISTORY_LENGTH, META_PROMPT

assert (
    MAX_HISTORY_LENGTH is not None
), "MAX_HISTORY_LENGTH должен быть инициализирован и иметь значение!"

user_histories = {}


def context_for_ai(user_id, user_message):
    if user_id not in user_histories:
        user_histories[user_id] = [
            [{"text": META_PROMPT}],
            "Хорошо",
        ]
    user_histories[user_id].append(user_message)

    if len(user_histories[user_id]) > int(MAX_HISTORY_LENGTH):
        user_histories[user_id] = user_histories[user_id][-int(MAX_HISTORY_LENGTH) :]
    return user_histories[user_id]


def add_ai_response_to_history(user_id, ai_message):
    user_histories[user_id].append(ai_message)
