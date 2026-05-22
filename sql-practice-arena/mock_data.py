import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from database import get_connection

def clear_database(conn):
    """Drop all tables in the database to start fresh."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
    conn.commit()

def generate_ga_data():
    conn = get_connection()
    clear_database(conn)
    print("Generating Google Analytics data...")
    
    num_users, num_sessions, num_events, num_transactions = 200, 500, 2000, 150
    start_date = datetime(2023, 1, 1)
    
    # 1. ga_sessions
    user_ids = [f"user_{i:04d}" for i in range(num_users)]
    browsers = ["Chrome", "Safari", "Firefox", "Edge", "Samsung Internet"]
    device_categories = ["desktop", "mobile", "tablet"]
    os_list = ["Windows", "Macintosh", "Android", "iOS", "Linux"]
    sources = ["google", "(direct)", "facebook", "newsletter", "bing"]
    mediums = ["organic", "(none)", "cpc", "email", "referral"]
    
    sessions_data = []
    session_ids = []
    for i in range(num_sessions):
        session_id = f"sess_{i:05d}"
        session_ids.append(session_id)
        date = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        sessions_data.append({
            "session_id": session_id,
            "user_id": random.choice(user_ids),
            "session_date": date.strftime("%Y-%m-%d"),
            "session_datetime": date.strftime("%Y-%m-%d %H:%M:%S"),
            "browser": random.choice(browsers),
            "device_category": random.choice(device_categories),
            "operating_system": random.choice(os_list),
            "source": random.choice(sources),
            "medium": random.choice(mediums),
            "pageviews": random.randint(1, 15)
        })
    df_sessions = pd.DataFrame(sessions_data)
    
    # 2. ga_events
    event_names = ["page_view", "scroll", "view_item", "add_to_cart", "begin_checkout", "purchase"]
    events_data = []
    for i in range(num_events):
        session_id = random.choice(session_ids)
        session_row = df_sessions[df_sessions['session_id'] == session_id].iloc[0]
        base_time = datetime.strptime(session_row['session_datetime'], "%Y-%m-%d %H:%M:%S")
        event_time = base_time + timedelta(minutes=random.randint(0, 30))
        events_data.append({
            "event_id": f"evt_{i:05d}",
            "session_id": session_id,
            "event_name": random.choice(event_names),
            "event_timestamp": event_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    df_events = pd.DataFrame(events_data)
    
    # 3. transactions
    transaction_sessions = random.sample(session_ids, num_transactions)
    products = ["T-Shirt", "Jeans", "Sneakers", "Hat", "Socks"]
    transactions_data = []
    for i, session_id in enumerate(transaction_sessions):
        session_row = df_sessions[df_sessions['session_id'] == session_id].iloc[0]
        revenue = round(random.uniform(20.0, 500.0), 2)
        transactions_data.append({
            "transaction_id": f"txn_{i:04d}",
            "session_id": session_id,
            "user_id": session_row['user_id'],
            "transaction_date": session_row['session_date'],
            "revenue": revenue,
            "product_name": random.choice(products),
            "quantity": random.randint(1, 5)
        })
    df_transactions = pd.DataFrame(transactions_data)
    
    df_sessions.to_sql('ga_sessions', conn, index=False)
    df_events.to_sql('ga_events', conn, index=False)
    df_transactions.to_sql('transactions', conn, index=False)
    conn.close()

def generate_retail_data():
    conn = get_connection()
    clear_database(conn)
    print("Generating Retail E-commerce data...")
    
    # 1. customers
    customers = []
    for i in range(1, 101):
        customers.append({
            "customer_id": f"CUST_{i:03d}",
            "customer_name": f"User {i}",
            "grade": random.choice(["Bronze", "Silver", "Gold", "VIP"]),
            "join_date": (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        })
    df_customers = pd.DataFrame(customers)
    
    # 2. products
    products = []
    for i in range(1, 21):
        products.append({
            "product_id": f"P_{i:03d}",
            "product_name": f"Product {i}",
            "price": random.randint(10, 200) * 10,
            "category": random.choice(["Electronics", "Clothing", "Home", "Sports"])
        })
    df_products = pd.DataFrame(products)
    
    # 3. orders and order_items
    orders = []
    order_items = []
    item_id_counter = 1
    
    for i in range(1, 301):
        order_id = f"ORD_{i:04d}"
        orders.append({
            "order_id": order_id,
            "customer_id": random.choice(customers)["customer_id"],
            "order_date": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d")
        })
        
        # 1 to 4 items per order
        for _ in range(random.randint(1, 4)):
            prod = random.choice(products)
            order_items.append({
                "item_id": item_id_counter,
                "order_id": order_id,
                "product_id": prod["product_id"],
                "quantity": random.randint(1, 3),
                "price": prod["price"]
            })
            item_id_counter += 1
            
    df_orders = pd.DataFrame(orders)
    df_order_items = pd.DataFrame(order_items)
    
    df_customers.to_sql('customers', conn, index=False)
    df_products.to_sql('products', conn, index=False)
    df_orders.to_sql('orders', conn, index=False)
    df_order_items.to_sql('order_items', conn, index=False)
    conn.close()

def generate_finance_data():
    conn = get_connection()
    clear_database(conn)
    print("Generating Finance data...")
    
    # 1. customers
    customers = []
    for i in range(1, 101):
        customers.append({
            "customer_id": f"CUST_{i:03d}",
            "customer_name": f"Client {i}",
            "credit_score": random.randint(500, 850)
        })
    df_customers = pd.DataFrame(customers)
    
    # 2. accounts
    accounts = []
    for i in range(1, 151):
        accounts.append({
            "account_id": f"ACC_{i:04d}",
            "customer_id": random.choice(customers)["customer_id"],
            "account_type": random.choice(["SAVINGS", "CHECKING"]),
            "balance": round(random.uniform(100.0, 50000.0), 2)
        })
    df_accounts = pd.DataFrame(accounts)
    
    # 3. transactions
    transactions = []
    for i in range(1, 501):
        acc = random.choice(accounts)
        ttype = random.choice(["DEPOSIT", "WITHDRAWAL", "TRANSFER"])
        amount = round(random.uniform(10.0, 2000.0), 2)
        
        # create an anomaly occasionally
        if random.random() < 0.05 and ttype == 'WITHDRAWAL':
            amount = acc["balance"] + random.randint(100, 1000)
            
        transactions.append({
            "transaction_id": f"TXN_{i:05d}",
            "account_id": acc["account_id"],
            "transaction_type": ttype,
            "amount": amount,
            "transaction_date": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 180))).strftime("%Y-%m-%d %H:%M:%S")
        })
    df_transactions = pd.DataFrame(transactions)
    
    # 4. loans
    loans = []
    for i in range(1, 41):
        loans.append({
            "loan_id": f"LN_{i:03d}",
            "customer_id": random.choice(customers)["customer_id"],
            "loan_amount": round(random.uniform(5000.0, 100000.0), 2),
            "interest_rate": round(random.uniform(2.5, 8.5), 2)
        })
    df_loans = pd.DataFrame(loans)
    
    df_customers.to_sql('customers', conn, index=False)
    df_accounts.to_sql('accounts', conn, index=False)
    df_transactions.to_sql('transactions', conn, index=False)
    df_loans.to_sql('loans', conn, index=False)
    conn.close()

def generate_streaming_data():
    conn = get_connection()
    clear_database(conn)
    print("Generating Streaming / Content Platform data...")
    
    # 1. users
    users = []
    for i in range(1, 201):
        users.append({
            "user_id": f"U_{i:04d}",
            "email": f"user{i}@example.com",
            "username": f"User_{i}",
            "country": random.choice(["US", "KR", "JP", "UK", "CA", "FR"]),
            "joined_at": (datetime(2022, 1, 1) + timedelta(days=random.randint(0, 500))).strftime("%Y-%m-%d"),
            "plan_type": random.choice(["free", "basic", "premium"])
        })
    df_users = pd.DataFrame(users)
    
    # 2. content
    content = []
    genres = ["Action", "Comedy", "Drama", "Sci-Fi", "Romance", "Documentary", "Thriller"]
    for i in range(1, 101):
        ctype = random.choice(["movie", "series"])
        dur = random.randint(80, 150) if ctype == "movie" else random.randint(20, 60)
        content.append({
            "content_id": f"C_{i:04d}",
            "title": f"Title {i}",
            "genre": random.choice(genres),
            "type": ctype,
            "release_year": random.randint(2010, 2024),
            "duration_min": dur,
            "rating": round(random.uniform(2.5, 9.8), 1)
        })
    df_content = pd.DataFrame(content)
    
    # 3. subscriptions
    subscriptions = []
    for i in range(1, 301):
        u = random.choice(users)
        start_d = datetime.strptime(u["joined_at"], "%Y-%m-%d") + timedelta(days=random.randint(0, 30))
        dur_days = random.choice([30, 90, 365])
        end_d = start_d + timedelta(days=dur_days)
        
        stat = "active"
        if end_d < datetime.now():
            stat = "expired"
        elif random.random() < 0.2:
            stat = "cancelled"
            
        subscriptions.append({
            "sub_id": f"S_{i:04d}",
            "user_id": u["user_id"],
            "plan": u["plan_type"],
            "start_date": start_d.strftime("%Y-%m-%d"),
            "end_date": end_d.strftime("%Y-%m-%d"),
            "status": stat
        })
    df_subscriptions = pd.DataFrame(subscriptions)
    
    # 4. watch_history
    watch_history = []
    for i in range(1, 1001):
        u = random.choice(users)
        c = random.choice(content)
        w_time = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        dur_sec = c["duration_min"] * 60
        if random.random() > 0.4:
            watched_sec = dur_sec
            completed = True
        else:
            watched_sec = random.randint(60, dur_sec)
            completed = False
            if watched_sec >= dur_sec * 0.9:
                completed = True
                
        watch_history.append({
            "watch_id": f"W_{i:05d}",
            "user_id": u["user_id"],
            "content_id": c["content_id"],
            "watched_at": w_time.strftime("%Y-%m-%d %H:%M:%S"),
            "watched_sec": watched_sec,
            "completed": completed
        })
    df_watch_history = pd.DataFrame(watch_history)
    
    # 5. reviews
    reviews = []
    for i in range(1, 301):
        u = random.choice(users)
        c = random.choice(content)
        r_time = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        reviews.append({
            "review_id": f"R_{i:04d}",
            "user_id": u["user_id"],
            "content_id": c["content_id"],
            "score": random.randint(1, 5),
            "comment": "Sample comment",
            "created_at": r_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    df_reviews = pd.DataFrame(reviews)
    
    df_users.to_sql('users', conn, index=False)
    df_content.to_sql('content', conn, index=False)
    df_subscriptions.to_sql('subscriptions', conn, index=False)
    df_watch_history.to_sql('watch_history', conn, index=False)
    df_reviews.to_sql('reviews', conn, index=False)
    conn.close()
