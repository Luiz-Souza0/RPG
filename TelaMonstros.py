import streamlit as st
import fitz  # PyMuPDF

# Banco de dados de monstros (adicione mais conforme necessário)
monstros_db = [
    {
        "nome": "Goblin",
        "tipo": "Terrestre",
        "ambientacao": ["Floresta", "Caverna"],
        "dificuldade": "Fácil",
        "pagina": 150
    },
    {
        "nome": "Dragão Vermelho",
        "tipo": "Voador",
        "ambientacao": ["Montanha", "Caverna"],
        "dificuldade": "Mestre",
        "pagina": 100
    },
    {
        "nome": "Sereia",
        "tipo": "Aquático",
        "ambientacao": ["Lago", "Mar"],
        "dificuldade": "Médio",
        "pagina": 200
    },
    # Adicione mais monstros aqui
]

def mostrar_pagina_pdf(pagina, nome_monstro, zoom=1.0):
    try:
        caminho_pdf = "Pdfs/manual_dos_monstros.pdf"
        doc = fitz.open(caminho_pdf)

        if pagina < 1 or pagina > len(doc):
            st.error("Página fora do intervalo.")
            return

        page = doc.load_page(pagina - 1)

        # Aplica zoom com uma matriz de transformação
        matrix = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=matrix)

        img_bytes = pix.tobytes("png")
        st.image(img_bytes, caption=f"{nome_monstro} - Página {pagina}", use_column_width=False)
    except Exception as e:
        st.error(f"Erro ao abrir o PDF: {e}")

def Monstros():
    st.title("Enciclopédia de Monstros")

    # Sidebar com filtros
    st.sidebar.subheader("Filtros")

    tipos = sorted(set(m["tipo"] for m in monstros_db))
    ambientacoes = sorted(set(a for m in monstros_db for a in m["ambientacao"]))
    dificuldades = ["Fácil", "Médio", "Difícil", "Mestre", "Impossível"]

    tipo_selecionado = st.sidebar.multiselect("Tipo", tipos, default=tipos)
    ambientacao_selecionada = st.sidebar.multiselect("Ambientação", ambientacoes, default=ambientacoes)
    dificuldade_selecionada = st.sidebar.multiselect("Dificuldade", dificuldades, default=dificuldades)

    # Filtrar monstros
    monstros_filtrados = [
        m for m in monstros_db
        if m["tipo"] in tipo_selecionado
        and any(a in ambientacao_selecionada for a in m["ambientacao"])
        and m["dificuldade"] in dificuldade_selecionada
    ]

    if not monstros_filtrados:
        st.warning("Nenhum monstro encontrado com os filtros selecionados.")
    else:
        for monstro in monstros_filtrados:
            with st.expander(monstro["nome"]):
                # st.markdown(f"**Tipo:** {monstro['tipo']}")
                # st.markdown(f"**Ambientação:** {', '.join(monstro['ambientacao'])}")
                # st.markdown(f"**Dificuldade:** {monstro['dificuldade']}")
                mostrar_pagina_pdf(monstro["pagina"], monstro["nome"])
