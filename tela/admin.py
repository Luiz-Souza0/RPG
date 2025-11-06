import streamlit as st

def admin_panel():
    st.title("Painel Administrativo")
    st.write("Bem-vindo ao painel administrativo. Aqui você pode gerenciar usuários, visualizar estatísticas e configurar o sistema.")
    if st.button("Gerenciar Habilidades"):
        criar_habilidades()

def criar_habilidades():
    st.title("Criação de Habilidades")
    st.write("Aqui você pode criar e gerenciar habilidades para os personagens do jogo.")
    