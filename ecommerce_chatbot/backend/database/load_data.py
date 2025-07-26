import pandas as pd
import os

# ✅ Path to your CSV folder
BASE_DIR = "E:/ecommerce_chatbot/csv_data"

# ✅ Define paths to each CSV file
csv_files = {
    "distribution_centers": os.path.join(BASE_DIR, "distribution_centers.csv"),
    "inventory_items": os.path.join(BASE_DIR, "inventory_items.csv"),
    "order_items": os.path.join(BASE_DIR, "order_items.csv"),
    "orders": os.path.join(BASE_DIR, "orders.csv"),
    "products": os.path.join(BASE_DIR, "products.csv"),
    "users": os.path.join(BASE_DIR, "users.csv")
}

# ✅ Load and preview each CSV
for name, path in csv_files.items():
    try:
        df = pd.read_csv(path)
        print(f"✅ Loaded '{name}' with {len(df)} rows.")
        print(df.head(2))  # preview top 2 rows
    except FileNotFoundError:
        print(f"❌ File not found: {path}")
    except Exception as e:
        print(f"⚠️ Failed to load '{name}': {e}")
