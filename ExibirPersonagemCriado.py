# ExibirPersonagemCriado.py

import streamlit as st
from Inventario import exibir_inventario
from Habilidades import exibir_Habilidades
from Connect.Verify import select_register

def exibir_personagem_criado(regid: int):
    # Buscar o personagem salvo no banco pelo ID
    resultado = select_register("personagens", {"id": regid}, columns="*")

    if not resultado or len(resultado) == 0:
        atributos_salvos = st.session_state.get('Atributos')
        if not atributos_salvos:
            st.warning("Nenhum personagem criado ainda.")
            return
    else:
        atributos_salvos = resultado[0]

    # Guarda as habilidades no session_state
    st.session_state["habilidades"] = atributos_salvos.get("habilidades", [])

    st.success("Personagem carregado do banco de dados.")
    st.header(f"Seu Personagem: {atributos_salvos['Nome']}")

    linha1_col1, linha1_col2, linha1_col3 = st.columns(3)
    with linha1_col1:
        st.metric("Raça", atributos_salvos["Raca"])
    with linha1_col2:
        st.metric("Classe", atributos_salvos["Classe"])
    with linha1_col3:
        st.metric("Nível", atributos_salvos["Nivel"])

    linha2_col1, linha2_col2, linha2_col3 = st.columns(3)
    with linha2_col1:
        st.metric("Ataque", atributos_salvos["Atk"])
    with linha2_col2:
        st.metric("Destreza", atributos_salvos["Des"])
    with linha2_col3:
        st.metric("Constituição", atributos_salvos["Const"])

    linha3_col1, linha3_col2, linha3_col3 = st.columns(3)
    with linha3_col1:
        st.metric("Carisma", atributos_salvos["Car"])
    with linha3_col2:
        st.metric("Inteligência", atributos_salvos["Int"])
    with linha3_col3:
        st.metric("Sabedoria", atributos_salvos["Sab"])

    st.divider()
    exibir_inventario()
    st.divider()
    exibir_Habilidades()

    if st.button("Reiniciar Criação de Personagem"):
        st.session_state['Atributos'] = None
        st.rerun()
