from questions import question_pack
from kb import buttons

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
    "repro_support": question_pack["q_14"],
    "beauty_enhancement": question_pack["q_15"],
}

answer_mapping = {button.callback_data: button.text for _, button in buttons.items()}
