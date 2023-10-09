from text import baa_list
import random


def get_recommended_baas(user_data):
    recommended_baas = []
    age_range = user_data.get("age")
    if age_range:
        if age_range[0] == 0:
            recommended_baas.extend(["🌿IodiumKelp", "🍃Spirulina"])
        elif age_range[0] == 18:
            recommended_baas.extend(
                [
                    "🦪Squalene",
                    "🍤CardioMarine",
                    "🌿IodiumKelp",
                    "🍃Ashitaba",
                    "🥕Caroten",
                    "🍃Spirulina",
                    "🍃Chlorella",
                ]
            )
        elif age_range[0] == 35:
            recommended_baas.extend(["🍃Ashitaba", "🦪Squalene"])

    if user_data.get("veg_consumption_child") == "veg_child_yes":
        recommended_baas.extend(["🌿Zostera"])
    else:
        recommended_baas.extend(["🍃Vito Multix", "🍤Vito Fishix", "🌿IodiumKelp"])

    if user_data.get("seafood_child") == "seafood_child_yes":
        recommended_baas.extend(["🌿Zostera"])
    else:
        recommended_baas.extend(["🌿IodiumKelp", "🍤Vito Fishix"])
    
    if user_data.get("memorybad_child") == "memorybad_child_often":
        recommended_baas.extend(["🌿IodiumKelp", "🍤Vito Fishix"])
    elif user_data.get("memorybad_child") == "memorybad_child_time_to_time":
        recommended_baas.extend(["🍃Vito Multix"])
    else:
        recommended_baas.extend(["🍃Spirulina"])
    
    if user_data.get("screentime_child") == "screentime_child_often":
        recommended_baas.extend(["🥕Caroten", "🍤Vito Fishix"])
    else:
        recommended_baas.extend(["🍃Spirulina"])

    
    if user_data.get("activesport_child") == "activesport_child_yes":
        recommended_baas.extend(["🍃Spirulina", "🍃Vito Multix" ])
    else:
        recommended_baas.extend(["🍤Vito Fishix", "🌿IodiumKelp"])


    if user_data.get("parametr_child") == "parametr_child_norm":
        recommended_baas.extend(["🍃Vito Multix", "🍤Vito Fishix", "🌿IodiumKelp"])
    elif user_data.get("parametr_child") == "parametr_child_underweight":
        recommended_baas.extend(["🍃Spirulina", "🌿IodiumKelp"])
    else:
        recommended_baas.extend(["🍃Vito Multix", "🍤Vito Fishix", "🌿IodiumKelp"])

    if user_data.get("stomach_child") == "stomach_child_often":
        recommended_baas.extend(["🍃Vito Multix"])
    else:
        recommended_baas.extend(["🌿IodiumKelp", "🥕Caroten", "🦪Squalene"])





    # Рекомендации на основе остальных ответов:
    if user_data.get("veg_consumption") == "often":
        recommended_baas.append("🌿Zostera")
    elif user_data.get("veg_consumption") == "rarely":
        recommended_baas.extend(["🍃Spirulina", "🍃Ashitaba", "🌿Zostera"])

    if user_data.get("fatigue_feeling") == "often":
        recommended_baas.extend(
            [
                "🦪Squalene",
                "🍤CardioMarine",
                "🌊VitaMarine A",
                "🌊VitaMarine B",
                "🌿IodiumKelp",
            ]
        )
    elif user_data.get("fatigue_feeling") == "rarely":
        recommended_baas.extend(["🍃Ashitaba", "🥕Caroten"])

    if user_data.get("seafood_consumption") == "often":
        recommended_baas.append("🍃Ashitaba")
    elif user_data.get("seafood_consumption") == "rarely":
        recommended_baas.extend(
            [
                "🌊VitaMarine A",
                "🌊VitaMarine B",
                "🌿IodiumKelp",
                "🍃Spirulina",
                "🍃Chlorella",
                "🦪Squalene",
            ]
        )
    if user_data.get("memory_issues") == "often":
        recommended_baas.extend(["🍤CardioMarine", "🌊VitaMarine B", "🌿IodiumKelp"])
    elif user_data.get("memory_issues") == "sometimes":
        recommended_baas.extend(["🍤CardioMarine", "🌊VitaMarine B", "🌿IodiumKelp"])
    else:
        recommended_baas.extend(["🍃Spirulina", "🍃Chlorella"])

    # Проблемы со зрением:
    if user_data.get("vision_problems") == "yes":
        recommended_baas.extend(["🥕Caroten", "🌊VitaMarine B"])
    else:
        recommended_baas.append("🌿IodiumKelp")

    # Проведение времени перед экранами:
    if user_data.get("screen_time") == "often":
        recommended_baas.extend(["🥕Caroten", "🌊VitaMarine B"])
    else:
        recommended_baas.append("🍃Ashitaba")

    # Проблемы с суставами:
    if user_data.get("joint_mobility") == "yes":
        recommended_baas.extend(["🍤ArtroMarine", "🦪Squalene"])
    else:
        recommended_baas.append("🍃Chlorella")

    # Активный спорт:
    if user_data.get("active_sport") == "yes":
        recommended_baas.extend(["🍤ArtroMarine", "🍃Spirulina", "🦪Squalene"])
    else:
        recommended_baas.append("🍃Chlorella")

    # Онемение и покалывания:
    if user_data.get("numbness") == "often":
        recommended_baas.append("🍤CardioMarine")
    else:
        recommended_baas.append("🍃Chlorella")

    # Головные боли:
    if user_data.get("headaches") == "often":
        recommended_baas.extend(["🍤CardioMarine", "🌊VitaMarine A"])
    else:
        recommended_baas.append("🥕Caroten")

    # Желание сохранить молодость:
    if user_data.get("youthfulness") == "yes":
        recommended_baas.extend(["🍃Ashitaba", "🦪Squalene", "🍃Spirulina"])

    # Потребность в детоксикации:
    if user_data.get("detox") == "yes":
        recommended_baas.extend(["🍃Ashitaba", "🍃Chlorella", "🌿Zostera"])
    else:
        recommended_baas.extend(
            ["🌊VitaMarine A", "🌊VitaMarine B", "🍃Spirulina", "🌿IodiumKelp", "🥕Caroten"]
        )

    # Проблемы с пищеварением:
    if user_data.get("digestion") == "yes":
        recommended_baas.extend(["🍃Ashitaba", "🌿Zostera", "🍃Chlorella"])
    else:
        recommended_baas.extend(
            [
                "🌊VitaMarine A",
                "🌊VitaMarine B",
                "🍃Spirulina",
                "🌿IodiumKelp",
                "🥕Caroten",
                "🦪Squalene",
            ]
        )

    # Поддержка репродуктивной системы:
    if user_data.get("reproductive_support") == "repro_support_yes":
        recommended_baas.append("🌿IodiumKelp")
    else:
        recommended_baas.extend(["🍃Ashitaba", "🍃Chlorella", "🌿Zostera", "🦪Squalene"])

    # Поддержка красоты:
    if user_data.get("beauty_enhancement") == "beauty_yes":
        recommended_baas.extend(["🍤CardioMarine", "🍤ArtroMarine", "🦪Squalene"])
    else:
        recommended_baas.extend(
            ["🍃Ashitaba", "🍃Chlorella", "🍃Spirulina", "🌿IodiumKelp"]
        )

        # Поддержка мужского здоровья:
    if user_data.get("male_support") == "male_support_yes":
        recommended_baas.append(["🍤CardioMarine", "🌊VitaMarine A"])
    else:
        recommended_baas.extend(["🍃Ashitaba", "🦪Squalene"])

    # Есть ли симптомы бессоницы со стороны мужчин:
    if user_data.get("male_symptoms") == "male_symptoms_yes":
        recommended_baas.extend(["🍤CardioMarine", "🌊VitaMarine A"])
    else:
        recommended_baas.extend(["🍃Ashitaba", "🦪Squalene"])

    recommended_baas = list(set(recommended_baas))
    # Если рекомендованных бадов больше 3, выбираем рандомно 3 из них
    if len(recommended_baas) > 3:
        recommended_baas = random.sample(recommended_baas, 3)

    # Если рекомендованных бадов меньше 3, добавляем рандомные, чтобы их стало 3
    while len(recommended_baas) < 3:
        baa = random.choice(baa_list)
        if baa not in recommended_baas:
            recommended_baas.append(baa)

    return recommended_baas

