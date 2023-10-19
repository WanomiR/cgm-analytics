import pandas as pd
import streamlit as st
from streamlit_dimensions import st_dimensions
import sys
# update system path to access higher order directories
sys.path.append("../")
from components.utils import *
from components.Graph import GlucoseGraph

# Page confit
st.set_page_config(page_title="CGM Daily Graph",
                   page_icon="📉",
                   layout="wide",
                   )


# @st.cache_data
def read_data():
    """
    Read and cash the data.
    :return: pandas dataframe
    """
    entries = process_entries("./data/entries.json")
    treatments = process_treatments("./data/treatments.json")
    return treatments.combine_first(entries).resample("5min").max()


df = read_data()

st.title("CGM Daily Graph")
st.divider()

st.subheader("Parameters")

col1, col2, col3 = st.columns([1, 2, 2])

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


st.subheader(f"Glucose graph")

col1, col2, col3, _ = st.columns([1, 1, 1, 2])

with col1:
    show_insulin = st.toggle("Insulin data", value=True)

with col2:
    show_carbs = st.toggle("Carbohydrates", value=True)

with col3:
    show_calibrations = st.toggle("Calibrations", value=False)

graph = GlucoseGraph(
    df, date,
    target_range_lower,
    target_range_upper,
    show_calibrations,
    show_carbs,
)

if show_insulin:
    plot = graph.plot_with_insulin
else:
    plot = graph.plot

with st.spinner("Loading..."):
    st.pyplot(
        plot(scale_factor=1.2),
        dpi=500, clear_figure=True,
        use_container_width=True
    )