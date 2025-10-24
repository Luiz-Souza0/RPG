import streamlit as st
import pymongo
import bcrypt
import re
from pymongo import MongoClient
import random 
from Connect.Verify import tela_registro, tela_login, validar_senha, criar_usuario, autenticar, verificar_senha, insert_register
import base64
from supabase import create_client, Client

def font_css(font_path):
    with open(font_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"""
        <style>
        @font-face {{
            font-family: 'MedievalSharp';
            src: url(data:font/truetype;charset=utf-8;base64,{encoded}) format('truetype');
        }}

        html, body, [class*="css"], .stMarkdown, .stText, .stTitle, .stHeader, .srWrite {{
            font-family: 'MedievalSharp', cursive !important;
        }}
        </style>
    """


def main():
    st.markdown(font_css("Fonts/MedievalSharp-BookOblique.ttf"), unsafe_allow_html=True)
    if 'autenticado' not in st.session_state:
        st.session_state['autenticado'] = False
    if 'Atributos' not in st.session_state:
        st.session_state['Atributos'] = None
    if 'usuario' not in st.session_state:
        st.session_state['usuario'] = None
        
    st.sidebar.title("Opções")
    
    if st.session_state['autenticado'] == False:
        escolha = st.sidebar.radio("Escolha uma opção", ("Login", "Registrar"))
        tipo = ""
    else:
        st.sidebar.write(f"Logado como: {st.session_state['usuario']}")
        tipo =  st.sidebar.radio("O que deseja ver?", ("Monstros","Ficha", "Sala do Mestre"))
        if st.sidebar.button("Sair"):
            st.session_state['autenticado'] = False
            st.session_state['Atributos'] = None
            st.session_state['usuario'] = None
            st.rerun()
        escolha = "Área Protegida"
    if tipo == "Monstros":
        from TelaMonstros import Monstros
        Monstros()
    elif tipo == "Sala do Mestre":
        from Master import seeAllPlayers
        seeAllPlayers()
    elif escolha == "Login":
        if not st.session_state['autenticado'] or st.session_state['autenticado'] == False:
            if tela_login():
                st.session_state['autenticado'] = True
                st.rerun()
    elif escolha == "Registrar":
            tela_registro()
    elif escolha == "Área Protegida":
        if st.session_state['autenticado']:
            st.title('Área Protegida - Criação de Personagem')

        if st.session_state['autenticado']:
            if 'Atributos' not in st.session_state or st.session_state['Atributos'] == None:
                st.session_state['Atributos'] = None
                
                from dadosPersonagem import gerar_valores_aleatorios

                NomePersonagem = st.text_input('Nome do Personagem', key='NomePersonagem')
                if NomePersonagem:
                    Raca = st.selectbox("Raca", ['None','Draconato', 'Elfo', 'Humano', 'Anao', 'Orc'], index=0, key='RacaPersonagem')
                    if Raca != 'None':
                        Classe = st.selectbox('Classe', ['None','Guerreiro', 'Mago', 'Ferreiro', 'Arqueiro'], index=0, key='ClassePersonagem')
                        if Classe != 'None':
                            Atributos = gerar_valores_aleatorios(NomePersonagem, Classe, Raca)
                            if Atributos != None: 
                                if (st.button("Salvar")):
                                    Atributos['Inventario'] = []
                                    st.session_state['Atributos'] = Atributos
                                    st.write(Atributos)
                                    print("Atributos front ")
                                    print(Atributos)
                                    Atributos.update({"Player":st.session_state['usuario']})
                                    insert_register(Atributos, "personagem")
                                    st.rerun()
            else :
                from ExibirPersonagemCriado import exibir_personagem_criado
                exibir_personagem_criado()


if __name__ == "__main__":
    main()
