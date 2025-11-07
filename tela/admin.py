import streamlit as st
from Connect.Verify import insert_register

def admin_panel():
    st.title("Painel Administrativo - Teste Inserção")

    with st.form("form_add_habilidade_minima", clear_on_submit=True):
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
                else:
                    st.error("❌ Erro ao inserir habilidade no banco de dados.")

if __name__ == "__main__":
    admin_panel()
