import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Load secrets
db = st.secrets["database"]

# Connect to Supabase PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
)

# Create table if not exists
with engine.begin() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id SERIAL PRIMARY KEY,
            item_name TEXT NOT NULL,
            quantity INT NOT NULL,
            category TEXT
        )
    """)

# --- UI ---
st.title("🌐 Online Inventory System (Supabase)")

# Add Item
with st.form("add_item"):
    name = st.text_input("Item Name")
    qty = st.number_input("Quantity", min_value=1)
    cat = st.text_input("Category")
    submit = st.form_submit_button("Add Item")

    if submit and name:
        with engine.begin() as conn:
            conn.execute(
                "INSERT INTO inventory (item_name, quantity, category) VALUES (%s, %s, %s)",
                (name, qty, cat)
            )
        st.success("Item added!")

# View Inventory
df = pd.read_sql("SELECT * FROM inventory", engine)
st.dataframe(df)

# Delete Item
if not df.empty:
    item_id = st.selectbox("Select ID to delete", df["id"])
    if st.button("Delete"):
        with engine.begin() as conn:
            conn.execute("DELETE FROM inventory WHERE id = %s", (item_id,))
        st.success("Item deleted.")
