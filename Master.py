import streamlit as st

def seeAllPlayers():
  atributos_salvos = st.session_state.get('Atributos')
  st.metric("Personagens:", atributos_salvos)
