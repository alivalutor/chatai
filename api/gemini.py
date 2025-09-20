from loader import client
from google.api_core.exceptions import ServiceUnavailable, BadRequest, Unauthenticated
from services.chat_context import add_ai_response_to_history
from services.logging import write_log
from services.text_cleaner import clean_text
from services.text_splitter import split_into_blocks
from services.block_splitter import split_by_length


def edit_markdown(text):
    txt_clean = clean_text(text)
    txt_split = split_into_blocks(txt_clean)
    parts = split_by_length(txt_split)

    return parts


def request_ai(user_id, message):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message,
        )
        add_ai_response_to_history(user_id, response.text)
        write_log(response.text, "response.log")
        parts_msg = edit_markdown(response.text)
    except ServiceUnavailable as e:
        print(f"Ошибка 503: {e}")
        raise
    except BadRequest as e:
        print(f"Ошибка 400: {e}")
        raise ValueError("Неправильный запрос к ИИ")
    except Unauthenticated as e:
        print(f"Ошибка 401: {e}")
        raise ValueError("Проблема с API-ключом")

    return parts_msg
