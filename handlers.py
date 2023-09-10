from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from main import logging
from states import Questionnaire
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from variables import get_recommended_baas


@dp.message_handler(lambda message: message.text == "Начать", state="*")
@dp.message_handler(commands="start", state="*")
async def user_name(message: types.Message):
    await Questionnaire.Name.set()
    await message.answer("Ваше имя?")


@dp.message_handler(state=Questionnaire.Name)
async def phone(message: types.Message, state: FSMContext):
    await Questionnaire.Phone.set()
    await state.update_data(name=message.text)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_request = KeyboardButton("Отправить мой номер телефона", request_contact=True)
    markup.add(btn_request)
    await message.answer(
        "Приятно познакомиться! Предоставьте ваш контактный номер, пожалуйста",
        reply_markup=markup,
    )


@dp.message_handler(content_types=["contact"], state=Questionnaire.Phone)
async def handle_contact(message: types.Message, state: FSMContext):
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)

        await message.answer("Спасибо, получил ваш номер!")
        await Questionnaire.Age.set()  # переходим к следующему этапу
        await user_age(message, state)  # вызываем функцию user_age
    else:
        await message.answer("Что-то пошло не так, попробуйте еще раз.")


@dp.message_handler(state=Questionnaire.Phone)
async def user_age(message_or_callback: types.Message, state: FSMContext):
    logging.info("Inside user_age handler")

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Меньше 18 лет", callback_data="age_less_18"))
    markup.row(InlineKeyboardButton("18-35 лет", callback_data="age_18_35"))
    markup.row(InlineKeyboardButton("Старше 35 лет", callback_data="age_more_35"))
    await message_or_callback.answer("Ваш возраст?", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data.startswith("age_"), state=Questionnaire.Age)
async def handle_age(callback_query: types.CallbackQuery, state: FSMContext):
    age_choice = callback_query.data
    await state.update_data(age=age_choice)
    await callback_query.answer(f"Вы выбрали: {age_choice}")
    await Questionnaire.VegConsumption.set()
    await veg_consumption(callback_query.message, state)


# Здесь вы можете продолжить диалог или завершить текущий этап


@dp.callback_query_handler(
    lambda c: c.data in ["age_less_18", "age_18_35", "age_more_35"],
    state=Questionnaire.Age,
)
async def veg_consumption(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Да, я ем много фруктов и овощей", callback_data="veg_yes")
    )
    markup.row(
        InlineKeyboardButton(
            "Нет, я редко употребляю фрукты и овощи", callback_data="veg_no"
        )
    )
    await message.answer(
        "Регулярно ли Вы употребляете овощи в своем ежедневном рационе?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["veg_yes", "veg_no"], state=Questionnaire.VegConsumption
)
async def fatigue_feeling(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.FatigueFeeling.set()
    await state.update_data(veg_consumption=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            "Да, я часто ощущаю усталость и истощение", callback_data="fatigue_yes"
        )
    )
    markup.row(
        InlineKeyboardButton(
            "Нет, я редко испытываю усталость и истощение", callback_data="fatigue_no"
        )
    )
    await callback_query.message.answer(
        "У вас часто возникает чувство усталости и истощения?", reply_markup=markup
    )


@dp.callback_query_handler(
    lambda c: c.data in ["fatigue_yes", "fatigue_no"],
    state=Questionnaire.FatigueFeeling,
)
async def seafood_consumption(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.SeafoodConsumption.set()
    await state.update_data(fatigue_feeling=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            "Да, я регулярно употребляю морепродукты", callback_data="seafood_yes"
        )
    )
    markup.row(
        InlineKeyboardButton(
            "Нет, я редко или почти никогда не употребляю морепродукты",
            callback_data="seafood_no",
        )
    )
    await callback_query.message.answer(
        "Ваш рацион питания включает морепродукты: рыбу и водоросли?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["seafood_yes", "seafood_no"],
    state=Questionnaire.SeafoodConsumption,
)
async def memory_issues(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.MemoryIssues.set()
    await state.update_data(seafood_consumption=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Часто", callback_data="memory_often"))
    markup.row(
        InlineKeyboardButton("Время от времени", callback_data="memory_sometimes")
    )
    markup.row(InlineKeyboardButton("Редко", callback_data="memory_rarely"))
    await callback_query.message.answer(
        "Как часто Вы замечаете, что плохо запоминаете новую информацию и имеете проблемы с памятью?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["memory_often", "memory_sometimes", "memory_rarely"],
    state=Questionnaire.MemoryIssues,
)
async def screen_time(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.ScreenTime.set()
    await state.update_data(memory_issues=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Да, часто", callback_data="screen_often"))
    markup.row(InlineKeyboardButton("Редко", callback_data="screen_rarely"))
    await callback_query.message.answer(
        "Часто ли Вы проводите время перед экранами: компьютером, смартфоном, телевизором?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["screen_often", "screen_rarely"],
    state=Questionnaire.ScreenTime,
)
async def vision_problems(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.VisionProblems.set()
    await state.update_data(screen_time=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            "Да, у меня есть проблемы со зрением", callback_data="vision_yes"
        )
    )
    markup.row(
        InlineKeyboardButton(
            "Нет, у меня нет проблем со зрением", callback_data="vision_no"
        )
    )
    await callback_query.message.answer(
        "Возникают ли у Вас проблемы со зрением, такие как пелена перед глазами, размытость или затруднения при чтении или видении на расстоянии?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["vision_yes", "vision_no"], state=Questionnaire.VisionProblems
)
async def joint_mobility(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.JointMobility.set()
    await state.update_data(vision_problems=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Да", callback_data="joints_yes"))
    markup.row(InlineKeyboardButton("Нет", callback_data="joints_no"))
    await callback_query.message.answer(
        "Чувствуете ли Вы ухудшение подвижности и гибкости в суставах?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["joints_yes", "joints_no"], state=Questionnaire.JointMobility
)
async def active_sport(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.ActiveSport.set()
    await state.update_data(joint_mobility=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Да", callback_data="sport_yes"))
    markup.row(InlineKeyboardButton("Нет", callback_data="sport_no"))
    await callback_query.message.answer(
        "Присутствует ли в Вашей жизни активный спорт?", reply_markup=markup
    )


@dp.callback_query_handler(
    lambda c: c.data in ["sport_yes", "sport_no"], state=Questionnaire.ActiveSport
)
async def numbness(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.Numbness.set()
    await state.update_data(active_sport=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Часто", callback_data="numbness_often"))
    markup.row(InlineKeyboardButton("Редко", callback_data="numbness_rarely"))
    await callback_query.message.answer(
        "Часто ли у Вас возникает онемение и покалывания в руках и ногах?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["numbness_often", "numbness_rarely"],
    state=Questionnaire.Numbness,
)
async def headaches(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.Headaches.set()
    await state.update_data(numbness=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Часто", callback_data="headaches_often"))
    markup.row(InlineKeyboardButton("Редко", callback_data="headaches_rarely"))
    await callback_query.message.answer(
        "Часто ли у Вас возникают головные боли, особенно в области затылка или лба?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["headaches_often", "headaches_rarely"],
    state=Questionnaire.Headaches,
)
async def youthfulness(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.Youthfulness.set()
    await state.update_data(headaches=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Да", callback_data="youthfulness_yes"))
    markup.row(InlineKeyboardButton("Нет", callback_data="youthfulness_no"))
    await callback_query.message.answer(
        "Важно ли Вам сохранить молодость и свежесть внешности?", reply_markup=markup
    )


@dp.callback_query_handler(
    lambda c: c.data in ["youthfulness_yes", "youthfulness_no"],
    state=Questionnaire.Youthfulness,
)
async def detox(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.Detox.set()
    await state.update_data(youthfulness=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Да", callback_data="detox_yes"))
    markup.row(InlineKeyboardButton("Нет", callback_data="detox_no"))
    await callback_query.message.answer(
        "Чувствуете ли Вы важность и необходимость на данный момент детоксикации и очищения организма?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["detox_yes", "detox_no"], state=Questionnaire.Detox
)
async def digestion(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.Digestion.set()
    await state.update_data(detox=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            "Да, у меня часто возникают проблемы с пищеварением",
            callback_data="digestion_yes",
        )
    )
    markup.row(
        InlineKeyboardButton(
            "Нет, у меня нет значительных проблем с пищеварением",
            callback_data="digestion_no",
        )
    )
    await callback_query.message.answer(
        "Часто ли у Вас возникают проблемы с пищеварением, такие как изжога, вздутие живота или запоры/поносы?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["digestion_yes", "digestion_no"], state=Questionnaire.Digestion
)
async def reproductive_support(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.ReproductiveSupport.set()
    await state.update_data(digestion=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Да", callback_data="repro_support_yes"))
    markup.row(InlineKeyboardButton("Нет", callback_data="repro_support_no"))
    await callback_query.message.answer(
        "У вас есть потребность в дополнительной поддержке здоровья женской репродуктивной системы?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["repro_support_yes", "repro_support_no"],
    state=Questionnaire.ReproductiveSupport,
)
async def beauty_enhancement(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.BeautyEnhancement.set()
    await state.update_data(repro_support=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Да", callback_data="beauty_yes"))
    markup.row(InlineKeyboardButton("Нет", callback_data="beauty_no"))
    await callback_query.message.answer(
        "У вас есть потребность в улучшении общего внешнего вида и поддержке красоты?",
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["beauty_yes", "beauty_no"],
    state=Questionnaire.BeautyEnhancement,
)
async def process_final_question(
    callback_query: types.CallbackQuery, state: FSMContext
):
    user_data = await state.get_data()
    await state.finish()

    recommended_baas = get_recommended_baas(user_data)

    await callback_query.message.answer(
        f"Спасибо за ответы! На их основе мы рекомендуем следующие БАДы: {', '.join(recommended_baas)}"
    )
