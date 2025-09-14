import re
from google import genai
from config_data.config import GEMINI_API_KEY
from services.chat_context import add_ai_response_to_history
from services.text_cleaner import clean_text
from services.text_splitter import split_into_blocks
from services.block_splitter import split_by_length


def edit_markdown(text):
    txt_clean = clean_text(text)
    txt_split = split_into_blocks(txt_clean)
    parts = split_by_length(txt_split)

    return parts


def request_ai(user_id, message):
    client = genai.Client()
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=message
        )
        add_ai_response_to_history(user_id, response.text)
        parts_msg = edit_markdown(response.text)
    except Exception as e:
        parts_msg = [f"Ошибка при запросе к ИИ: {str(e)}"]

    return parts_msg
