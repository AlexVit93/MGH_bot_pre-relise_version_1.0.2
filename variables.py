from text import baa_list
from main import *
from handlers import *
from states import *
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
                    "🌊VitaMarine A",
                    "🌊VitaMarine B",
                    "🌿IodiumKelp",
                    "🍃Ashitaba",
                    "🥕Caroten",
                    "🍃Spirulina",
                    "🍃Chlorella",
                ]
            )
        elif age_range[0] == 35:
            recommended_baas.extend(["🍃Ashitaba", "🦪Squalene"])

    # Рекомендации на основе остальных ответов:
    if user_data.get("vegetable_intake") == "often":
        recommended_baas.append("🌿Zostera")
    elif user_data.get("vegetable_intake") == "rarely":
        recommended_baas.extend(["🍃Spirulina", "🍃Ashitaba", "🌿Zostera"])

    if user_data.get("fatigue") == "often":
        recommended_baas.extend(
            [
                "🦪Squalene",
                "🍤CardioMarine",
                "🌊VitaMarine A",
                "🌊VitaMarine B",
                "🌿IodiumKelp",
            ]
        )
    elif user_data.get("fatigue") == "rarely":
        recommended_baas.extend(["🍃Ashitaba", "🥕Caroten"])

    if user_data.get("seafood") == "often":
        recommended_baas.append("🍃Ashitaba")
    elif user_data.get("seafood") == "rarely":
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
    if user_data.get("vision_issues") == "yes":
        recommended_baas.extend(["🥕Caroten", "🌊VitaMarine B"])
    else:
        recommended_baas.append("🌿IodiumKelp")

    # Проведение времени перед экранами:
    if user_data.get("screen_time") == "often":
        recommended_baas.extend(["🥕Caroten", "🌊VitaMarine B"])
    else:
        recommended_baas.append("🍃Ashitaba")

    # Проблемы с суставами:
    if user_data.get("joint_issues") == "yes":
        recommended_baas.extend(["🍤ArtroMarine", "🦪Squalene"])
    else:
        recommended_baas.append("🍃Chlorella")

    # Активный спорт:
    if user_data.get("active_sport") == "yes":
        recommended_baas.extend(["🍤ArtroMarine", "🍃Spirulina", "🦪Squalene"])
    else:
        recommended_baas.append("🍃Chlorella")

    # Онемение и покалывания:
    if user_data.get("numbness_tingling") == "often":
        recommended_baas.append("🍤CardioMarine")
    else:
        recommended_baas.append("🍃Chlorella")

    # Головные боли:
    if user_data.get("headaches") == "often":
        recommended_baas.extend(["🍤CardioMarine", "🌊VitaMarine A"])
    else:
        recommended_baas.append("🥕Caroten")

    # Желание сохранить молодость:
    if user_data.get("youth_importance") == "yes":
        recommended_baas.extend(
            ["🍃Ashitaba", "🌊VitaMarine A", "🌊VitaMarine B", "🍃Spirulina"]
        )

    # Потребность в детоксикации:
    if user_data.get("detox_need") == "yes":
        recommended_baas.extend(["🍃Ashitaba", "🍃Chlorella", "🌿Zostera"])
    else:
        recommended_baas.extend(
            ["🌊VitaMarine A", "🌊VitaMarine B", "🍃Spirulina", "🌿IodiumKelp", "🥕Caroten"]
        )

    # Проблемы с пищеварением:
    if user_data.get("digestion_issues") == "yes":
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
    if user_data.get("repro_support") == "repro_support_yes":
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
