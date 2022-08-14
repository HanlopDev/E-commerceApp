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
    SECURITY_KEY = os.getenv("SECURITY_KEY")
    ALGORITHM = "HS256"

setting = Setting()

