import asyncpg
from docs import generate_and_upload


async def create_pool():
    return await asyncpg.create_pool(
        user="root",
        password="1234",
        database="your_database",
        host="localhost",
    )


async def create_table(conn):
    await conn.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        phone_number VARCHAR(20),
        name VARCHAR(100),
        answers JSONB,
        recommendations JSONB
    );
    """
    )


async def save_user_data(conn, user_id, phone_number, name, answers, recommendations):
    await conn.execute(
        """
        INSERT INTO users (user_id, phone_number, name, answers, recommendations) VALUES ($1, $2, $3)
        ON CONFLICT (id) DO UPDATE
        SET answers = $2, recommendations = $3;
    """,
        user_id,
        phone_number,
        name,
        answers,
        recommendations,
    )
    data = {
        "user_id": user_id,
        "name": name,
        "phone_number": phone_number,
        "answers": answers,
        "recommendations": recommendations,
    }

    generate_and_upload(data)


async def get_user_data(conn, user_id):
    return await conn.fetchrow("SELECT * FROM users WHERE id = $1;", user_id)
