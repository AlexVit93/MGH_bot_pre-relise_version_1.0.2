import asyncpg
from docs import generate_and_upload
import logging
import json


async def create_pool():
    return await asyncpg.create_pool(
        user="postgres",
        password="1234",
        database="special_users",
        host="localhost",
    )


async def create_table(conn):
    await conn.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        phone_number JSONB,
        name VARCHAR(100),
        age INTEGER,
        answers JSONB,
        recommendations JSONB
    );
    """
    )


async def save_user_data(
    conn, user_id, phone_number, name, age, answers, recommendations
):
    logging.info(f"Saving data for user {user_id}...")
    json_answers = json.dumps(answers)
    json_recommendations = json.dumps(recommendations)
    try:
        result = await conn.execute(
            """
            INSERT INTO users (user_id, phone_number, name, age, answers, recommendations)
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
        "answers": answers,
        "recommendations": recommendations,
    }

    generate_and_upload(data)


async def get_user_data(conn, user_id):
    return await conn.fetchrow("SELECT * FROM users WHERE user_id = $1;", user_id)
