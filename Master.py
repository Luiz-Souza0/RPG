import streamlit as st

def seeAllPlayers():
  atributos_salvos = select_register("personagens", None, columns="*")
  st.write( atributos_salvos)
