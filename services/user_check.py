from config_data.config import USER_ID

assert USER_ID is not None, "USER_ID должен быть инициализирован и иметь значение!"
ALLOWED_USER_IDS = USER_ID.split(",")


def is_user_allowed(id_user):
    if str(id_user) in ALLOWED_USER_IDS:
        return True
    else:
        return False
