import streamlit as st
from Connect.Verify import insert_register, select_register, delete_register, update_register  # vou supor que update_register existe

def admin_panel():
    st.title("Painel Administrativo - Gerenciamento de Habilidades")

    # --- Formulário para adicionar nova habilidade ---
    with st.expander("➕ Adicionar Nova Habilidade", expanded=True):
        with st.form("form_add_habilidade", clear_on_submit=True):
            nome = st.text_input("Nome da Magia / Habilidade")
            nivel = st.number_input("Nível", min_value=0, max_value=10, step=1)
            tempo_de_conjuracao = st.number_input("Tempo de Conjuração", min_value=0, step=1)
            tipo_tempo_de_conjuracao = st.selectbox(
                "Tipo do Tempo de Conjuração",
                ["Ação", "Ação bônus", "Reação", "Minuto(s)", "Hora(s)"]
            )
            alcance = st.number_input("Alcance (em metros)", min_value=0, step=1)
            duracao = st.text_input("Duração", placeholder="Ex: 1 minuto, Instantânea, Concentration, etc.")
            componentes = st.text_input("Componentes", placeholder="Ex: V, S, M (um cristal de quartzo)")
            classe = st.selectbox("Classe", ["Bárbaro", "Mago", "Guerreiro", "Arqueiro", "Clérigo"])
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
                        "duracao": duracao,
                        "componentes": componentes,
                        "classe": classe,
                        "descricao": descricao
                    }
                    resultado = insert_register(dados, "habilidades")
                    if resultado:
                        st.success(f"✅ Habilidade '{nome}' adicionada com sucesso!")
                    else:
                        st.error("❌ Erro ao inserir habilidade no banco de dados.")

    st.markdown("---")

    # --- Listagem e edição/exclusão ---
    st.subheader("🧙‍♂️ Habilidades Cadastradas")

    habilidades = select_register("habilidades", None, columns="*")
    if not habilidades:
        st.info("Nenhuma habilidade cadastrada ainda.")
        return

    for hab in habilidades:
        with st.expander(f"{hab['nome_da_magia']} (Nível {hab['nivel']}) - {hab['classe']}"):
            st.markdown(f"""
            **Descrição:** {hab['descricao']}  
            **Tempo de Conjuração:** {hab['tempo_de_conjuracao']} {hab['tipo_tempo_de_conjuracao']}  
            **Alcance:** {hab['alcance']} m  
            **Duração:** {hab['duracao'] or "—"}  
            **Componentes:** {hab['componentes'] or "—"}  
            """)

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✏️ Editar {hab['id']}", key=f"edit_{hab['id']}"):
                    editar_habilidade(hab)
            with col2:
                if st.button(f"🗑️ Excluir {hab['id']}", key=f"delete_{hab['id']}"):
                    confirm = st.confirm("Tem certeza que deseja excluir esta habilidade?")
                    if confirm:
                        sucesso = delete_register("habilidades", hab["id"])
                        if sucesso:
                            st.success("Habilidade excluída com sucesso!")
                            st.experimental_rerun()
                        else:
                            st.error("Erro ao excluir habilidade.")

def editar_habilidade(habilidade):
    st.title(f"Editar Habilidade: {habilidade['nome_da_magia']}")

    with st.form("form_edit_habilidade", clear_on_submit=False):
        nome = st.text_input("Nome da Magia / Habilidade", value=habilidade["nome_da_magia"])
        nivel = st.number_input("Nível", min_value=0, max_value=10, step=1, value=habilidade["nivel"])
        tempo_de_conjuracao = st.number_input("Tempo de Conjuração", min_value=0, step=1, value=habilidade["tempo_de_conjuracao"])
        tipo_tempo_de_conjuracao = st.selectbox(
            "Tipo do Tempo de Conjuração",
            ["Ação", "Ação bônus", "Reação", "Minuto(s)", "Hora(s)"],
            index=["Ação", "Ação bônus", "Reação", "Minuto(s)", "Hora(s)"].index(habilidade["tipo_tempo_de_conjuracao"])
        )
        alcance = st.number_input("Alcance (em metros)", min_value=0, step=1, value=habilidade["alcance"])
        duracao = st.text_input("Duração", value=habilidade["duracao"] or "")
        componentes = st.text_input("Componentes", value=habilidade["componentes"] or "")
        classe = st.selectbox("Classe", ["Bárbaro", "Mago", "Guerreiro", "Arqueiro", "Clérigo"],
                             index=["Bárbaro", "Mago", "Guerreiro", "Arqueiro", "Clérigo"].index(habilidade["classe"]) if habilidade["classe"] in ["Bárbaro", "Mago", "Guerreiro", "Arqueiro", "Clérigo"] else 0)
        descricao = st.text_area("Descrição da Magia / Efeito", value=habilidade["descricao"] or "")

        submit = st.form_submit_button("Salvar Alterações")

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
                    "duracao": duracao,
                    "componentes": componentes,
                    "classe": classe,
                    "descricao": descricao
                }
                # update_register espera: dados, tabela, id_coluna, id_valor
                sucesso = update_register(dados, "habilidades", "id", habilidade["id"])
                if sucesso:
                    st.success("✅ Habilidade atualizada com sucesso!")
                    st.experimental_rerun()
                else:
                    st.error("❌ Erro ao atualizar habilidade.")

if __name__ == "__main__":
    admin_panel()
