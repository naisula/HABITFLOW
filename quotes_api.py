import requests
import streamlit as st


@st.cache_data(ttl=60)
def get_quote():

    try:

        response = requests.get(
            "https://zenquotes.io/api/random"
        )

        data = response.json()

        quote = data[0]["q"]
        author = data[0]["a"]

        return f'"{quote}" — {author}'

    except:

        return "Stay consistent. Small progress matters."