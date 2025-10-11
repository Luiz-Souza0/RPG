# InventarioPersonagem.py

import streamlit as st

def exibir_inventario():
    personagem = st.session_state.get("Atributos")

    if not personagem:
        st.warning("Nenhum personagem criado.")
        return

    st.subheader("Inventário")

    inventario = personagem.get("Inventario", [])

    with st.expander("Inventário"):
        with st.container(height=400, border=True):    
            if inventario:
                for i, item in enumerate(inventario):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"• {item}")
                        st.divider()
                    with col2:
                        if st.button(f"Remover", key=f"remover_{i}"):
                            inventario.pop(i)
                            st.session_state['Atributos']['Inventario'] = inventario
                            st.rerun()
            else:
                st.info("Inventário vazio.")

        st.write(len(inventario))
        novo_item = st.text_input("Novo item", key="novo_item")
        if st.button("Adicionar item"):
            if len(inventario) >= 10:
                st.warning("Inventário cheio! Remova um item antes de adicionar outro.")
            elif novo_item:
                inventario.append(novo_item)
                st.session_state['Atributos']['Inventario'] = inventario
                st.success(f"Item '{novo_item}' adicionado!")
                st.rerun()
            else:
                st.warning("Digite o nome do item para adicionar.")
