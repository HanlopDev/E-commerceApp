import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


class Setting:
    TITLE = "E-CommerceApp"
    VERSION = "0.0.1"
    DESCRIPTION = """
        #This the Project for learning fastAPI by creating 
        E-Commerce webApp
    """
    NAME = "Developer"
    EMAIL = "hanlopb@gmail.com"

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "mydb")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    TEST_EMAIL = "user2@exxample.com"
    TEST_PASS = "user2"
    TEST_ITEM = "item1"
    TEST_ITEM_DESC = "test item"

setting = Setting()

