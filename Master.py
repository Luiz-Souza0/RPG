import streamlit as st
from Connect.Verify import select_register
 
def seeAllPlayers():
  atributos_salvos = select_register("personagens", filter: dict = None, columns="*")
  st.write( atributos_salvos)

