# habilidadesPersonagem.py

import streamlit as st

def exibir_Habilidades():
    personagem = st.session_state.get("Atributos")

    if not personagem:
        st.warning("Nenhum personagem criado.")
        return

    st.subheader("Habilidades")

    habilidades = personagem.get("habilidades", [])

    with st.expander("Habilidades"):
        with st.container(height=400, border=True):    
            if habilidades:
                for i, item in enumerate(habilidades):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"• {item}")
                        st.divider()
                    with col2:
                        if st.button(f"Remover", key=f"remover_Habilidade_{i}"):
                            habilidades.pop(i)
                            st.session_state['Atributos']['habilidades'] = habilidades
                            st.rerun()
            else:
                st.info("Habilidades vazio.")

        st.write(len(habilidades))
        novo_item = st.text_input("Novo item", key="nova_Skill")
        if st.button("Adicionar habilidade"):
            if len(habilidades) >= 10:
                st.warning("Habilidades cheio! Remova um item antes de adicionar outro.")
            elif novo_item:
                habilidades.append(novo_item)
                st.session_state['Atributos']['habilidades'] = habilidades
                st.success(f"Item '{novo_item}' adicionado!")
                st.rerun()
            else:
                st.warning("Digite o nome do item para adicionar.")
