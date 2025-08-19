import streamlit as st
from supabase import create_client

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]

supabase = create_client(url, key)

if __name__ == "__main__":
    from pprint import pprint
    data = supabase.table("teams").select("*").execute()
    pprint(data.data)
