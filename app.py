import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Load secrets
db = st.secrets["database"]

# Build the pooler-based connection string
engine = create_engine(
    f"postgresql+psycopg2://{db['user']}:{db['password']}"
    f"@{db['host']}:{db['port']}/{db['database']}"
)

st.title("🌐 Online Inventory (Supabase Pooler)")

# Add New Item
with st.form("add_form"):
    name = st.text_input("Item Name")
    qty = st.number_input("Quantity", min_value=1)
    cat = st.text_input("Category")
    if st.form_submit_button("Add Item") and name:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO inventory (item_name, quantity, category) VALUES (:name, :qty, :cat)"),
                {"name": name, "qty": qty, "cat": cat}
            )
        st.success("Added!")

# Display Inventory
df = pd.read_sql("SELECT * FROM inventory", engine)
st.dataframe(df)

# Delete Item
if not df.empty:
    item_id = st.selectbox("Delete item ID", df["id"])
    if st.button("Delete"):
        with engine.begin() as conn:
            conn.execute(
                text("DELETE FROM inventory WHERE id = :id"),
                {"id": item_id}
            )
        st.success("Deleted!")
