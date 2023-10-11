import streamlit as st
import sys
sys.path.append("../")

from src.components.utils import (
    process_entries,
    process_treatments
)

st.set_page_config(
    page_title="Page 2",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded",

    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


# Prepare the data
@st.cache_data
def read_data():
    entries = process_entries("./data/entries.json")
    treatments = process_treatments("./data/treatments.json")
    return treatments.combine_first(entries)


left_col, right_col = st.columns(2)
left_col.button("Press me!")

with right_col:
    chosen = st.radio(
        "Sorting hat",
        (f"option{i}" for i in range(4)))
    st.write(f"You are in {chosen} house!")


df = read_data()
st.write(df.head())
