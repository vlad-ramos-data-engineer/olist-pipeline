from pathlib import Path
from dotenv import load_dotenv
import os


RAIZ = Path(__file__).resolve().parent
RAW = RAIZ / 'data' / 'raw'
PROCESSED = RAIZ / 'data' / 'processed'

load_dotenv()
        
DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = os.getenv("DB_PORT")
DB_NAME     = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"        


if __name__ == "__main__":
    if RAW.exists():
        print("--- Conteúdo da pasta RAW ---")
        for item in RAW.iterdir():
            print(item.name)
    else:
        print("Tá faltando coisa aqui!")