"""
generate_data.py
Generates a realistic synthetic Superstore-style sales dataset.
Run once to create data/sales.csv (5,000+ rows).
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N_ROWS = 6000

# --- Reference lists -------------------------------------------------
regions = ["East", "West", "Central", "South"]
states_by_region = {
    "East": ["New York", "New Jersey", "Pennsylvania", "Massachusetts"],
    "West": ["California", "Washington", "Oregon", "Nevada"],
    "Central": ["Texas", "Illinois", "Ohio", "Michigan"],
    "South": ["Florida", "Georgia", "North Carolina", "Tennessee"],
}
segments = ["Consumer", "Corporate", "Home Office"]
categories = {
    "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
    "Office Supplies": ["Binders", "Paper", "Storage", "Art", "Labels"],
    "Technology": ["Phones", "Machines", "Accessories", "Copiers"],
}
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]
payment_modes = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery"]

product_names = {
    "Chairs": ["Executive Chair", "Mesh Task Chair", "Ergo Chair", "Folding Chair"],
    "Tables": ["Conference Table", "Study Table", "Round Table", "Standing Desk"],
    "Bookcases": ["Oak Bookcase", "Metal Bookcase", "Corner Bookcase"],
    "Furnishings": ["Desk Lamp", "Wall Clock", "Cushion", "Photo Frame"],
    "Binders": ["Ring Binder", "View Binder", "Clip Binder"],
    "Paper": ["A4 Paper Ream", "Sticky Notes", "Printer Paper"],
    "Storage": ["File Cabinet", "Storage Box", "Shelf Unit"],
    "Art": ["Marker Set", "Sketch Pad", "Color Pencils"],
    "Labels": ["Label Maker", "Label Roll"],
    "Phones": ["Smartphone X1", "Smartphone Lite", "Cordless Phone"],
    "Machines": ["Laptop Pro", "Desktop PC", "3D Printer"],
    "Accessories": ["Wireless Mouse", "Keyboard", "USB Hub", "Webcam"],
    "Copiers": ["Office Copier", "Portable Scanner"],
}

customer_first = ["Aarav", "Isha", "Rohan", "Meera", "Karan", "Diya", "Aditya", "Neha",
                   "Vivaan", "Ananya", "Kabir", "Sara", "Arjun", "Priya", "Dev", "Tara",
                   "Reyansh", "Zara", "Ishaan", "Kiara"]
customer_last = ["Sharma", "Verma", "Patel", "Reddy", "Nair", "Gupta", "Iyer", "Khan",
                  "Singh", "Rao", "Mehta", "Joshi", "Kapoor", "Das", "Chawla"]

start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
date_range_days = (end_date - start_date).days

# --- Generate rows -----------------------------------------------------
rows = []
for i in range(1, N_ROWS + 1):
    order_id = f"ORD-{10000 + i}"
    order_date = start_date + timedelta(days=int(np.random.randint(0, date_range_days)))
    ship_delay = np.random.randint(1, 8)
    ship_date = order_date + timedelta(days=int(ship_delay))

    region = np.random.choice(regions)
    state = np.random.choice(states_by_region[region])
    segment = np.random.choice(segments, p=[0.55, 0.3, 0.15])

    category = np.random.choice(list(categories.keys()), p=[0.25, 0.45, 0.30])
    sub_category = np.random.choice(categories[category])
    product_name = np.random.choice(product_names[sub_category])

    customer_name = f"{np.random.choice(customer_first)} {np.random.choice(customer_last)}"
    customer_id = f"CUST-{hash(customer_name) % 900 + 100}"

    quantity = np.random.randint(1, 12)

    # base unit price varies by category
    base_price = {
        "Furniture": np.random.uniform(80, 900),
        "Office Supplies": np.random.uniform(5, 120),
        "Technology": np.random.uniform(50, 1500),
    }[category]

    discount = np.random.choice([0, 0.1, 0.15, 0.2, 0.3, 0.4], p=[0.35, 0.2, 0.15, 0.15, 0.1, 0.05])
    sales = round(base_price * quantity * (1 - discount), 2)

    # profit margin logic: higher discount tends to squeeze / hurt profit
    base_margin = np.random.uniform(0.05, 0.35)
    margin = base_margin - (discount * 0.6)
    profit = round(sales * margin, 2)

    ship_mode = np.random.choice(ship_modes, p=[0.6, 0.2, 0.15, 0.05])
    payment_mode = np.random.choice(payment_modes)

    rows.append([
        order_id, order_date.date(), ship_date.date(), ship_mode,
        customer_id, customer_name, segment,
        region, state, category, sub_category, product_name,
        sales, quantity, discount, profit, payment_mode
    ])

df = pd.DataFrame(rows, columns=[
    "Order ID", "Order Date", "Ship Date", "Ship Mode",
    "Customer ID", "Customer Name", "Segment",
    "Region", "State", "Category", "Sub-Category", "Product Name",
    "Sales", "Quantity", "Discount", "Profit", "Payment Mode"
])

df.to_csv("data/sales.csv", index=False)
print(f"Generated {len(df)} rows -> data/sales.csv")
