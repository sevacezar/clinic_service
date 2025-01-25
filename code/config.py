"""Module with app configuration"""

import os

from dotenv import load_dotenv


dotenv_path: str = os.path.join(os.path.dirname(__file__), '../.env')


if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    raise FileNotFoundError(f'File with environment variables {dotenv_path} is not found')


DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

JWT_SECRET: str = os.getenv('JWT_SECRET')
JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')
EXPIRES_DELTA_DAYS: int = int(os.getenv('EXPIRES_DELTA_DAYS'))
