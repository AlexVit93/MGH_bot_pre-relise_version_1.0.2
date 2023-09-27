import asyncpg
from docs import generate_and_upload
import logging
import json
from utils import question_mapping, answer_mapping


async def create_pool():
    return await asyncpg.create_pool(
        PGUSER="postgres",
        PGPASSWORD="kWt0XEdOQ90Bs18Dj8Ip",
        PGDATABASE="railway",
        PGHOST="containers-us-west-79.railway.app",
    )


async def create_table(conn):
    await conn.execute(
        """
    CREATE TABLE IF NOT EXISTS new_users (
        user_id SERIAL PRIMARY KEY,
        phone_number BIGINT,
        name VARCHAR(100),
        age VARCHAR(30),
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
    conn, user_id, phone_number, name, age, answers, recommendations
):
    logging.info(f"Saving data for user {user_id}...")
    readable_answers = transform_answers(answers)
    json_answers = json.dumps(readable_answers)
    json_recommendations = json.dumps(recommendations)

    # Преобразование номера телефона из строки в число
    try:
        phone_number = int(phone_number)
    except ValueError:
        logging.error(f"Invalid phone number format: {phone_number}")
        return

    try:
        result = await conn.execute(
            """
            INSERT INTO new_users (user_id, phone_number, name, age, answers, recommendations)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (user_id) DO UPDATE
            SET phone_number = EXCLUDED.phone_number,
                name = EXCLUDED.name,
                age = EXCLUDED.age,
                answers = EXCLUDED.answers,
                recommendations = EXCLUDED.recommendations;
            """,
            user_id,
            phone_number,
            name,
            age,
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
        "answers": readable_answers,
        "recommendations": recommendations,
    }

    generate_and_upload(data)


async def get_user_data(conn, user_id):
    return await conn.fetchrow("SELECT * FROM new_users WHERE user_id = $1;", user_id)
