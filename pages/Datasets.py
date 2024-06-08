import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
# Set the page title and header
st.title("Dataset de eleccion ")

df = pd.read_csv('static/datasets/cesde.csv')