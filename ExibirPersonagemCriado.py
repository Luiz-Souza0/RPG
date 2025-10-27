# ExibirPersonagemCriado.py

import streamlit as st
from Inventario import exibir_inventario
from Habilidades import exibir_Habilidades
from Connect.Verify import select_register

def exibir_personagem_criado(regid: int):
        # Buscar o personagem salvo no banco pelo ID
    atributos_salvos = select_register("personagens", {"id": regid}, columns="*")[0]

    if not atributos_salvos or len(atributos_salvos) == 0:
        atributos_salvos = st.session_state.get('Atributos')
    if not atributos_salvos:
        st.warning("Nenhum personagem criado ainda.")
        return


    st.session_state["habilidades"] = atributos_salvos.get("habilidades", [])
    st.error("Personagem carregado do banco de dados.")
    if not atributos_salvos:
        atributos_salvos = st.session_state.get('Atributos')
        if not atributos_salvos:
            st.warning("Nenhum personagem criado ainda.")
            return
    
    st.header(f"Seu Personagem: {atributos_salvos['Nome']}")

    linha1_col1, linha1_col2, linha1_col3 = st.columns(3)
    with linha1_col1:
        st.metric("Raca", atributos_salvos["Raca"])
    with linha1_col2:
        st.metric("Classe", atributos_salvos["Classe"])
    with linha1_col3:
        st.metric("Nivel", atributos_salvos["Nivel"])
        # st.empty()

    linha2_col1, linha2_col2, linha2_col3 = st.columns(3)
    with linha2_col1:
        st.metric("Ataque", atributos_salvos["Atk"])
    with linha2_col2:
        st.metric("Destreza", atributos_salvos["Des"])
    with linha2_col3:
        st.metric("Constituicao", atributos_salvos["Const"])

    linha3_col1, linha3_col2, linha3_col3 = st.columns(3)
    with linha3_col1:
        st.metric("Carisma", atributos_salvos["Car"])
    with linha3_col2:
        st.metric("Inteligencia", atributos_salvos["Int"])
    with linha3_col3:
        st.metric("Sabedoria", atributos_salvos["Sab"])
    
    st.divider()  # linha separadora
    exibir_inventario()
    st.divider()  # linha separadora
    exibir_Habilidades()

    if st.button("Reiniciar Criacao de Personagem"):
        st.session_state['Atributos'] = None
        st.rerun()
