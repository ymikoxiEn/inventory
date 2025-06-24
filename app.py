import streamlit as st
import sqlite3
import pandas as pd

# --- Database Setup ---
conn = sqlite3.connect("inventory.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        category TEXT
    )
""")
conn.commit()

# --- UI ---
st.title("📦 Simple Inventory System")

# --- Add Item ---
with st.form("add_form"):
    st.subheader("Add New Item")
    item_name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    category = st.text_input("Category")
    submitted = st.form_submit_button("Add Item")

    if submitted:
        if item_name:
            c.execute("INSERT INTO inventory (item_name, quantity, category) VALUES (?, ?, ?)",
                      (item_name, quantity, category))
            conn.commit()
            st.success(f"'{item_name}' added to inventory.")
        else:
            st.warning("Item name is required.")

# --- View Inventory ---
st.subheader("📋 Inventory List")
df = pd.read_sql("SELECT * FROM inventory", conn)
st.dataframe(df)

# --- Delete Item ---
st.subheader("🗑️ Delete Item")
item_to_delete = st.selectbox("Select Item ID to Delete", df['id'] if not df.empty else [0])
if st.button("Delete"):
    c.execute("DELETE FROM inventory WHERE id = ?", (item_to_delete,))
    conn.commit()
    st.success(f"Item ID {item_to_delete} deleted.")

conn.close()
