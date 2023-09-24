from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp
from main import logging
from states import Questionnaire
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from variables import get_recommended_baas
from questions import question_pack
from kb import buttons
from db import save_user_data

# from utils import question_mapping, answer_mapping


@dp.message_handler(lambda message: message.text == "Начать", state="*")
@dp.message_handler(commands="start", state="*")
async def user_name(message: types.Message):
    await Questionnaire.Name.set()
    await message.answer("Ваше имя?")


@dp.message_handler(state=Questionnaire.Name)
async def phone(message: types.Message, state: FSMContext):
    await Questionnaire.Phone.set()
    await state.update_data(name=message.text)
    await message.answer(
        "Приятно познакомиться! Введите ваш контактный номер телефона, пожалуйста."
    )


@dp.message_handler(state=Questionnaire.Phone)
async def handle_phone(message: types.Message, state: FSMContext):
    phone_number = message.text

    await state.update_data(phone_number=phone_number)

    await message.answer("Спасибо, получил ваш номер!")
    await Questionnaire.Age.set()
    await user_age(message, state)


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
    # await callback_query.answer(f"Вы выбрали: {age_choice}")
    await Questionnaire.VegConsumption.set()
    await veg_consumption(callback_query.message, state)


@dp.callback_query_handler(
    lambda c: c.data in ["age_less_18", "age_18_35", "age_more_35"],
    state=Questionnaire.Age,
)
async def veg_consumption(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup()
    markup.row(buttons["veg_yes"], buttons["veg_no"])
    question_text = question_pack.get("q_1", "Вопрос не найден")
    await message.answer(
        question_text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["veg_yes", "veg_no"], state=Questionnaire.VegConsumption
)
async def fatigue_feeling(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.FatigueFeeling.set()
    # await state.update_data(veg_consumption=callback_query.data)
    await state.update_data(answers={"veg_consumption": callback_query.data})
    markup = InlineKeyboardMarkup()
    markup.row(buttons["fatigue_yes"], buttons["fatigue_no"])
    question_text = question_pack.get("q_2", "Вопрос не найден")
    await callback_query.message.answer(question_text, reply_markup=markup)


@dp.callback_query_handler(
    lambda c: c.data in ["fatigue_yes", "fatigue_no"],
    state=Questionnaire.FatigueFeeling,
)
async def seafood_consumption(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.SeafoodConsumption.set()
    await state.update_data(fatigue_feeling=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(buttons["seafood_yes"], buttons["seafood_no"])
    question_text = question_pack.get("q_3", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
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
    markup.row(
        buttons["memory_often"], buttons["memory_sometimes"], buttons["memory_rarely"]
    )
    question_text = question_pack.get("q_4", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
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
    markup.row(buttons["screen_often"], buttons["screen_rarely"])
    question_text = question_pack.get("q_5", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
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
    markup.row(buttons["vision_yes"], buttons["vision_no"])
    question_text = question_pack.get("q_6", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["vision_yes", "vision_no"], state=Questionnaire.VisionProblems
)
async def joint_mobility(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.JointMobility.set()
    await state.update_data(vision_problems=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(buttons["joints_yes"], buttons["joints_no"])
    question_text = question_pack.get("q_7", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["joints_yes", "joints_no"], state=Questionnaire.JointMobility
)
async def active_sport(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.ActiveSport.set()
    await state.update_data(joint_mobility=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(buttons["sport_yes"], buttons["sport_no"])
    question_text = question_pack.get("q_8", "Вопрос не найден")
    await callback_query.message.answer(question_text, reply_markup=markup)


@dp.callback_query_handler(
    lambda c: c.data in ["sport_yes", "sport_no"], state=Questionnaire.ActiveSport
)
async def numbness(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.Numbness.set()
    await state.update_data(active_sport=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(buttons["numbness_often"], buttons["numbness_rarely"])
    question_text = question_pack.get("q_9", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
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
    markup.row(buttons["headaches_often"], buttons["headaches_rarely"])
    question_text = question_pack.get("q_10", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
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
    markup.row(buttons["youthfulness_yes"], buttons["youthfulness_no"])
    question_text = question_pack.get("q_11", "Вопрос не найден")
    await callback_query.message.answer(question_text, reply_markup=markup)


@dp.callback_query_handler(
    lambda c: c.data in ["youthfulness_yes", "youthfulness_no"],
    state=Questionnaire.Youthfulness,
)
async def detox(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.Detox.set()
    await state.update_data(youthfulness=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(buttons["detox_yes"], buttons["detox_no"])
    question_text = question_pack.get("q_12", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["detox_yes", "detox_no"], state=Questionnaire.Detox
)
async def digestion(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.Digestion.set()
    await state.update_data(detox=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(buttons["digestion_yes"], buttons["digestion_no"])
    question_text = question_pack.get("q_13", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["digestion_yes", "digestion_no"], state=Questionnaire.Digestion
)
async def reproductive_support(callback_query: types.CallbackQuery, state: FSMContext):
    await Questionnaire.ReproductiveSupport.set()
    await state.update_data(digestion=callback_query.data)
    markup = InlineKeyboardMarkup()
    markup.row(buttons["repro_support_yes"], buttons["repro_support_no"])
    question_text = question_pack.get("q_14", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
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
    markup.row(buttons["beauty_yes"], buttons["beauty_no"])
    question_text = question_pack.get("q_15", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
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

    recommended_baas = get_recommended_baas(user_data)

    user_id = callback_query.from_user.id

    # Добавьте запись в базу данных. Вызовите функцию save_user_data здесь.
    async with dp["db_pool"].acquire() as conn:
        await save_user_data(
            conn,
            user_id,
            user_data.get("phone_number"),
            user_data.get("name"),
            user_data.get("age"),
            user_data.get("answers"),
            user_data.get("recommendations"),
        )

    await state.finish()

    await callback_query.message.answer(
        f"Спасибо за ответы! На их основе мы рекомендуем следующие БАДы: {', '.join(recommended_baas)}"
    )
