from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


buttons = {
    "veg_yes": InlineKeyboardButton(
        "Да", callback_data="veg_yes"
    ),
    "veg_no": InlineKeyboardButton(
        "Нет, редко", callback_data="veg_no"
    ),
    "fatigue_yes": InlineKeyboardButton(
        "Да, часто", callback_data="fatigue_yes"
    ),
    "fatigue_no": InlineKeyboardButton(
        "Нет, редко", callback_data="fatigue_no"
    ),
    "seafood_yes": InlineKeyboardButton(
        "Да, регулярно", callback_data="seafood_yes"
    ),
    "seafood_no": InlineKeyboardButton(
        "Нет, редко",
        callback_data="seafood_no",
    ),
    "memory_often": InlineKeyboardButton("Часто", callback_data="memory_often"),
    "memory_sometimes": InlineKeyboardButton(
        "Иногда", callback_data="memory_sometimes"
    ),
    "memory_rarely": InlineKeyboardButton("Редко", callback_data="memory_rarely"),
    "screen_often": InlineKeyboardButton("Да, часто", callback_data="screen_often"),
    "screen_rarely": InlineKeyboardButton("Редко", callback_data="screen_rarely"),
    "vision_yes": InlineKeyboardButton(
        "Да", callback_data="vision_yes"
    ),
    "vision_no": InlineKeyboardButton(
        "Нет", callback_data="vision_no"
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
        "Да, часто",
        callback_data="digestion_yes",
    ),
    "digestion_no": InlineKeyboardButton(
        "Нет",
        callback_data="digestion_no",
    ),
    "repro_support_yes": InlineKeyboardButton("Да", callback_data="repro_support_yes"),
    "repro_support_no": InlineKeyboardButton("Нет", callback_data="repro_support_no"),
    "beauty_yes": InlineKeyboardButton("Да", callback_data="beauty_yes"),
    "beauty_no": InlineKeyboardButton("Нет", callback_data="beauty_no"),
    "conscious_yes": InlineKeyboardButton("Да", callback_data="conscious_yes"),
    "conscious_no": InlineKeyboardButton("Нет", callback_data="conscious_no"),
    "ready_yes": InlineKeyboardButton("Да", callback_data="ready_yes"),
    "ready_no": InlineKeyboardButton("Нет", callback_data="ready_no"),
    "male_support_yes": InlineKeyboardButton("Да", callback_data="male_support_yes"),
    "male_support_no": InlineKeyboardButton("Нет", callback_data="male_support_no"),
    "male_symptoms_yes": InlineKeyboardButton(
        "Да, есть", callback_data="male_symptoms_yes"
    ),
    "male_symptoms_no": InlineKeyboardButton("Нет", callback_data="male_symptoms_no"),
}

child_buttons = {
    "veg_child_yes": InlineKeyboardButton("Да", callback_data="veg_child_yes"),
    "veg_child_no": InlineKeyboardButton("Нет, редко", callback_data="veg_child_no"),
    "seafood_child_yes": InlineKeyboardButton("Да, регулярно", callback_data="seafood_child_yes"),
    "seafood_child_no": InlineKeyboardButton("Нет, редко", callback_data="seafood_child_no"),
    "memorybad_child_often": InlineKeyboardButton("Часто", callback_data="memorybad_child_often"),
    "memorybad_child_time_to_time": InlineKeyboardButton("Иногда", callback_data="memorybad_child_time_to_time"),
    "memorybad_child_rarely": InlineKeyboardButton("Редко", callback_data="memorybad_child_rarely"),
    "screentime_child_often": InlineKeyboardButton("Да, часто", callback_data="screentime_child_often"),
    "screentime_child_rarely": InlineKeyboardButton("Редко", callback_data="screentime_child_rarely"),
    "activesport_child_yes": InlineKeyboardButton("Да", callback_data="activesport_child_yes"),
    "activesport_child_no": InlineKeyboardButton("Нет", callback_data="activesport_child_no"),
    "parametr_child_norm": InlineKeyboardButton("Нормальный", callback_data="parametr_child_norm"),
    "parametr_child_underweight": InlineKeyboardButton("Недостаточный", callback_data="parametr_child_underweight"),
    "parametr_child_overweight": InlineKeyboardButton("Избыточный", callback_data="parametr_child_overweight"),
    "stomach_child_often": InlineKeyboardButton("Часто", callback_data="stomach_child_often"),
    "stomach_child_rarely": InlineKeyboardButton("Редко", callback_data="stomach_child_rarely"),
}


restart_and_view_kb = InlineKeyboardMarkup(row_width=2)
restart_and_view_kb.add(
    InlineKeyboardButton("Перезапуск", callback_data="restart_bot"),
    InlineKeyboardButton("Результат", callback_data="view_recommendations"),
    InlineKeyboardButton("💊 Мои БАДы", url="https://www.marinehealth.asia/products")
)