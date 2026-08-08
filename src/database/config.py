# We are connecting our Streamlit application to our Supabase database so that our Python code can read and write data in Supabase.
import streamlit as st

from supabase import create_client, Client 
#From the Supabase Python library, import the tools create_client and Client so I can use them in my code.


supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_PUBLISHABLE_KEY"]
)
# Here is my Supabase project URL and my API key. Create a client that I can use to communicate with Supabase."
# supabase becomes your tool for interacting with the database.