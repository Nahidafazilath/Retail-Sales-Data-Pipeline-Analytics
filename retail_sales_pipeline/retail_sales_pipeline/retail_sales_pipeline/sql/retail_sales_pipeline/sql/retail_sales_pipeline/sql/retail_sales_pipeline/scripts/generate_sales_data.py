import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

def generate_sales_data(num_records=1000, output_dir='../data/raw'):
    fake = Faker('en_US')
    products = [
        {"id": "P001", "name": "Laptop", "category": "Electronics", "price": 1200.00},
        {"id": "P002", "name": "Mouse", "category": "Electronics", "price": 25.00},
        {"id": "P003", "name": "Keyboard", "category": "Electronics", "price": 75.00},
        {"id": "P004", "name": "Desk Chair", "category": "Furniture", "price": 150.00},
        {"id": "P005", "name": "Bookshelf", "category": "Furniture", "price": 90.00},
        {"id": "P006", "name": "Coffee Maker", "category": "Appliances", "price": 50.00},
        {"id": "P007", "name": "Toaster", "category": "Appliances", "price": 30.00},
        {"id": "P008", "name": "T-Shirt", "category": "Apparel", "price": 20.00},
        {"id": "P009", "name": "Jeans", "category": "Apparel", "price": 60.00},
        {"id": "P010", "name": "Running Shoes", "category": "Footwear", "price": 80.00},
    ]
    regions = ["North", "South", "East", "West", "Central"]

    data = []
    start_date = datetime.now() - timedelta(days=30) # Last 30 days of data

    for _ in range(num_records):
        product = random.choice(products)
        quantity = random.randint(1, 5)
        sale_date = fake.date_between(start_date=start_date, end_date='now')

        data.append({
            "sale_id": fake.uuid4(),
            "transaction_date": sale_date.strftime("%Y-%m-%d"),
            "product_id": product["id"],
            "product_name": product["name"],
            "category": product["category"],
            "price": product["price"],
            "quantity": quantity,
            "customer_id": fake.uuid4(),
            "customer_name": fake.name(),
            "region": random.choice(regions)
        })

    df = pd.DataFrame(data)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save to CSV with current date in filename
    current_date_str = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"sales_data_{current_date_str}.csv")
    df.to_csv(output_file, index=False)
    print(f"Generated {num_records} sales records to {output_file}")

if __name__ == "__main__":
    generate_sales_data(num_records=random.randint(500, 1500)) # Vary daily records
