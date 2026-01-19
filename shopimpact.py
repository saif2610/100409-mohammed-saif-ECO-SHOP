# =========================================================
# 🌍 ECO SHOP IMPACT — FULL CLEAN & PREMIUM VERSION
# Exam-Ready • Cart Enabled • Impact Visualized
# =========================================================

import streamlit as st
import time
import math
import pandas as pd
import matplotlib.pyplot as plt
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="EcoShop Impact",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# GLOBAL CSS (UNCHANGED)
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0fdf4, #ecfeff);
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 { color: #064e3b; font-weight: 700; }
.card {
    background: white;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    transition: 0.3s ease;
    text-align:center;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 18px 35px rgba(0,0,0,0.15);
}
.category-card {
    background: linear-gradient(135deg, #ecfeff, #f0fdf4);
    border-radius: 20px;
    padding: 35px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
.earth-box {
    background: radial-gradient(circle at center, #0ea5e9, #020617);
    border-radius: 50%;
    width: 260px;
    height: 260px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 40px rgba(14,165,233,0.7);
}
.footer {
    text-align: center;
    font-size: 13px;
    color: #6b7280;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "selected_product" not in st.session_state:
    st.session_state.selected_product = None
if "cart" not in st.session_state:
    st.session_state.cart = []

# -----------------------------
# ECO TIPS
# -----------------------------
ECO_TIPS = [
    "🌱 Buying durable products reduces waste.",
    "♻️ Reusing saves more CO₂ than recycling.",
    "🌍 Small choices make a big impact.",
    "🐢 Slow fashion is good for Earth.",
]

# -----------------------------
# GREENER ALTERNATIVES
# -----------------------------
GREENER_ALTERNATIVES = {
    "Smartphone": ["Refurbished Phone", "Long-life Models"],
    "Laptop": ["Energy Star Laptop", "Refurbished Laptop"],
    "Sneakers": ["Recycled Material Shoes"],
    "Cheese": ["Plant-Based Cheese"],
    "Chocolate": ["Fair Trade Chocolate"],
}

# -----------------------------
# PRODUCT DATABASE
# -----------------------------
PRODUCT_DATABASE = {
    "Electronics": {
        "icon": "🔌",
        "products": [
            {"name": "Smartphone", "price": 799, "co2": 70},
            {"name": "Laptop", "price": 1299, "co2": 220},
            {"name": "Tablet", "price": 499, "co2": 95},
            {"name": "Smart Watch", "price": 299, "co2": 35},
            {"name": "Wireless Earbuds", "price": 199, "co2": 20},
            {"name": "Gaming Console", "price": 499, "co2": 180},
        ],
    },
    "Clothing": {
        "icon": "👗",
        "products": [
            {"name": "Cotton T-Shirt", "price": 25, "co2": 8},
            {"name": "Denim Jeans", "price": 60, "co2": 33},
            {"name": "Hoodie", "price": 45, "co2": 28},
            {"name": "Jacket", "price": 120, "co2": 55},
            {"name": "Sneakers", "price": 90, "co2": 42},
            {"name": "Cap", "price": 18, "co2": 5},
        ],
    },
    "Groceries": {
        "icon": "🛒",
        "products": [
            {"name": "Organic Vegetables", "price": 15, "co2": 3},
            {"name": "Fruits Pack", "price": 12, "co2": 2},
            {"name": "Plant-Based Milk", "price": 6, "co2": 1.8},
            {"name": "Cheese", "price": 8, "co2": 13},
            {"name": "Whole Grains", "price": 10, "co2": 2.5},
            {"name": "Chocolate", "price": 5, "co2": 19},
        ],
    },
    "Home Appliances": {
        "icon": "🏠",
        "products": [
            {"name": "Refrigerator", "price": 899, "co2": 300},
            {"name": "Washing Machine", "price": 699, "co2": 250},
            {"name": "Microwave Oven", "price": 299, "co2": 120},
            {"name": "Air Conditioner", "price": 1499, "co2": 500},
            {"name": "Ceiling Fan", "price": 120, "co2": 90},
        ],
    },
}

# -----------------------------
# EMOJI MAP
# -----------------------------
EMOJI_MAP = {
    "Smartphone": "📱", "Laptop": "💻", "Tablet": "📲",
    "Smart Watch": "⌚", "Wireless Earbuds": "🎧", "Gaming Console": "🎮",
    "Cotton T-Shirt": "👕", "Denim Jeans": "👖", "Hoodie": "🧥",
    "Jacket": "🧥", "Sneakers": "👟", "Cap": "🧢",
    "Organic Vegetables": "🥦", "Fruits Pack": "🍎", "Plant-Based Milk": "🥛",
    "Cheese": "🧀", "Whole Grains": "🌾", "Chocolate": "🍫",
    "Refrigerator": "🧊", "Washing Machine": "🌀",
    "Microwave Oven": "🔥", "Air Conditioner": "❄️", "Ceiling Fan": "🌀",
}

# -----------------------------
# BADGE LOGIC
# -----------------------------
def get_badges(df):
    badges = []
    if df["co2"].mean() < 20:
        badges.append("🌱 Eco Saver")
    if df["co2"].sum() < 150:
        badges.append("🐢 Low Impact Shopper")
    if len(df) >= 5:
        badges.append("🛍️ Conscious Buyer")
    return badges

# -----------------------------
# HOME PAGE
# -----------------------------
def show_home():
    st.markdown("<h1>🌍 EcoShop Impact</h1>", unsafe_allow_html=True)
    st.markdown("### Clean shopping. Smart sustainability 🌱")
    st.markdown("---")

    cols = st.columns(len(PRODUCT_DATABASE))
    for col, (category, data) in zip(cols, PRODUCT_DATABASE.items()):
        with col:
            st.markdown(
                f"""
                <div class="category-card">
                    <div style="font-size:70px;">{data['icon']}</div>
                    <h3>{category}</h3>
                </div>
                """, unsafe_allow_html=True
            )
            if st.button(f"Explore {category}", key=category):
                st.session_state.selected_category = category
                st.session_state.page = "products"
                st.rerun()

    if st.button("🛒 View Cart", use_container_width=True):
        st.session_state.page = "cart"
        st.rerun()

# -----------------------------
# PRODUCTS PAGE
# -----------------------------
def show_products():
    data = PRODUCT_DATABASE[st.session_state.selected_category]
    st.markdown(f"<h1>{data['icon']} {st.session_state.selected_category}</h1>", unsafe_allow_html=True)

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

    if st.button("🛒 View Cart"):
        st.session_state.page = "cart"
        st.rerun()

    cols = st.columns(3)
    for i, product in enumerate(data["products"]):
        with cols[i % 3]:
            emoji = EMOJI_MAP.get(product["name"], "🛍️")
            st.markdown(
                f"""
                <div class="card">
                    <div style="font-size:56px;">{emoji}</div>
                    <h3>{product['name']}</h3>
                    <p style="font-size:22px; font-weight:600;">💰 ${product['price']}</p>
                </div>
                """, unsafe_allow_html=True
            )
            if st.button("🛒 Add to Cart", key=f"cart_{i}"):
                item = product.copy()
                item["date"] = pd.Timestamp.now().date()
                st.session_state.cart.append(item)
                st.success("Added to cart")
                st.info(random.choice(ECO_TIPS))

            if st.button("💳 Buy Now", key=f"buy_{i}"):
                st.session_state.selected_product = product
                st.session_state.page = "impact"
                st.rerun()

# -----------------------------
# CART PAGE
# -----------------------------
def show_cart():
    st.markdown("<h1>🛒 Your Cart</h1>", unsafe_allow_html=True)

    if st.button("⬅ Continue Shopping"):
        st.session_state.page = "home"
        st.rerun()

    if not st.session_state.cart:
        st.info("Your cart is empty 🌱")
        return

    df = pd.DataFrame(st.session_state.cart)

    st.table(df[["name", "price", "co2", "date"]])
    st.success(f"💰 Total Price: ${df['price'].sum()}")
    st.warning(f"🌍 Total CO₂ Impact: {df['co2'].sum()} kg")

    badges = get_badges(df)
    if badges:
        st.markdown("### 🏅 Your Eco Badges")
        for b in badges:
            st.success(b)

    st.markdown("### 📊 Overall Carbon Impact by Product")
    impact_df = df.groupby("name")["co2"].sum()

    fig, ax = plt.subplots()
    ax.bar(impact_df.index, impact_df.values)
    ax.set_xlabel("Product")
    ax.set_ylabel("CO₂ (kg)")
    ax.set_title("Carbon Impact per Product in Cart")
    plt.xticks(rotation=30, ha="right")
    st.pyplot(fig)

    if st.button("💳 Checkout"):
        st.success("✅ Order placed successfully (Demo)")
        st.session_state.cart.clear()

# -----------------------------
# IMPACT PAGE
# -----------------------------
def show_impact():
    product = st.session_state.selected_product
    st.markdown(f"<h1>🌍 Carbon Impact — {product['name']}</h1>", unsafe_allow_html=True)

    if st.button("⬅ Back to Products"):
        st.session_state.page = "products"
        st.rerun()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="earth-box"><div style="font-size:90px;">🌍</div></div>', unsafe_allow_html=True)

    with col2:
        bar = st.progress(0)
        for i in range(101):
            bar.progress(i)
            time.sleep(0.015)

        df = pd.DataFrame({
            "Metric": ["CO₂ Emission", "Driving Equivalent", "Trees to Offset"],
            "Value": [
                f"{product['co2']} kg",
                f"{product['co2']*4:.1f} km",
                f"{math.ceil(product['co2']/21)} 🌳"
            ]
        })
        st.table(df)

        alts = GREENER_ALTERNATIVES.get(product["name"])
        if alts:
            st.markdown("### ♻️ Greener Alternatives")
            for a in alts:
                st.write("•", a)

# -----------------------------
# ROUTER
# -----------------------------
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "products":
    show_products()
elif st.session_state.page == "cart":
    show_cart()
elif st.session_state.page == "impact":
    show_impact()

# -----------------------------
# FOOTER
# -----------------------------
st.markdown(
    "<div class='footer'>🌱 EcoShop Impact • Clean UI • Exam-Ready Project</div>",
    unsafe_allow_html=True
)
