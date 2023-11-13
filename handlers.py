import ast
from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp, logging
from states import Questionnaire
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from variables import get_recommended_baas
from questions import question_pack, child_questions
from kb import buttons, child_buttons, restart_and_view_kb
from db import save_user_data, get_user_data
from spec_rec import middle_and_old, youngest


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
        "Приятно познакомиться! Предоставьте ваш контактный номер, пожалуйста",   reply_markup=markup)


@dp.message_handler(content_types=["contact"], state=Questionnaire.Phone)
async def handle_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    user_data = await state.get_data()
    logging.info(f"Phone number saved in state: {user_data['phone_number']}")
    await message.answer("Спасибо, получил ваш номер!", reply_markup=ReplyKeyboardRemove())
    await Questionnaire.Gender.set()
    await user_gender(message, state)



@dp.message_handler(state=Questionnaire.Gender)
async def user_gender(message_or_callback: types.Message, state: FSMContext):
    logging.info("Inside user_gender handler")

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Мужчина", callback_data="male"))
    markup.row(InlineKeyboardButton("Женщина", callback_data="female"))    
    await message_or_callback.answer("Ваш пол?", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data in ["male", "female"], state=Questionnaire.Gender)
async def handle_gender(callback_query: types.CallbackQuery, state: FSMContext):
    gender_choice = callback_query.data
    await state.update_data(gender=gender_choice)
    
    await Questionnaire.Age.set()
    await user_age(callback_query.message, state)


@dp.message_handler(state=Questionnaire.Age)
async def user_age(message_or_callback: types.Message, state: FSMContext):
    logging.info("Inside user_age handler")

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Меньше 18 лет", callback_data="age_less_18"))
    markup.row(InlineKeyboardButton("18-35 лет", callback_data="age_18_35"))
    markup.row(InlineKeyboardButton("Старше 35 лет", callback_data="age_more_35"))
    
    await message_or_callback.answer("Ваш возраст?", reply_markup=markup)


# Вопросы исключительно для детей

@dp.callback_query_handler(
    lambda c: c.data in ["age_less_18"], state=Questionnaire.Age
)
async def handle_child(callback_query: types.CallbackQuery, state: FSMContext):
    age_less_18_choice = callback_query.data
    await state.update_data(age=age_less_18_choice)
    await Questionnaire.VegConsumptionChild.set()
    await veg_consumption_child(callback_query, state)

async def veg_consumption_child(callback_query: types.CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup()
    markup.row(child_buttons["veg_child_yes"], child_buttons["veg_child_no"])
    question_child_text = child_questions.get("q_1", "Вопрос не найден")
    await callback_query.message.answer(
        question_child_text,
        reply_markup=markup,
    )

@dp.callback_query_handler(
    lambda c: c.data in ["veg_child_yes", "veg_child_no"], state=Questionnaire.VegConsumptionChild
)
async def seafood_child(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"veg_consumption_child": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.SeafoodConsumptionChild.set()
    markup = InlineKeyboardMarkup()
    markup.row(child_buttons["seafood_child_yes"], child_buttons["seafood_child_no"])
    question_child_text = child_questions.get("q_2", "Вопрос не найден")
    await callback_query.message.answer(question_child_text, reply_markup=markup)


@dp.callback_query_handler(
    lambda c: c.data in ["seafood_child_yes", "seafood_child_no"],
    state=Questionnaire.SeafoodConsumptionChild,
)
async def memorybad_child(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"seafood_child": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.MemoryIssuesChild.set()
    markup = InlineKeyboardMarkup()
    markup.row(child_buttons["memorybad_child_often"], child_buttons["memorybad_child_time_to_time"], child_buttons["memorybad_child_rarely"])
    question_child_text = child_questions.get("q_3", "Вопрос не найден")
    await callback_query.message.answer(
        question_child_text,
        reply_markup=markup,
    )

@dp.callback_query_handler(
    lambda c: c.data in ["memorybad_child_often", "memorybad_child_time_to_time", "memorybad_child_rarely"],
    state=Questionnaire.MemoryIssuesChild,
)
async def screentime_child(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"memorybad_child": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.ScreenTimeChild.set()
    markup = InlineKeyboardMarkup()
    markup.row(child_buttons["screentime_child_often"], child_buttons["screentime_child_rarely"])
    question_child_text = child_questions.get("q_4", "Вопрос не найден")
    await callback_query.message.answer(
        question_child_text,
        reply_markup=markup,
    )


@dp.callback_query_handler(
    lambda c: c.data in ["screentime_child_often", "screentime_child_rarely"],
    state=Questionnaire.ScreenTimeChild,
)
async def activesport_child(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"screentime_child": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.ActiveSportChild.set()
    markup = InlineKeyboardMarkup()
    markup.row(child_buttons["activesport_child_yes"], child_buttons["activesport_child_no"])
    question_child_text = child_questions.get("q_5", "Вопрос не найден")
    await callback_query.message.answer(
        question_child_text,
        reply_markup=markup,
    )

@dp.callback_query_handler(
    lambda c: c.data in ["activesport_child_yes", "activesport_child_no"],
    state=Questionnaire.ActiveSportChild,
)
async def parametr_child(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"activesport_child": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.ParametrChild.set()
    markup = InlineKeyboardMarkup()
    markup.row(child_buttons["parametr_child_norm"], child_buttons["parametr_child_underweight"], child_buttons["parametr_child_overweight"])
    question_child_text = child_questions.get("q_6", "Вопрос не найден")
    await callback_query.message.answer(
        question_child_text,
        reply_markup=markup,
    )

@dp.callback_query_handler(
    lambda c: c.data in ["parametr_child_norm", "parametr_child_underweight", "parametr_child_overweight"],
    state=Questionnaire.ParametrChild,
)
async def stomach_child(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"parametr_child": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.StomachChild.set()
    markup = InlineKeyboardMarkup()
    markup.row(child_buttons["stomach_child_often"], child_buttons["stomach_child_rarely"])
    question_child_text = child_questions.get("q_7", "Вопрос не найден")
    await callback_query.message.answer(
        question_child_text,
        reply_markup=markup,
    )

@dp.callback_query_handler(
    lambda c: c.data in ["stomach_child_often", "stomach_child_rarely"],
    state=Questionnaire.StomachChild,
)
async def child_conscious_response(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"stomach_child": callback_query.data}) 
    await state.update_data(answers=current_answers)
    await Questionnaire.ConsciousResponse.set()
    markup = InlineKeyboardMarkup()
    markup.row(buttons["conscious_yes"], buttons["conscious_no"])
    question_text = question_pack.get("q_18", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )

# Вопросы для взрослых

@dp.callback_query_handler(lambda c: c.data.startswith("age_"), state=Questionnaire.Age)
async def handle_age(callback_query: types.CallbackQuery, state: FSMContext):
    age_choice = callback_query.data
    await state.update_data(age=age_choice)
    await Questionnaire.VegConsumption.set()
    await veg_consumption(callback_query, state)


async def veg_consumption(callback_query: types.CallbackQuery, state: FSMContext):
    markup = InlineKeyboardMarkup()
    markup.row(buttons["veg_yes"], buttons["veg_no"])
    question_text = question_pack.get("q_1", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )

@dp.callback_query_handler(
    lambda c: c.data in ["veg_yes", "veg_no"], state=Questionnaire.VegConsumption
)
async def fatigue_feeling(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"veg_consumption": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.FatigueFeeling.set()
    markup = InlineKeyboardMarkup()
    markup.row(buttons["fatigue_yes"], buttons["fatigue_no"])
    question_text = question_pack.get("q_2", "Вопрос не найден")
    await callback_query.message.answer(question_text, reply_markup=markup)


@dp.callback_query_handler(
    lambda c: c.data in ["fatigue_yes", "fatigue_no"],
    state=Questionnaire.FatigueFeeling,
)
async def seafood_consumption(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"fatigue_feeling": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.SeafoodConsumption.set()
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
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"seafood_consumption": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.MemoryIssues.set()
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
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"memory_issues": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.ScreenTime.set()
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
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"screen_time": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.VisionProblems.set()
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
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"vision_problems": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.JointMobility.set()
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
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"joint_mobility": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.ActiveSport.set()
    markup = InlineKeyboardMarkup()
    markup.row(buttons["sport_yes"], buttons["sport_no"])
    question_text = question_pack.get("q_8", "Вопрос не найден")
    await callback_query.message.answer(question_text, reply_markup=markup)

@dp.callback_query_handler(
    lambda c: c.data in ["sport_yes", "sport_no"], state=Questionnaire.ActiveSport
)
async def numbness(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"active_sport": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.Numbness.set()
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
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"numbness": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.Headaches.set()
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
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"headaches": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.Youthfulness.set()
    markup = InlineKeyboardMarkup()
    markup.row(buttons["youthfulness_yes"], buttons["youthfulness_no"])
    question_text = question_pack.get("q_11", "Вопрос не найден")
    await callback_query.message.answer(question_text, reply_markup=markup)

@dp.callback_query_handler(
    lambda c: c.data in ["youthfulness_yes", "youthfulness_no"],
    state=Questionnaire.Youthfulness,
)
async def detox(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"youthfulness": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.Detox.set()
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
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"detox": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.Digestion.set()
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
async def transition_to_gender_specific_question(
    callback_query: types.CallbackQuery, state: FSMContext
):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"digestion": callback_query.data})
    await state.update_data(answers=current_answers)
    user_gender = current_data.get("gender")
    if user_gender == "male":
        await Questionnaire.MaleSupport.set()
        markup = InlineKeyboardMarkup()
        markup.row(buttons["male_support_yes"], buttons["male_support_no"])
        question_text = question_pack.get("q_16", "Вопрос не найден")
    elif user_gender == "female":
        await Questionnaire.ReproductiveSupport.set()
        markup = InlineKeyboardMarkup()
        markup.row(buttons["repro_support_yes"], buttons["repro_support_no"])
        question_text = question_pack.get("q_14", "Вопрос не найден")
    else:
        await callback_query.message.answer(
            "Произошла ошибка, попробуйте начать заново."
        )
        return  
    
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )

async def male_support(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"digestion": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.MaleSupport.set()
    markup = InlineKeyboardMarkup()
    markup.row(buttons["male_support_yes"], buttons["male_support_no"])
    question_text = question_pack.get("q_16", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )

@dp.callback_query_handler(
    lambda c: c.data in ["male_support_yes", "male_support_no"],
    state=Questionnaire.MaleSupport,
)
async def male_symptoms(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"male_support": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.MaleSymptoms.set()
    markup = InlineKeyboardMarkup()
    markup.row(buttons["male_symptoms_yes"], buttons["male_symptoms_no"])
    question_text = question_pack.get("q_17", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )

@dp.callback_query_handler(
    lambda c: c.data in ["male_symptoms_yes", "male_symptoms_no"],
    state=Questionnaire.MaleSymptoms,
)
async def man_conscious_response(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"male_symptoms": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.ConsciousResponse.set()
    markup = InlineKeyboardMarkup()
    markup.row(buttons["conscious_yes"], buttons["conscious_no"])
    question_text = question_pack.get("q_18", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )

async def reproductive_support(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"digestion": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.ReproductiveSupport.set()
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
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"reproductive_support": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.BeautyEnhancement.set()
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
async def woman_conscious_response(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"beauty_enhancement": callback_query.data}) 
    await state.update_data(answers=current_answers)
    await Questionnaire.ConsciousResponse.set()
    markup = InlineKeyboardMarkup()
    markup.row(buttons["conscious_yes"], buttons["conscious_no"])
    question_text = question_pack.get("q_18", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )

@dp.callback_query_handler(
    lambda c: c.data in ["conscious_yes", "conscious_no"],
    state=Questionnaire.ConsciousResponse,
)
async def ready_response(callback_query: types.CallbackQuery, state: FSMContext):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"conscious_response": callback_query.data})
    await state.update_data(answers=current_answers)
    await Questionnaire.ReadyResponse.set()
    markup = InlineKeyboardMarkup()
    markup.row(buttons["ready_yes"], buttons["ready_no"])
    question_text = question_pack.get("q_19", "Вопрос не найден")
    await callback_query.message.answer(
        question_text,
        reply_markup=markup,
    )

@dp.callback_query_handler(
    lambda c: c.data in ["ready_yes", "ready_no"],
    state=Questionnaire.ReadyResponse,
)
async def process_final_question(
    callback_query: types.CallbackQuery, state: FSMContext
):
    current_data = await state.get_data()
    current_answers = current_data.get("answers", {})
    current_answers.update({"ready_response": callback_query.data})
    await state.update_data(answers=current_answers)

    await callback_query.message.answer(
        "Ваши ответы обрабатываются, нам нужно буквально 10-15 секунд или менее..."
    )

    user_data = await state.get_data()
    logging.info(f"Data to be saved: {user_data}")
    recommended_baas = get_recommended_baas(user_data)
    user_id = callback_query.from_user.id

    async with dp["db_pool"].acquire() as conn:
        await save_user_data(
            conn,
            user_id,
            user_data.get("name"),
            user_data.get("phone_number"),
            user_data.get("gender"),
            user_data.get("age"),
            user_data.get("child_answers"),
            user_data.get("answers"),
            recommended_baas,
        )

    message_final = "Спасибо за ответы! На их основе мы рекомендуем следующие БАДы: \n{}".format(',\n'.join(recommended_baas))
    await callback_query.message.answer(message_final)

    # Рекомендации по возрасту
    user_age = user_data.get("age")
    if user_age == "age_less_18":
        await callback_query.message.answer('\n\n'.join(youngest.values()))
    elif user_age in ["age_18_35", "age_more_35"]:
        await callback_query.message.answer('\n\n'.join(middle_and_old.values()))


    await state.finish()

    await callback_query.message.answer(
        "Если желаете перезапустить опрос - нажмите на кнопку \"Перезапуск\", если желаете посмотреть ваши рекомендации - нажмите на кнопку \"Мои БАДы\".",
        reply_markup=restart_and_view_kb,
    )

@dp.callback_query_handler(lambda c: c.data == "restart_bot")
async def restart_bot(callback_query: types.CallbackQuery):
    await callback_query.answer(callback_query.id)
    await user_name(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == "view_recommendations")
async def view_recommendations(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    async with dp["db_pool"].acquire() as conn:
        user_data = await get_user_data(conn, user_id)
    if user_data and user_data.get("recommendations"):
        recommendations_list = ast.literal_eval(user_data['recommendations'])
        recommendations_text = ",\n".join(recommendations_list)
        await callback_query.message.answer(f"Ваши последние рекомендации:\n{recommendations_text}")
    else:
        await callback_query.message.answer(
            "У вас пока нет никаких рекомендаций, нажмите /start и пройдите опрос!"
        )
    await callback_query.answer(callback_query.id)
