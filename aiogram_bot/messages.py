

class Messages:
    START_MESSAGE = "👥Выберите студию"
    SELECT_USER_MESSAGE = "Выберите пользователя группы "
    BACK_TO_GROUPS_MESSAGE = "⬅️ К группам"
    BACK_TO_USERS_MESSAGE = "⬅️ К пользователям"
    BLOCK_USER_MESSAGE = "⛔️ Заблокировать"
    BAN_ALL_GROUP_USERS = "⛔️ Заблокировать группу"
    UNBAN_ALL_GROUP_USERS = "✅ Разблокировать группу"
    USER_MESSAGE = "Пользователь:"
    USER_STATUS_MESSAGE = "Статус: "
    USER_LAST_LOGON_MESSAGE = "Последний раз подключался: "
    USER_STATUS_STATE_MESSAGE = {
        0: "🔴 Заблокирован",
        1: "🟢 Подключён",
        2: "⚪ Разблокирован"
    }

    USER_STATUS_STATE_EMOJI = {
        0: "🔴",
        1: "🟢",
        2: "⚪️"
    }

    USER_TURN_STATE = {
        True: "❌ Заблокировать",
        False: "✅ Разблокировать",
    }

    CALLBACK_TURN_STATE = {
        True: "disable",
        False: "enable",
    }

    USER_GROUP_DICT = {
        "EKB": "Екатеринбург",
        "Krasnoyarsk": "Красноярск",
        "Nsk-Bogatkova": "НСК Богаткова",
        "Nsk-Dusi": "НСК Дуси",
        "Nsk-Oktyabr": "НСК Октябрьская",
        "Nsk-Titova": "НСК Титова",
        "SPB": "Санкт-Петербург",
        "Tomsk": "Томск",
        "Tymen": "Тюмень",
        "Uprava": "*Управляющие*"
    }

    CALLBACK_DATA = {
        "ON"
    }



messages = Messages()
