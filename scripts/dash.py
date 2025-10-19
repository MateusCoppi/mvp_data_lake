import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Função principal do dashboard
# -------------------------------
def main(df: pd.DataFrame):
    st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
    st.title("💰 Dashboard Financeiro Pessoal")

    # -----------------------------------
    # Pré-processamento dos dados
    # -----------------------------------
    # Remover colunas técnicas do Airbyte
    df = df[[c for c in df.columns if not c.startswith("_airbyte")]]

    # Converter data e valor
    df["data_transacao"] = pd.to_datetime(df["data_transacao"], errors="coerce")
    df["valor__R__"] = (
        df["valor__R__"]
        .astype(str)
        .str.replace("R\$", "", regex=True)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # -----------------------------------
    # Filtros laterais
    # -----------------------------------
    st.sidebar.header("🔎 Filtros")

    contas = st.sidebar.multiselect("Conta", df["conta"].unique(), default=df["conta"].unique())
    categorias = st.sidebar.multiselect("Categoria", df["categoria"].unique(), default=df["categoria"].unique())
    tipos = st.sidebar.multiselect("Tipo de Transação", df["tipo_transacao"].unique(), default=df["tipo_transacao"].unique())

    # Filtro de datas
    min_data, max_data = df["data_transacao"].min(), df["data_transacao"].max()
    data_range = st.sidebar.date_input("Período", [min_data, max_data])

    # Aplicar filtros
    df_filtered = df[
        (df["conta"].isin(contas))
        & (df["categoria"].isin(categorias))
        & (df["tipo_transacao"].isin(tipos))
        & (df["data_transacao"].between(pd.to_datetime(data_range[0]), pd.to_datetime(data_range[1])))
    ]

    # -----------------------------------
    # KPIs principais
    # -----------------------------------
    col1, col2, col3 = st.columns(3)
    total_entrada = df_filtered[df_filtered["tipo_transacao"].str.lower().str.contains("entrada")]["valor__R__"].sum()
    total_saida = df_filtered[df_filtered["tipo_transacao"].str.lower().str.contains("saida")]["valor__R__"].sum()
    saldo = total_entrada - total_saida

    col1.metric("💵 Total Entradas (R$)", f"{total_entrada:,.2f}")
    col2.metric("💸 Total Saídas (R$)", f"{total_saida:,.2f}")
    col3.metric("📊 Saldo (R$)", f"{saldo:,.2f}")

    st.markdown("---")

    # -----------------------------------
    # Gráficos
    # -----------------------------------
    st.subheader("📈 Análises Visuais")

    tab1, tab2, tab3 = st.tabs(["Por Categoria", "Por Mês", "Por Tipo"])

    with tab1:
        cat_agg = df_filtered.groupby("categoria")["valor__R__"].sum().reset_index()
        fig1 = px.bar(cat_agg, x="categoria", y="valor__R__", title="Total por Categoria", text_auto=True)
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        df_filtered["mes"] = df_filtered["data_transacao"].dt.to_period("M").astype(str)
        mes_agg = df_filtered.groupby("mes")["valor__R__"].sum().reset_index()
        fig2 = px.line(mes_agg, x="mes", y="valor__R__", markers=True, title="Evolução Mensal")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        tipo_agg = df_filtered.groupby("tipo_transacao")["valor__R__"].sum().reset_index()
        fig3 = px.pie(tipo_agg, names="tipo_transacao", values="valor__R__", title="Distribuição por Tipo")
        st.plotly_chart(fig3, use_container_width=True)

    # -----------------------------------
    # Tabela de dados
    # -----------------------------------
    st.subheader("📋 Dados Filtrados")
    st.dataframe(df_filtered.sort_values("data_transacao", ascending=False), use_container_width=True)


# -------------------------------
# Exemplo de uso local
# -------------------------------
if __name__ == "__main__":
    # Exemplo: carregue um DataFrame de teste
    df_exemplo = pd.DataFrame({
        "id": ["1", "2", "3"],
        "conta": ["Nubank", "Itaú", "Nubank"],
        "categoria": ["Alimentação", "Salário", "Transporte"],
        "descricao": ["Supermercado", "Pagamento", "Uber"],
        "valor__R__": ["R$ 150,00", "R$ 5.000,00", "R$ 25,00"],
        "observacoes": ["", "", ""],
        "data_transacao": ["2025-10-01", "2025-10-05", "2025-10-10"],
        "tipo_transacao": ["Saída", "Entrada", "Saída"],
        "metodo_pagamento": ["Crédito", "PIX", "Débito"],
        "_airbyte_raw_id": ["abc", "def", "ghi"],
        "_airbyte_extracted_at": pd.to_datetime(["2025-10-10", "2025-10-10", "2025-10-10"]),
        "_airbyte_generation_id": [1, 1, 1],
        "_airbyte_meta": ["{}", "{}", "{}"],
    })

    main(df_exemplo)
