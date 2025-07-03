# app/main.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from api.fetch_data import get_airline_data

# Set page config
st.set_page_config(page_title="Airline Market Demand", layout="wide")

# App Title
st.title("✈️ Airline Booking Market Demand Dashboard")

# Load data
df = get_airline_data()

# Sidebar filters
st.sidebar.header("📅 Filter by Date")
if not df.empty:
    date_range = st.sidebar.date_input("Select Date Range", [])
    if date_range and len(date_range) == 2:
        df = df[
            (df["date"] >= pd.to_datetime(date_range[0])) & 
            (df["date"] <= pd.to_datetime(date_range[1]))
        ]

    # Bar Chart for Route Demand
    st.subheader("📊 Popular Routes")
    fig1 = px.bar(df, x="route", y="demand", title="Most Demanded Routes")
    st.plotly_chart(fig1, use_container_width=True)

    # Line Chart for Price Trends
    st.subheader("💰 Price Trends")
    fig2 = px.line(df, x="date", y="price", color="route", title="Price Trends Over Time")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No data found. Please check your data source.")

