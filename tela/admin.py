import streamlit as st
from Connect.Verify import insert_register, select_register, alter_register, delete_register

def admin_panel():
    st.title("Painel Administrativo - Habilidades")

    # ===========================
    # FORMULÁRIO PARA ADICIONAR
    # ===========================
    st.subheader("Adicionar Nova Habilidade")
    with st.form("form_add_habilidade", clear_on_submit=True):
        nome = st.text_input("Nome da Magia / Habilidade")
        nivel = st.number_input("Nível", min_value=0, max_value=10, step=1)
        tempo_de_conjuracao = st.number_input("Tempo de Conjuração", min_value=0, step=1)
        tipo_tempo_de_conjuracao = st.selectbox(
            "Tipo do Tempo de Conjuração",
            ["Ação", "Ação bônus", "Reação", "Minuto(s)", "Hora(s)"]
        )
        alcance = st.number_input("Alcance (em metros)", min_value=0, step=1)
        descricao = st.text_area("Descrição da Magia / Efeito")

        submit = st.form_submit_button("Salvar Habilidade")

        if submit:
            if not nome or not descricao:
                st.warning("⚠️ Preencha ao menos o nome e a descrição antes de salvar.")
            else:
                dados = {
                    "nome_da_magia": nome,
                    "nivel": nivel,
                    "tempo_de_conjuracao": tempo_de_conjuracao,
                    "tipo_tempo_de_conjuracao": tipo_tempo_de_conjuracao,
                    "alcance": alcance,
                    "duracao": None,
                    "componentes": None,
                    "classe": None,
                    "descricao": descricao
                }
                resultado = insert_register(dados, "habilidades")
                if resultado:
                    st.success(f"✅ Habilidade '{nome}' adicionada com sucesso!")
    
    # ===========================
    # LISTAGEM E EDIÇÃO
    # ===========================
    st.subheader("Habilidades Existentes")
    habilidades = select_register("habilidades") or []

    for hab in habilidades:
        with st.expander(f"{hab['nome_da_magia']} (Nível {hab['nivel']})"):
            st.text_area("Descrição", hab['descricao'], key=f"desc_{hab['id']}")
            st.number_input("Nível", min_value=0, max_value=10, value=hab['nivel'], key=f"nivel_{hab['id']}")
            st.number_input("Tempo de Conjuração", min_value=0, value=hab['tempo_de_conjuracao'], key=f"tempo_{hab['id']}")
            st.selectbox(
                "Tipo do Tempo de Conjuração",
                ["Ação", "Ação bônus", "Reação", "Minuto(s)", "Hora(s)"],
                index=["Ação", "Ação bônus", "Reação", "Minuto(s)", "Hora(s)"].index(hab['tipo_tempo_de_conjuracao']),
                key=f"tipo_{hab['id']}"
            )
            st.number_input("Alcance (em metros)", min_value=0, value=hab['alcance'], key=f"alcance_{hab['id']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Salvar Alterações", key=f"save_{hab['id']}"):
                    updates = {
                        "descricao": st.session_state.get(f"desc_{hab['id']}"),
                        "nivel": st.session_state.get(f"nivel_{hab['id']}"),
                        "tempo_de_conjuracao": st.session_state.get(f"tempo_{hab['id']}"),
                        "tipo_tempo_de_conjuracao": st.session_state.get(f"tipo_{hab['id']}"),
                        "alcance": st.session_state.get(f"alcance_{hab['id']}")
                    }
                    alter_register(hab['id'], updates, "habilidades")

            with col2:
                if st.button("Deletar Habilidade", key=f"del_{hab['id']}"):
                    delete_register("habilidades", {"id": hab['id']})
                    st.rerun()  # Recarrega a página após deletar
                

if __name__ == "__main__":
    admin_panel()
