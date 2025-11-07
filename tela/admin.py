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

    with st.expander("Adicionar Habilidade"):
        st.subheader("Adicionar Nova Habilidade")
        with st.form("form_add_habilidade", clear_on_submit=True):
            nome = st.text_input("Nome da Habilidade")
            descricao = st.text_area("Descrição")
            nivel = st.number_input("Nível da Habilidade", min_value=0, max_value=10, step=1)
            classe = st.selectbox("Classe", ["Bárbaro", "Mago", "Guerreiro", "Arqueiro", "Clérigo"])
            submit = st.form_submit_button("Salvar Habilidade")
    
            if submit:
                if nome and descricao:
                    dados = {
                        "nome": nome,
                        "descricao": descricao,
                        "nivel": nivel,
                        "classe": classe
                    }
                    if insert_register(dados, "habilidades"):
                        st.success(f"Habilidade '{nome}' adicionada com sucesso!")
                    else:
                        st.error("Erro ao inserir habilidade.")
                else:
                    st.warning("Preencha todos os campos antes de salvar.")

        # =========================
        # FILTRO DE HABILIDADES
        # =========================
    st.subheader("Listar Habilidades")

    col1, col2 = st.columns(2)
    with col1:
        filtro_nivel = st.selectbox("Filtrar por Nível", list(range(0, 11)), index=0)
    with col2:
        filtro_classe = st.selectbox("Filtrar por Classe", ["Todas", "Bárbaro", "Mago", "Guerreiro", "Arqueiro", "Clérigo"])

    # Monta filtro dinâmico
    filtros = {}
    if filtro_nivel != 0:
        filtros["nivel"] = filtro_nivel
    if filtro_classe != "Todas":
        filtros["classe"] = filtro_classe

    habilidades = select_register("habilidades", filtros if filtros else None, columns="*")

    # =========================
    # EXIBIÇÃO DAS HABILIDADES
    # =========================
    if not habilidades or len(habilidades) == 0:
        st.info("Nenhuma habilidade encontrada para esse filtro.")
    else:
        for hab in habilidades:
            with st.expander(f"🧙‍♂️ {hab['nome']} (Nível {hab['nivel']}) - {hab['classe']}"):
                st.write(f"**Descrição:** {hab['descricao']}")
