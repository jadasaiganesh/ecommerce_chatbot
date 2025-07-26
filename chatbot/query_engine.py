from .utils import get_dataframe
import pandas as pd


def handle_query(intent, entities):
        if intent == "track_order":
            return track_order_status(entities)
        
        elif intent == "product_info":
            return get_product_details(entities)
        
        elif intent == "user_info":
            return get_user_details(entities)
        elif intent == "inventory_check":
            return get_inventory_count(entities)
        elif intent == "top_selling_products":
            return get_top_selling_products()
        elif intent == "top_users_by_city":
            return get_top_users_by_city(entities)
        elif intent == "list_distribution_centers":
            return list_distribution_centers()


        else:
            return "🤖 Sorry, I couldn't understand that request."

def get_top_selling_products():
        order_items_df = get_dataframe('order_items')
        products_df = get_dataframe('products')

        if order_items_df is None or products_df is None:
            return "⚠️ Order or product data not available."

        # Step 1: Count product_id frequencies
        top_counts = (
            order_items_df['product_id']
            .value_counts()
            .head(5)
            .reset_index()
        )
        top_counts.columns = ['product_id', 'sold_count']

        # Step 2: Merge with product details
        top_products = top_counts.merge(products_df, left_on='product_id', right_on='id', how='left')

        # Step 3: Build response
        response_lines = ["🏆 Top 5 Best-Selling Products:"]
        for i, row in top_products.iterrows():
            name = row['name'] if pd.notna(row['name']) else "Unknown"
            brand = row['brand'] if pd.notna(row['brand']) else "Unknown"
            count = row['sold_count']
            response_lines.append(f"{i+1}. {name} ({brand}) — Sold: {count}")

        return "\n".join(response_lines)


    # -----------------------------------
def track_order_status(entities):
        import pandas as pd  # ✅ Ensure pandas is imported

        order_id = entities.get('order_id')
        if not order_id:
            return "❗ Please provide a valid order ID."
        
        orders_df = get_dataframe('orders')
        result = orders_df[orders_df['order_id'] == int(order_id)]
        
        if not result.empty:
            order = result.iloc[0]
            status = order['status']
            shipped_at = order['shipped_at']
            delivered_at = order['delivered_at']
            returned_at = order['returned_at']

            response = f"📦 Order #{order_id} is currently '{status}'."

            if pd.notna(shipped_at):
                response += f" It was shipped on {shipped_at.strftime('%Y-%m-%d')}."
            if pd.notna(delivered_at):
                response += f" Delivered on {delivered_at.strftime('%Y-%m-%d')}."
            if pd.notna(returned_at):
                response += f" Returned on {returned_at.strftime('%Y-%m-%d')}."

            return response
        else:
            return f"❌ No order found with ID #{order_id}."


    # -----------------------------------
def get_product_details(entities):
        product_name = entities.get('product_name')
        if not product_name:
            return "❗ Please specify a product name."

        products_df = get_dataframe('products')
        result = products_df[products_df['name'].str.lower().str.contains(product_name.lower(), na=False)]

        if not result.empty:
            product = result.iloc[0]
            return f"🧥 {product['name']} from {product['brand']} (₹{product['retail_price']}) is available in {product['department']} department."
        else:
            return f"❌ No product found matching '{product_name}'."

    # -----------------------------------
def get_user_details(entities):
        order_id = entities.get('order_id')
        if not order_id:
            return "❗ Please provide a valid order ID."

        orders_df = get_dataframe('orders')
        users_df = get_dataframe('users')
        
        order = orders_df[orders_df['order_id'] == int(order_id)]
        if not order.empty:
            user_id = order.iloc[0]['user_id']
            user = users_df[users_df['id'] == user_id]
            if not user.empty:
                user = user.iloc[0]
                return f"👤 User: {user['first_name']} {user['last_name']} from {user['city']}, {user['state']}. Email: {user['email']}."
        return f"❌ No user found for order #{order_id}."


import re

def normalize(text):
    # Lowercase, remove symbols, numbers, extra spaces
    return re.sub(r'[^a-zA-Z\s]', '', text).strip().lower()

def get_inventory_count(entities):
    product_name = entities.get('product_name')
    if not product_name:
        return "❗ Please specify a product name to check inventory."

    inventory_df = get_dataframe('inventory_items')
    if inventory_df is None:
        return "⚠️ Inventory data not loaded."

    # Normalize the user input
    normalized_input = normalize(product_name)

    # Create a normalized column in inventory for comparison
    inventory_df['normalized_name'] = inventory_df['product_name'].apply(lambda x: normalize(str(x)))

    # Match rows where normalized names contain the normalized input
    matching = inventory_df[inventory_df['normalized_name'].str.contains(normalized_input, na=False)]

    if 'sold_at' not in matching.columns:
        return "⚠️ Inventory data missing 'sold_at' field."

    unsold = matching[matching['sold_at'].isna()]
    count = unsold.shape[0]

    if count > 0:
        return f"🧮 We have {count} unsold units of '{product_name}' in stock."
    elif not matching.empty:
        return f"❌ '{product_name}' is currently out of stock."
    else:
        return f"❓ Product '{product_name}' not found in inventory."


def get_top_users_by_city(entities):
    city = entities.get('city')
    if not city:
        return "❗ Please specify a city name."

    orders_df = get_dataframe('orders')
    users_df = get_dataframe('users')

    # Merge orders with users
    merged_df = orders_df.merge(users_df, left_on='user_id', right_on='id', how='inner')

    # Filter by city (case-insensitive)
    filtered_df = merged_df[merged_df['city'].str.lower() == city.lower()]

    if filtered_df.empty:
        return f"❌ No users found from {city}."

    # Get top 5 user IDs with most orders
    top_users = (
    filtered_df['user_id']
    .value_counts()
    .head(5)
    .reset_index(name='order_count')  # ✅ keeps 'user_id' as column and adds 'order_count'
)


    # Merge back to get user info
    top_users = top_users.merge(users_df, left_on='user_id', right_on='id')

    # Build the response
    response = [f"📍 Top 5 users from {city} who ordered most:"]
    for i, row in top_users.iterrows():
        name = f"{row['first_name']} {row['last_name']}"
        count = row['order_count']
        response.append(f"{i+1}. {name} — {count} orders")

    return "\n".join(response)


def list_distribution_centers():
    df = get_dataframe('distribution_centers')
    if df is None or df.empty:
        return "⚠️ Distribution center data is not available."

    response_lines = ["🏢 List of Distribution Centers:"]
    for i, row in df.iterrows():
        name = row.get('name', 'Unknown')
        lat = row.get('latitude', 'N/A')
        lon = row.get('longitude', 'N/A')
        response_lines.append(f"{i+1}. {name} (Lat: {lat}, Lon: {lon})")

    return "\n".join(response_lines)
