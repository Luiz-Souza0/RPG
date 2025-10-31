import streamlit as st
import bcrypt
import random
import base64
from Connect.Verify import (
    tela_registro, tela_login, validar_senha,
    criar_usuario, autenticar, verificar_senha,
    insert_register, select_register
)

def font_css(font_path):
    with open(font_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"""
        <style>
        @font-face {{
            font-family: 'MedievalSharp';
            src: url(data:font/truetype;charset=utf-8;base64,{encoded}) format('truetype');
        }}
        html, body, [class*="css"], .stMarkdown, .stText, .stTitle, .stHeader {{
            font-family: 'MedievalSharp', cursive !important;
        }}
        </style>
    """

def main():
    st.markdown(font_css("Fonts/MedievalSharp-BookOblique.ttf"), unsafe_allow_html=True)

    # Inicializa sessão
    if 'autenticado' not in st.session_state:
        st.session_state['autenticado'] = False
    if 'Atributos' not in st.session_state:
        st.session_state['Atributos'] = None
    if 'usuario' not in st.session_state:
        st.session_state['usuario'] = None
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    if 'role' not in st.session_state:
        st.session_state['role'] = None
    if 'menu' not in st.session_state:
        st.session_state['menu'] = ["Login", "Registrar"]

    st.sidebar.title("Opções")

    # ========================================
    # LOGIN / REGISTRO
    # ========================================
    if not st.session_state['autenticado']:
        escolha = st.sidebar.radio("Escolha uma opção", st.session_state['menu'])

        if escolha == "Login":
            if tela_login():
                dados = select_register("usuarios", {"usuario": st.session_state['usuario']}, columns=["id", "role"])
                if dados and len(dados) > 0:
                    st.session_state['user_id'] = dados[0]['id']
                    st.session_state['role'] = dados[0]['role']
                st.session_state['autenticado'] = True
                st.session_state['menu'] = ["Monstros", "Ficha", "Sala do Mestre"]
                if st.session_state['role'] == "admin":
                    st.session_state['menu'].append("admin")
                st.rerun()

        elif escolha == "Registrar":
            tela_registro()
        return  # evita executar o resto

    # ========================================
    # ÁREA PROTEGIDA
    # ========================================
    st.sidebar.write(f"Logado como: {st.session_state['usuario']}")
    st.sidebar.write(f"Função: {st.session_state['role']}")
    tipo = st.sidebar.radio("O que deseja ver?", st.session_state['menu'])

    if st.sidebar.button("Sair"):
        st.session_state['autenticado'] = False
        st.session_state['Atributos'] = None
        st.session_state['usuario'] = None
        st.session_state['user_id'] = None
        st.rerun()

    # =======================
    # SEÇÕES DO SISTEMA
    # =======================
    if tipo == "Monstros":
        from TelaMonstros import Monstros
        Monstros()

    elif tipo == "Sala do Mestre":
        from Master import seeAllPlayers
        seeAllPlayers()

    elif tipo == "admin":
        st.title("Sala do Administrador")
        if st.input_text("Qual a senha? ") == "777":
            st.write("Entrou!! ")

    elif tipo == "Ficha":
        if not st.session_state['user_id']:
            st.error("Erro: ID do jogador não encontrado.")
            return

        st.title("Criação e Exibição de Personagem")

        user_id = st.session_state['user_id']
        personagem_existente = select_register("personagens", {"Player": user_id}, columns="*")

        # Se já existe personagem → exibe
        if personagem_existente and len(personagem_existente) > 0:
            from ExibirPersonagemCriado import exibir_personagem_criado
            exibir_personagem_criado(personagem_existente[0]["id"])
            return

        # Caso contrário → cria novo personagem
        from dadosPersonagem import gerar_valores_aleatorios

        NomePersonagem = st.text_input('Nome do Personagem', key='NomePersonagem')
        if NomePersonagem:
            Raca = st.selectbox("Raça", ['None', 'Draconato', 'Elfo', 'Humano', 'Anão', 'Orc'], index=0, key='RacaPersonagem')
            if Raca != 'None':
                Classe = st.selectbox('Classe', ['None', 'Guerreiro', 'Mago', 'Ferreiro', 'Arqueiro'], index=0, key='ClassePersonagem')
                if Classe != 'None':
                    Atributos = gerar_valores_aleatorios(NomePersonagem, Classe, Raca)
                    if Atributos:
                        if st.button("Salvar"):
                            Atributos['Inventario'] = []
                            Atributos.update({"Player": user_id})
                            st.session_state['Atributos'] = Atributos

                            if insert_register(Atributos, "personagens"):
                                st.success("Personagem criado com sucesso!")
                                st.rerun()

if __name__ == "__main__":
    main()
