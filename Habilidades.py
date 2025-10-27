import streamlit as st
from Connect.Verify import alter_register

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
                            personagem["habilidades"] = habilidades
                            st.session_state['Atributos'] = personagem
                            # Atualiza no banco
                            if "id" in personagem:
                                alter_register(personagem["id"], {"habilidades": habilidades}, "personagens")
                            st.rerun()
            else:
                st.info("Habilidades vazio.")

        st.write(f"Total: {len(habilidades)}")

        novo_item = st.text_input("Novo item", key="nova_Skill")
        if st.button("Adicionar habilidade"):
            if len(habilidades) >= 10:
                st.warning("Habilidades cheio! Remova um item antes de adicionar outro.")
            elif novo_item:
                habilidades.append(novo_item)
                personagem["habilidades"] = habilidades
                st.session_state['Atributos'] = personagem
                # Atualiza no banco
                if "id" in personagem:
                    alter_register(personagem["id"], {"habilidades": habilidades}, "personagens")
                st.success(f"Item '{novo_item}' adicionado!")
                st.rerun()
            else:
                st.warning("Digite o nome do item para adicionar.")
