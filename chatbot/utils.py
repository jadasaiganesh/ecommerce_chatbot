import pandas as pd
import os

# ✅ Updated path to where your CSVs are stored
BASE_DIR = os.path.join('E:/ecommerce_chatbot', 'csv_data')  # Put your CSVs in this folder

dataframes = {}

def load_csv_files():
    global dataframes
    try:
        dataframes['distribution_centers'] = pd.read_csv(os.path.join(BASE_DIR, 'distribution_centers.csv'))
        dataframes['inventory_items'] = pd.read_csv(os.path.join(BASE_DIR, 'inventory_items.csv'))
        dataframes['order_items'] = pd.read_csv(os.path.join(BASE_DIR, 'order_items.csv'))
        dataframes['orders'] = pd.read_csv(os.path.join(BASE_DIR, 'orders.csv'))
        dataframes['products'] = pd.read_csv(os.path.join(BASE_DIR, 'products.csv'))
        dataframes['users'] = pd.read_csv(os.path.join(BASE_DIR, 'users.csv'))
        print("✅ All CSVs loaded successfully!")
    except Exception as e:
        print("❌ Error loading CSVs:", e)

def get_dataframe(name):
    return dataframes.get(name)
