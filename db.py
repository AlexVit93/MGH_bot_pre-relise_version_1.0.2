import asyncpg
import os
from docs import generate_and_upload
import logging
import json
from utils import question_mapping, answer_mapping


async def create_pool():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    return await asyncpg.create_pool(DATABASE_URL, ssl="require")


async def create_table(conn):
    await conn.execute(
        """
    CREATE TABLE IF NOT EXISTS new_users (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone_number BIGINT,
        age VARCHAR(30),
        gender VARCHAR(50),  
        answers JSONB,
        recommendations JSONB
    );
    """
    )


def transform_answers(answers):
    readable_answers = {}
    for key, value in answers.items():
        question = question_mapping[key]
        answer = answer_mapping[value]
        readable_answers[question] = answer
    return readable_answers


async def save_user_data(
    conn, user_id, name, phone_number, age, gender, answers, recommendations
):
    logging.info(f"Saving data for user {user_id}...")
    readable_answers = transform_answers(answers)
    json_answers = json.dumps(readable_answers)
    json_recommendations = json.dumps(recommendations)

    try:
        phone_number = int(phone_number)
    except ValueError:
        logging.error(f"Invalid phone number format: {phone_number}")
        return

    try:
        result = await conn.execute(
            """
            INSERT INTO new_users (user_id, name, phone_number, age, gender, answers, recommendations)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (user_id) DO UPDATE
            SET name = EXCLUDED.name,
                phone_number = EXCLUDED.phone_number,
                age = EXCLUDED.age,
                gender = EXCLUDED.gender,  
                answers = EXCLUDED.answers,
                recommendations = EXCLUDED.recommendations;
            """,
            user_id,
            name,
            phone_number,
            age,
            gender,
            json_answers,
            json_recommendations,
        )
        logging.info(f"Query result: {result}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    data = {
        "user_id": user_id,
        "name": name,
        "phone_number": phone_number,
        "age": age,
        "gender": gender,
        "answers": readable_answers,
        "recommendations": recommendations,
    }

    generate_and_upload(data)


async def get_user_data(conn, user_id):
    return await conn.fetchrow("SELECT * FROM new_users WHERE user_id = $1;", user_id)
