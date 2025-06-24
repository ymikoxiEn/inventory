import streamlit as st
import requests
import pandas as pd

API_URL = "API_URL = "https://your-backend.onrender.com"
"

st.title("📦 Inventory Dashboard")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")
else:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    with st.form("add_form"):
        item_name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=1)
        category = st.text_input("Category")
        submitted = st.form_submit_button("Add Item")
        if submitted and item_name:
            r = requests.post(f"{API_URL}/items", json={
                "item_name": item_name,
                "quantity": quantity,
                "category": category
            })
            if r.status_code == 200:
                st.success("Item added!")
            else:
                st.error("Failed to add item")

    r = requests.get(f"{API_URL}/items")
    if r.status_code == 200:
        df = pd.DataFrame(r.json())
        st.dataframe(df)
        if not df.empty:
            item_id = st.selectbox("Delete item ID", df["id"])
            if st.button("Delete"):
                r = requests.delete(f"{API_URL}/items/{item_id}")
                if r.status_code == 200:
                    st.success("Deleted!")
                else:
                    st.error("Error deleting")
    else:
        st.error("Failed to fetch items")
