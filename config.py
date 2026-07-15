from pathlib import Path

RAIZ = Path(__file__).resolve().parent
RAW = RAIZ / 'data' / 'raw'
PROCESSED = RAIZ / 'data' / 'processed'


if __name__ == "__main__":
    if RAW.exists():
        print("--- Conteúdo da pasta RAW ---")
        for item in RAW.iterdir():
            print(item.name)
    else:
        print("Tá faltando coisa aqui!")