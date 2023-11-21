import asyncpg
import os
from docs import generate_and_upload
import logging
import json
from utils import question_mapping, child_mapping, answer_mapping, child_answer_mapping, gender_mapping


async def create_pool():
    # DATABASE_URL = os.environ.get("DATABASE_URL")
    # return await asyncpg.create_pool(DATABASE_URL, ssl="require")
        return await asyncpg.create_pool(
        user="postgres",
        password="1234",
        database="postgres",
        host="localhost",
    )


async def create_table(conn):
    await conn.execute(
        """
    CREATE TABLE IF NOT EXISTS mains_users_special (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone_number VARCHAR(40),
        gender VARCHAR(50),
        age VARCHAR(30),
        child_answers JSONB,  
        answers JSONB,
        recommendations JSONB
    );
    """
    )


def transform_answers(answers):
    readable_answers = {}
    readable_child_answers = {}
    for key, value in answers.items():
        
        if key in question_mapping:
            question = question_mapping[key]
            answer = answer_mapping[value]
            readable_answers[question] = answer
        
        
        elif key in child_mapping:
            child_qs = child_mapping[key]
            child_an = child_answer_mapping[value]
            readable_child_answers[child_qs] = child_an
        
        
        else:
            print(f"Warning: key {key} not found in either mapping.")
        
    return readable_answers, readable_child_answers



async def save_user_data(
    conn, user_id, name, phone_number, gender, age, child_answers, answers, recommendations
):
    logging.info(f"Saving data for user {user_id}...")
    gender = gender_mapping.get(gender, "Неизвестно")
    readable_answers, readable_child_answers = transform_answers(answers)
    all_answers = {**readable_answers, **readable_child_answers}
    json_child_answers = json.dumps(child_answers)
    json_answers = json.dumps(all_answers)
    json_recommendations = json.dumps(recommendations)


    if not phone_number:
        logging.warning("Phone number is missing.")
        phone_number = None 

    try:
        result = await conn.execute(
            """
            INSERT INTO mains_users_special (user_id, name, phone_number, gender, age, child_answers, answers, recommendations)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (user_id) DO UPDATE
            SET name = EXCLUDED.name,
                phone_number = EXCLUDED.phone_number,
                gender = EXCLUDED.gender,
                age = EXCLUDED.age,
                child_answers = EXCLUDED.child_answers,    
                answers = EXCLUDED.answers,
                recommendations = EXCLUDED.recommendations;
            """,
            user_id,
            name,
            phone_number,  
            gender,
            age,
            json_child_answers,
            json_answers,
            json_recommendations,
        )
        logging.info(f"Query result: {result}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    # Данные для генерации документа DOCX
    data = {
        "user_id": user_id,
        "name": name,
        "phone_number": phone_number,  
        "gender": gender,
        "age": age,
        "child_answers": readable_child_answers,
        "answers": readable_answers,
        "recommendations": recommendations,
    }

    generate_and_upload(data)


async def get_user_data(conn, user_id):
    return await conn.fetchrow("SELECT * FROM mains_users_special WHERE user_id = $1;", user_id)
