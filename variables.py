from text import baa_list, child_baa_list
import random

def get_recommended_baas(user_data):
    recommended_baas = []

    # Берем возрастной диапазон
    age_range = user_data.get("age")
    age_baa_mapping = {
        "age_less_18": ["🌿IodiumKelp", "🍃Spirulina"],
        "age_18_35": ["🦈Squalene", "❤️CardioMarine", "🌿IodiumKelp", "🍃Ashitaba", "🥕Caroten", "🍃Spirulina",
    "🍃Chlorella", "🦴ArtroMarine"],
        "age_more_35": ["🍃Ashitaba", "🦈Squalene", "❤️CardioMarine"]
    }
    recommended_baas.extend(age_baa_mapping.get(age_range, []))

    # Рекомендации на основе ответов для детей
    child_answers_mapping = {
        "veg_consumption_child": {
            "veg_child_yes": ["🥕Caroten"],
            "veg_child_no": ["🍃Spirulina"]
        },
        "seafood_child": {
            "seafood_child_no": ["🌿IodiumKelp"]
        },
        "memorybad_child": {
            "memorybad_child_often": ["🌿IodiumKelp"],
            "memorybad_child_time_to_time": ["🌿IodiumKelp"],
            "memorybad_child_no": ["🍃Spirulina"]
        },
        "screentime_child": {
            "screentime_child_often": ["🥕Caroten"],
            "screentime_child_no": ["🍃Spirulina"]
        },
        "activesport_child": {
            "activesport_child_yes": ["🍃Spirulina"],
            "activesport_child_no": ["🌿IodiumKelp"]
        },
        "parametr_child": {
            "parametr_child_norm": ["🌿IodiumKelp"],
            "parametr_child_underweight": ["🍃Spirulina", "🌿IodiumKelp"],
            "parametr_child_overweight": ["🌿IodiumKelp"]
        },
        "stomach_child": {
            "stomach_child_often": ["🌿IodiumKelp"],
            "stomach_child_no": ["🌿IodiumKelp", "🥕Caroten"]
        }
    }

    for question, answers in child_answers_mapping.items():
        answer = user_data.get(question)
        recommended_baas.extend(answers.get(answer, []))

    # Рекомендации на основе остальных взрослых ответов
    adult_answers_mapping = {
        "veg_consumption": {
            "often": ["🌿Zostera"],
            "rarely": ["🍃Spirulina", "🍃Ashitaba", "🌿Zostera"]
        },
        "fatigue_feeling": {
            "often": ["🦈Squalene", "❤️CardioMarine", "🌿IodiumKelp"],
            "rarely": ["🍃Ashitaba", "🥕Caroten"]
        },
	    "seafood_consumption": {
            "often": ["🍃Ashitaba"],
            "rarely": ["🌊VitaMarine A", "🌊VitaMarine B", "🌿IodiumKelp", "🍃Spirulina", "🍃Chlorella",
            "🦈Squalene"]
        },
	    "memory_issues":{
            "often": ["❤️CardioMarine", "🌿IodiumKelp"],
            "sometimes": ["❤️CardioMarine", "🌊VitaMarine B", "🌿IodiumKelp"],
            "rarely": ["🍃Spirulina", "🍃Chlorella"]
        },
	    "vision_problems":{
            "yes": ["🥕Caroten", "🌊VitaMarine B"],
            "no": ["🌿IodiumKelp", "🦴ArtroMarine"]
        },
	    "screen_time":{
            "often": ["🥕Caroten", "🌊VitaMarine B"],
            "rarely": ["🍃Ashitaba"]

        },
	    "joint_mobility":{
            "yes": ["🦴ArtroMarine", "🦈Squalene"],
            "no": ["🍃Chlorella"]
        },
	    "active_sport":{
            "yes": ["🦴ArtroMarine", "🍃Spirulina", "🦈Squalene"],
            "no": ["🍃Chlorella"]
        },
	    "numbness":{
            "often": ["❤️CardioMarine"],
            "rarely": ["❤️CardioMarine", "🍃Chlorella", "🌿IodiumKelp"]
        },
	    "headaches":{
            "often": ["❤️CardioMarine", "🌊VitaMarine A"],
            "rarely": ["🌿IodiumKelp", "🦈Squalene", "🥕Caroten"]
        },
	    "youthfulness":{
            "yes": ["🍃Ashitaba", "🌊VitaMarine A", "🍃Spirulina","🦈Squalene"],
            "no": ["🍃Ashitaba"]
        },
	    "detox":{
            "yes": ["🍃Ashitaba", "🍃Chlorella", "🌿Zostera"],
            "no": ["🍃Spirulina", "🌿IodiumKelp", "🥕Caroten"]
        },
	    "digestion":{
            "yes": ["🍃Ashitaba", "🌿Zostera", "🍃Chlorella"],
            "no": ["🌊VitaMarine A", "🌊VitaMarine B",
                "🍃Spirulina", "🌿IodiumKelp",
                "🥕Caroten", "🦈Squalene"]
        },
	    "reproductive_support":{
            "repro_support_yes": ["🌿IodiumKelp"],
            "repro_support_no": ["🍃Ashitaba", "🍃Chlorella", "🌿Zostera", "🦈Squalene"]
        },
	    "beauty_enhancement":{
            "beauty_yes": ["❤️CardioMarine", "🦈Squalene"],
            "beauty_no": ["🍃Ashitaba", "🍃Chlorella", "🍃Spirulina", "🌿IodiumKelp"]
        },
	    "male_support":{
            "male_support_yes":["❤️CardioMarine", "🌊VitaMarine A"],
            "male_support_no": ["🍃Ashitaba", "🦈Squalene"]
        },
	    "male_symptoms":{
            "male_symptoms_yes": ["❤️CardioMarine", "🌊VitaMarine A"],
            "male_symptoms_no": ["🍃Ashitaba", "🦈Squalene"]
        }

    }

    for question, answers in adult_answers_mapping.items():
        answer = user_data.get(question)
        recommended_baas.extend(answers.get(answer, []))

    # Убираем дубликаты
    recommended_baas = list(set(recommended_baas))

    # Выбираем рандомно 3 рекомендованных бада, если их больше 3
    if len(recommended_baas) > 3:
        recommended_baas = random.sample(recommended_baas, 3)

    # Если рекомендованных бадов меньше 3, добавляем рандомные, чтобы их стало 3
    while len(recommended_baas) < 3:
        baa = random.choice(baa_list)
        if baa not in recommended_baas:
            recommended_baas.append(baa)

    return recommended_baas