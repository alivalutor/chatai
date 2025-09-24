import base64
import io
import time
from api import gemini
from loader import bot
from PIL import Image
from google.api_core.exceptions import ServiceUnavailable
from services.chat_context import context_for_ai
from services.logging import write_log
from services.user_check import is_user_allowed


def add_message_part(message):
    current_message_parts = []
    if len(message) == 1:
        current_message_parts.append({"text": message[0]})
    elif len(message) == 2:
        current_message_parts.append({"text": message[0]})
        current_message_parts.append(
            {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": message[1],
                }
            }
        )

    return current_message_parts


def send_message(message, result):
    max_retries = 3
    delay = 5

    for attempt in range(max_retries):
        try:
            for part in result:
                bot.send_message(message.chat.id, part, parse_mode="Markdown")
            break
        except ServiceUnavailable:
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                bot.reply_to(message, "ИИ перегружен, попробуй позже.")
        except Exception as e:
            bot.reply_to(message, f"Ошибка при отправке сообщения от ИИ:'\n'{str(e)}")
            log_txt = ["\n" + message.text + "\n", "----------\n", result]
            write_log(log_txt, "filed_md.log", "a")
            break


@bot.message_handler(content_types=["photo"])
def handle_photo_message(message):
    if not is_user_allowed(message.from_user.id):
        bot.reply_to(message, "Извините, у вас нет доступа к этому боту.")
        return

    thinking_message = bot.send_message(
        message.chat.id, "Получил фото! Обрабатываю запрос..."
    )
    bot.send_chat_action(message.chat.id, "typing")

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    img = Image.open(io.BytesIO(downloaded_file))
    text_prompt = (
        message.caption
        if message.caption
        else "Опиши, что изображено на этой фотографии."
    )
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    history_context = context_for_ai(
        message.from_user.id, add_message_part([text_prompt, img_base64])
    )
    result = gemini.request_ai(message.from_user.id, history_context)

    bot.delete_message(thinking_message.chat.id, thinking_message.message_id)

    send_message(message, result)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if not is_user_allowed(message.from_user.id):
        bot.reply_to(message, "Извините, у вас нет доступа к этому боту.")
        return

    thinking_message = bot.send_message(
        message.chat.id, "Получил запрос! Готовлю ответ..."
    )
    bot.send_chat_action(message.chat.id, "typing")

    history_context = context_for_ai(
        message.from_user.id, add_message_part([message.text])
    )
    result = gemini.request_ai(message.from_user.id, history_context)

    bot.delete_message(thinking_message.chat.id, thinking_message.message_id)

    send_message(message, result)
