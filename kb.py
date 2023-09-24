from aiogram.types import InlineKeyboardButton

buttons = {
    "veg_yes": InlineKeyboardButton(
        "Да, я ем много фруктов и овощей", callback_data="veg_yes"
    ),
    "veg_no": InlineKeyboardButton(
        "Нет, я редко употребляю фрукты и овощи", callback_data="veg_no"
    ),
    "fatigue_yes": InlineKeyboardButton(
        "Да, я часто ощущаю усталость и истощение", callback_data="fatigue_yes"
    ),
    "fatigue_no": InlineKeyboardButton(
        "Нет, я редко испытываю усталость и истощение", callback_data="fatigue_no"
    ),
    "seafood_yes": InlineKeyboardButton(
        "Да, я регулярно употребляю морепродукты", callback_data="seafood_yes"
    ),
    "seafood_no": InlineKeyboardButton(
        "Нет, я редко или почти никогда не употребляю морепродукты",
        callback_data="seafood_no",
    ),
    "memory_often": InlineKeyboardButton("Часто", callback_data="memory_often"),
    "memory_sometimes": InlineKeyboardButton(
        "Время от времени", callback_data="memory_sometimes"
    ),
    "memory_rarely": InlineKeyboardButton("Редко", callback_data="memory_rarely"),
    "screen_often": InlineKeyboardButton("Да, часто", callback_data="screen_often"),
    "screen_rarely": InlineKeyboardButton("Редко", callback_data="screen_rarely"),
    "vision_yes": InlineKeyboardButton(
        "Да, у меня есть проблемы со зрением", callback_data="vision_yes"
    ),
    "vision_no": InlineKeyboardButton(
        "Нет, у меня нет проблем со зрением", callback_data="vision_no"
    ),
    "joints_yes": InlineKeyboardButton("Да", callback_data="joints_yes"),
    "joints_no": InlineKeyboardButton("Нет", callback_data="joints_no"),
    "sport_yes": InlineKeyboardButton("Да", callback_data="sport_yes"),
    "sport_no": InlineKeyboardButton("Нет", callback_data="sport_no"),
    "numbness_often": InlineKeyboardButton("Часто", callback_data="numbness_often"),
    "numbness_rarely": InlineKeyboardButton("Редко", callback_data="numbness_rarely"),
    "headaches_often": InlineKeyboardButton("Часто", callback_data="headaches_often"),
    "headaches_rarely": InlineKeyboardButton("Редко", callback_data="headaches_rarely"),
    "youthfulness_yes": InlineKeyboardButton("Да", callback_data="youthfulness_yes"),
    "youthfulness_no": InlineKeyboardButton("Нет", callback_data="youthfulness_no"),
    "detox_yes": InlineKeyboardButton("Да", callback_data="detox_yes"),
    "detox_no": InlineKeyboardButton("Нет", callback_data="detox_no"),
    "digestion_yes": InlineKeyboardButton(
        "Да, у меня часто возникают проблемы с пищеварением",
        callback_data="digestion_yes",
    ),
    "digestion_no": InlineKeyboardButton(
        "Нет, у меня нет значительных проблем с пищеварением",
        callback_data="digestion_no",
    ),
    "repro_support_yes": InlineKeyboardButton("Да", callback_data="repro_support_yes"),
    "repro_support_no": InlineKeyboardButton("Нет", callback_data="repro_support_no"),
    "beauty_yes": InlineKeyboardButton("Да", callback_data="beauty_yes"),
    "beauty_no": InlineKeyboardButton("Нет", callback_data="beauty_no"),
}

age_buttons = {
    "age_less_18": "Меньше 18 лет",
    "age_18_35": "18-35 лет",
    "age_more_35": "Старше 35 лет",
}
