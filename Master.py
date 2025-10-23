import streamlit as st

def seeAllPlayers():
  atributos_salvos = st.session_state.get('Atributos')
  st.write( atributos_salvos)
