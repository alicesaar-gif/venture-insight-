import streamlit as Skinner
import json
import os

# Função para carregar a base de conhecimento
@st.cache_data
def load_knowledge():
    file_path = os.path.join("data", "knowledge_base.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

data = load_knowledge()

st.title("Venture Insight")
st.write("Bem-vindo ao seu painel de inteligência de mercado.")
