import pandas as pd
from src.ingestao import carregar_csv

orders = carregar_csv('olist_orders_dataset.csv')
reviews = carregar_csv('olist_order_reviews_dataset.csv')


def limpar_orders(orders):
    
    """ função para limpar a tabela orders"""
    orders = orders.copy()
    orders['dt_entrega'] = pd.to_datetime(orders['order_delivered_customer_date'], errors='coerce')
    assert orders['dt_entrega'].isna().sum() == orders['order_delivered_customer_date'].isna().sum(), "Valores nulos indevidos na coluna dt_entrega"
    orders['dt_compra'] = pd.to_datetime(orders['order_purchase_timestamp'], errors='coerce')
    assert orders['dt_compra'].isna().sum() == orders['order_purchase_timestamp'].isna().sum(), "valores nulos indevidos na coluna dt_compra"
    delivered = orders[(orders['order_status'] == 'delivered')].copy()
    entregues_cln = delivered[delivered['dt_entrega'].notna()].copy()
    assert len(delivered) - len(entregues_cln) == 8, "valores nulos inesperados na coluna dt_entrega"
    entregues_cln = entregues_cln[['order_id', 'dt_compra', 'dt_entrega']]
       
    return entregues_cln
   
def limpar_reviews(reviews):
    
    """ função para limpar tabela reviews"""
    reviews = reviews.copy() 
    reviews['dt_review'] = pd.to_datetime(reviews['review_answer_timestamp'], errors='coerce')
    assert reviews['dt_review'].isna().sum() == 0, "valores nulos indevidos na coluna dt_review"  
    uniq = reviews.sort_values('dt_review', ascending=True).copy()
    uniq = uniq.drop_duplicates(subset='order_id', keep='last')
    assert len(uniq) == reviews['order_id'].nunique(), "Valores de order_id duplicados detectados"
    reviews_cln = uniq[['review_id', 'order_id', 'review_score', 'dt_review']].copy()
    
    return reviews_cln     
   
   
   
# testa todo o script: carregar e limpar ambos os arquivos
if __name__ == "__main__":
    print("orders", orders.shape)
    print("reviews", reviews.shape)
    
    orders_limpo = limpar_orders(orders)     
    print("orders_limpo:", orders_limpo.shape)
    print(orders_limpo.head())
    print(orders_limpo.dtypes)
    
    reviews_limpo = limpar_reviews(reviews)
    print("reviews_limpo:", reviews_limpo.shape)
    print(reviews_limpo.head())
    print(reviews_limpo.dtypes)



