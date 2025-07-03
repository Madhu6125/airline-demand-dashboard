# api/fetch_data.py

import pandas as pd
import requests
import streamlit as st  # ✅ Add this line to access secrets

def get_airline_data():
    API_KEY = st.secrets["API_KEY"]  # ✅ Securely read your API key
    url = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}&limit=100"

    try:
        response = requests.get(url)
        data = response.json()

        flights = data.get('data', [])
        records = []

        for flight in flights:
            try:
                route = f"{flight['departure']['airport']} - {flight['arrival']['airport']}"
                date = flight['departure']['scheduled']
                price = 100 + hash(route) % 200  # Simulated price
                demand = hash(route + date) % 200  # Simulated demand

                records.append({
                    "route": route,
                    "date": pd.to_datetime(date),
                    "price": price,
                    "demand": demand
                })
            except:
                continue  # skip if any field is missing

        df = pd.DataFrame(records)
        return df

    except Exception as e:
        print("Error fetching API data:", e)
        return pd.DataFrame()
