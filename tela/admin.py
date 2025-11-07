import streamlit as st
from Connect.Verify import insert_register, select_register, delete_register, alter_register  # vou supor que update_register existe


def admin_panel():
    st.title("Painel Administrativo")
    st.write("Bem-vindo ao painel administrativo. Aqui você pode gerenciar usuários, visualizar estatísticas e configurar o sistema.")
    
    if st.button("Gerenciar Habilidades"):
        st.title("Gerenciador de Habilidades")

        # =========================
        # CADASTRO DE NOVA HABILIDADE
        # =========================
        with st.expander("➕ Adicionar Nova Habilidade"):
            st.subheader("Cadastrar Habilidade")

            with st.form("form_add_habilidade", clear_on_submit=False):
                nome = st.text_input("Nome da Magia / Habilidade")
                nivel = st.number_input("Nível", min_value=0, max_value=10, step=1)

                col1, col2 = st.columns(2)
                with col1:
                    tempo_de_conjuracao = st.number_input("Tempo de Conjuração", min_value=0, step=1)
                with col2:
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

        # =========================
        # FILTRO DE HABILIDADES
        # =========================
        st.subheader("🔍 Listar Habilidades")

        col1, col2 = st.columns(2)
        with col1:
            filtro_nivel = st.selectbox("Filtrar por Nível", ["Todos"] + [str(i) for i in range(0, 11)])
        with col2:
            filtro_classe = st.selectbox("Filtrar por Classe", ["Todas", "Bárbaro", "Mago", "Guerreiro", "Arqueiro", "Clérigo"])

        filtros = {}
        if filtro_nivel != "Todos":
            filtros["nivel"] = int(filtro_nivel)
        if filtro_classe != "Todas":
            filtros["classe"] = filtro_classe

        habilidades = select_register("habilidades", filtros if filtros else None, columns="*")

        # =========================
        # EXIBIÇÃO, EDIÇÃO E EXCLUSÃO DAS HABILIDADES
        # =========================
        if not habilidades:
            st.info("Nenhuma habilidade encontrada com esses filtros.")
        else:
            for hab in habilidades:
                with st.expander(f"🧙 {hab['nome_da_magia']} (Nível {hab['nivel']}) - {hab['classe']}"):

                    # Mostrar detalhes
                    st.markdown(f"""
                    **Descrição:** {hab['descricao']}  
                    **Tempo de Conjuração:** {hab['tempo_de_conjuracao']} {hab['tipo_tempo_de_conjuracao']}  
                    **Alcance:** {hab['alcance']} m  
                    **Duração:** {hab['duracao'] or "—"}  
                    **Componentes:** {hab['componentes'] or "—"}  
                    """)

                    col_edit, col_delete = st.columns(2)

                    # BOTÃO DE EDIÇÃO
                    with col_edit:
                        if st.button(f"✏️ Editar {hab['nome_da_magia']}", key=f"edit_{hab['id']}"):
                            with st.form(f"form_edit_{hab['id']}"):
                                nome_edit = st.text_input("Nome da Magia / Habilidade", value=hab['nome_da_magia'])
                                nivel_edit = st.number_input("Nível", min_value=0, max_value=10, step=1, value=hab['nivel'])
                                tempo_edit = st.number_input("Tempo de Conjuração", min_value=0, step=1, value=hab['tempo_de_conjuracao'])
                                tipo_tempo_edit = st.selectbox(
                                    "Tipo do Tempo de Conjuração",
                                    ["Ação", "Ação bônus", "Reação", "Minuto(s)", "Hora(s)"],
                                    index=["Ação", "Ação bônus", "Reação", "Minuto(s)", "Hora(s)"].index(hab['tipo_tempo_de_conjuracao'])
                                )
                                alcance_edit = st.number_input("Alcance (em metros)", min_value=0, step=1, value=hab['alcance'])
                                duracao_edit = st.text_input("Duração", value=hab['duracao'] or "")
                                componentes_edit = st.text_input("Componentes", value=hab['componentes'] or "")
                                classe_edit = st.selectbox(
                                    "Classe",
                                    ["Bárbaro", "Mago", "Guerreiro", "Arqueiro", "Clérigo"],
                                    index=["Bárbaro", "Mago", "Guerreiro", "Arqueiro", "Clérigo"].index(hab['classe'])
                                )
                                descricao_edit = st.text_area("Descrição", value=hab['descricao'])

                                submit_edit = st.form_submit_button("Salvar Alterações")
                                if submit_edit:
                                    updates = {
                                        "nome_da_magia": nome_edit,
                                        "nivel": nivel_edit,
                                        "tempo_de_conjuracao": tempo_edit,
                                        "tipo_tempo_de_conjuracao": tipo_tempo_edit,
                                        "alcance": alcance_edit,
                                        "duracao": duracao_edit,
                                        "componentes": componentes_edit,
                                        "classe": classe_edit,
                                        "descricao": descricao_edit
                                    }
                                    alter_register(hab['id'], updates, "habilidades")

                    # BOTÃO DE EXCLUSÃO
                    with col_delete:
                        if st.button(f"🗑️ Excluir {hab['nome_da_magia']}", key=f"del_{hab['id']}"):
                            delete_register("habilidades", {"id": hab['id']})
                            st.experimental_rerun()  # Recarrega a página para atualizar lista
