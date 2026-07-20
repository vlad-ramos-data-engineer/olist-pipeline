
from config import engine
from src.ingestao import carregar_csv
from src.limpeza import limpar_orders, limpar_reviews
from sqlalchemy import text

if __name__ == "__main__":
    # 1. produzir os frames 
    orders_limpo  = limpar_orders(carregar_csv('olist_orders_dataset.csv'))
    reviews_limpo = limpar_reviews(carregar_csv('olist_order_reviews_dataset.csv'))

    # 2. alinhar reviews ao escopo de orders (mata as órfãs antes da carga)
    mascara = reviews_limpo['order_id'].isin(orders_limpo['order_id'])
    reviews_alinhado = reviews_limpo[mascara]
    
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE reviews, orders"))
        conn.commit()
    
    # 3. carregar
    orders_limpo.to_sql('orders', engine, if_exists='append', index=False)
    reviews_alinhado.to_sql('reviews', engine, if_exists='append', index=False)
    
    # 4. QA pelo pandas
    with engine.connect() as conn:
        n_orders  = conn.execute(text("SELECT COUNT(*) FROM orders")).scalar()
        n_reviews = conn.execute(text("SELECT COUNT(*) FROM reviews")).scalar()

    assert n_orders == len(orders_limpo), f"orders: esperado {len(orders_limpo)}, veio {n_orders}"
    assert n_reviews == len(reviews_alinhado), f"reviews: esperado {len(reviews_alinhado)}, veio {n_reviews}"
    print(f"✓ carga validada: orders={n_orders}, reviews={n_reviews}")
    
    # 5. QA pelo SQL
    with engine.connect() as conn:
        orfas = conn.execute(text("""
            SELECT COUNT(*)
            FROM reviews r
            LEFT JOIN orders o ON r.order_id = o.order_id
            WHERE o.order_id IS NULL
        """)).scalar()

    assert orfas == 0, f"integridade quebrada: {orfas} reviews órfãs no banco"
    print(f"✓ integridade validada: {orfas} órfãs")