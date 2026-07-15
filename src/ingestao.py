import pandas as pd
from config import RAW

def carregar_csv(nome_arquivo):
    return pd.read_csv(RAW / nome_arquivo)