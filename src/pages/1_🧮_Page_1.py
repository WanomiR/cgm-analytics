import streamlit as st
import numpy as np
from streamlit_dimensions import st_dimensions
import sys
sys.path.append("../")

from components.utils import *
from components.glucose_graph import plot_glucose

st.set_page_config(page_title="DataFrame Demo",
                   page_icon="📊", layout="wide")

@st.cache_data
def read_data():
    entries = process_entries("./data/entries.json")
    treatments = process_treatments("./data/treatments.json")
    return treatments.combine_first(entries)


df = read_data()

# temporary variables
DATE = "2022-12-16"
RANGE_LOWER = 3.9
RANGE_UPPER = 12


st.pyplot(
    plot_glucose(df, DATE, RANGE_LOWER, RANGE_UPPER, fig_scale(5)),
    dpi=400, clear_figure=True, use_container_width=True
)