from dotenv import load_dotenv
from os import getenv


load_dotenv()


BOT_TOKEN = getenv('BOT_TOKEN')
ADMIN_ID = int(getenv('ADMIN_ID'))
POSTGRES_HOST = getenv('POSTGRES_HOST')
POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_DB = getenv('POSTGRES_DB')

DB_URL=f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
ALEMBIC_DB_URL=f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
