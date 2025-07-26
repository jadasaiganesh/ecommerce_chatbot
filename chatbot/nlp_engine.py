import re
def extract_intent_and_entities(query):
    query = query.lower()
    intent = "unknown"
    entities = {}

    # ✅ 1. Top Selling Products - check FIRST
    if "top" in query and "sold" in query:
        intent = "top_selling_products"
        return intent, entities

    # 2. Track Order
    if "where is my order" in query or "track order" in query or "status of order" in query:
        intent = "track_order"
        order_id = extract_order_id(query)
        if order_id:
            entities['order_id'] = order_id

    # 3. User Info
    elif "user details" in query or "who placed order" in query:
        intent = "user_info"
        order_id = extract_order_id(query)
        if order_id:
            entities['order_id'] = order_id

    # 4. Inventory Check
    elif "how many" in query and "left" in query:
        intent = "inventory_check"
        product_name = extract_product_name(query)
        if product_name:
            entities['product_name'] = product_name

    # 5. Product Info - moved to last
    elif "show me" in query or "product" in query or "details of" in query:
        intent = "product_info"
        product_name = extract_product_name(query)
        if product_name:
            entities['product_name'] = product_name

    return intent, entities



def extract_order_id(query):
    match = re.search(r"(?:#)?(\d{4,10})", query)
    return match.group(1) if match else None

def extract_product_name(query):
    # Remove only start and end phrases, not product names in the middle
    query = query.lower()

    # Remove starter/ending noise phrases
    patterns = [
        r"how many", r"are left", r"left in stock", r"do you have",
        r"show me", r"give me", r"details of", r"please", r"\?"
    ]

    for pattern in patterns:
        query = re.sub(pattern, '', query)

    # Final trim
    return query.strip().title()  # Title-case for better matching



import re

def extract_intent_and_entities(query):
    query_lower = query.lower()

    # Track order
    if "track" in query_lower or "status of order" in query_lower:
        match = re.search(r'\b\d{5,}\b', query)
        order_id = match.group() if match else None
        return "track_order", {"order_id": order_id}
    
    # Product info
    elif "show me details of" in query_lower or "info about" in query_lower:
        product_match = re.search(r"details of (.+)", query_lower)
        return "product_info", {"product_name": product_match.group(1).strip() if product_match else None}
    
    # Top users by city
    elif "top" in query_lower and "users" in query_lower and "order" in query_lower:
        city_match = re.search(r'from ([a-zA-Z\s]+)', query_lower)
        return "top_users_by_city", {"city": city_match.group(1).strip() if city_match else None}
    
    # Add more intent handlers as needed...

    return "unknown", {}
