from questions import question_pack, child_questions
from kb import buttons, child_buttons

question_mapping = {
    "veg_consumption": question_pack["q_1"],
    "fatigue_feeling": question_pack["q_2"],
    "seafood_consumption": question_pack["q_3"],
    "memory_issues": question_pack["q_4"],
    "screen_time": question_pack["q_5"],
    "vision_problems": question_pack["q_6"],
    "joint_mobility": question_pack["q_7"],
    "active_sport": question_pack["q_8"],
    "numbness": question_pack["q_9"],
    "headaches": question_pack["q_10"],
    "youthfulness": question_pack["q_11"],
    "detox": question_pack["q_12"],
    "digestion": question_pack["q_13"],
    "reproductive_support": question_pack["q_14"],
    "beauty_enhancement": question_pack["q_15"],
    "male_support": question_pack["q_16"],
    "male_symptoms": question_pack["q_17"],
    "conscious_response": question_pack["q_18"],
    "ready_response": question_pack["q_19"],
}

child_mapping = {
    "veg_consumption_child": child_questions["q_1"],
    "seafood_child": child_questions["q_2"],
    "memorybad_child": child_questions["q_3"],
    "screentime_child": child_questions["q_4"],
    "activesport_child": child_questions["q_5"],
    "parametr_child": child_questions["q_6"],
    "stomach_child": child_questions["q_7"],
}

gender_mapping = {
    "male": "Мужчина",
    "female": "Женщина",
}

child_answer_mapping = {button.callback_data: button.text for _, button in child_buttons.items()}
answer_mapping = {button.callback_data: button.text for _, button in buttons.items()}
