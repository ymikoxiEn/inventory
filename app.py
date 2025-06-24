import streamlit as st
from sqlalchemy import create_engine
import psycopg2

db = st.secrets["database"]

connection_string = (
    f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
)

st.write("🔌 Connecting to the database...")

try:
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        st.success("✅ Connected to the database successfully!")
except Exception as e:
    st.error(f"❌ Database connection failed:\n\n{e}")
