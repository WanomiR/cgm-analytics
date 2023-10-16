import pandas as pd
import streamlit as st
import sys
# update system path to access higher order directories
sys.path.append("../")
from components.utils import *
from components.glucose_graph import GlucosePlot

# Page confit
st.set_page_config(page_title="CGM Daily Graph",
                   page_icon="📉",
                   layout="wide",
                   )


@st.cache_data
def read_data():
    """
    Read and cash the data.
    :return: pandas dataframe
    """
    entries = process_entries("./data/entries.json")
    treatments = process_treatments("./data/treatments.json")
    return treatments.combine_first(entries)


df = read_data()

# temporary variables
DATE = "2022-12-16"
RANGE_LOWER = 3.9
RANGE_UPPER = 12

st.title("CGM Daily Graph")
st.divider()

st.subheader("Graph settings")

col1, col2, col3 = st.columns(3)

with col1:
    date = st.date_input(
        "Pick a date",
        min_value=pd.to_datetime(df.index.min()),
        max_value=pd.to_datetime(df.index.max()),
        value=pd.to_datetime(df.index.min() + pd.Timedelta("4D")),
        format="YYYY-MM-DD"
    )

with col2:
    target_range_lower = st.slider(
        "Glucose range threshold: __lower__",
        min_value=3.,
        max_value=5.,
        step=.1,
        value=3.9
    )

with col3:
    target_range_upper = st.slider(
        "Glucose range threshold: __upper__",
        min_value=10.,
        max_value=14.,
        step=.2,
        value=12.
    )

st.subheader(f"Line plot graph")

glucose_plot = GlucosePlot(
    df, date,
    target_range_lower,
    target_range_upper,
)
st.pyplot(
    glucose_plot.plot(scale_factor=1.2),
    dpi=400, clear_figure=True, use_container_width=True
)