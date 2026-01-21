import streamlit as st
import pdfplumber
import language_tool_python
import pandas as pd

st.set_page_config(page_title="Revisor Ortográfico de PDF")

st.title("Revisor Ortográfico de PDF")
st.write("Envie um arquivo PDF para revisão ortográfica e gramatical.")

uploaded_file = st.file_uploader("Selecione um PDF", type=["pdf"])

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        paginas = []
        for i, page in enumerate(pdf.pages, start=1):
            texto = page.extract_text() or ""
            paginas.append((i, texto))

    tool = language_tool_python.LanguageTool('pt-BR')
    erros = []

    for pagina, texto in paginas:
        matches = tool.check(texto)
        for m in matches:
            erros.append({
                "Página": pagina,
                "Tipo de erro": m.ruleIssueType,
                "Texto original": texto[m.offset:m.offset + m.errorLength],
                "Sugestão": ", ".join(m.replacements[:3])
            })

    if erros:
        df = pd.DataFrame(erros)
        st.success("Revisão concluída")
        st.dataframe(df)
        st.download_button(
            "Baixar relatório (Excel)",
            df.to_excel(index=False),
            file_name="relatorio_revisao.xlsx"
        )
    else:
        st.info("Nenhum erro encontrado.")
      
