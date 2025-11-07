import streamlit as st
from Connect.Verify import insert_register, select_register

def admin_panel():
    st.title("Painel Administrativo")
    st.write("Bem-vindo ao painel administrativo. Aqui você pode gerenciar usuários, visualizar estatísticas e configurar o sistema.")
    
    if st.button("Gerenciar Habilidades"):
        exibir_habilidades()


def exibir_habilidades():
    st.title("Gerenciador de Habilidades")

    # =========================
    # CADASTRO DE NOVA HABILIDADE
    # =========================
    with st.expander("➕ Adicionar Nova Habilidade"):
        st.subheader("Cadastrar Habilidade")

        # clear_on_submit = False → mantém os valores preenchidos
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
                if nome and descricao:
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

                    if insert_register(dados, "habilidades"):
                        st.success(f"✅ Habilidade '{nome}' adicionada com sucesso!")
                        # st.rerun() removido — mantém o formulário preenchido
                    else:
                        st.error("❌ Erro ao inserir habilidade no banco de dados.")
                else:
                    st.warning("⚠️ Preencha ao menos o nome e a descrição antes de salvar.")

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
    # EXIBIÇÃO DAS HABILIDADES
    # =========================
    if not habilidades or len(habilidades) == 0:
        st.info("Nenhuma habilidade encontrada com esses filtros.")
    else:
        for hab in habilidades:
            with st.expander(f"🧙 {hab['nome_da_magia']} (Nível {hab['nivel']}) - {hab['classe']}"):
                st.markdown(f"""
                **Descrição:** {hab['descricao']}  
                **Tempo de Conjuração:** {hab['tempo_de_conjuracao']} {hab['tipo_tempo_de_conjuracao']}  
                **Alcance:** {hab['alcance']} m  
                **Duração:** {hab['duracao'] or "—"}  
                **Componentes:** {hab['componentes'] or "—"}  
                """)
