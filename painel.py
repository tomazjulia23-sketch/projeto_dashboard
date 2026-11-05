import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# ========================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================

st.set_page_config(
    page_title="Dashboard Petrobras",
    page_icon="🛢️",
    layout="wide"
)

# ========================================
# CSS CUSTOMIZADO
# ========================================

st.markdown("""
<style>

.main {
    background-color: #F5F7FA;
}

.block-container {
    padding-top: 1rem;
}

div[data-testid="metric-container"] {
    background-color: white;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    border-left: 5px solid #00A651;
}

h1 {
    color: #003B5C;
}

h2,h3 {
    color: #003B5C;
}

</style>
""", unsafe_allow_html=True)

# ========================================
# LEITURA DOS DADOS
# ========================================

df = pd.read_excel("PETR4_evolucao.xlsx")

# ========================================
# FILTRO DE LUCRO
# ========================================

dados_lucro = (
    df[df["conta"] == "lucro"]
    [["trimestre", "valor"]]
    .copy()
)

# ========================================
# KPIs
# ========================================

lucro_atual = dados_lucro["valor"].iloc[-1]

crescimento = (
    (
        dados_lucro["valor"].iloc[-1]
        - dados_lucro["valor"].iloc[-2]
    )
    /
    dados_lucro["valor"].iloc[-2]
) * 100

# ========================================
# TABS
# ========================================

tab1, tab2 = st.tabs(
    ["📈 Dashboard PETR4", "🏢 Empresas da B3"]
)

# ========================================
# TAB 1
# ========================================

with tab1:

    st.title("🛢️ Dashboard Corporativo Petrobras")

    st.markdown("""
    ### Visão Geral da Companhia

    A Petrobras é uma das maiores empresas de energia do mundo,
    líder em exploração de petróleo em águas profundas e
    ultraprofundas.

    **Ticker:** PETR4  
    **Setor:** Petróleo, Gás e Energia  
    **Negociação:** B3  
    **Refinarias:** 10  
    **Atuação:** Exploração, Produção, Refino e Distribuição
    """)

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💰 Lucro Atual",
        f"R$ {lucro_atual:,.0f}"
    )

    col2.metric(
        "📈 Crescimento",
        f"{crescimento:.2f}%"
    )

    col3.metric(
        "📊 Observações",
        len(dados_lucro)
    )

    col4.metric(
        "🏭 Setor",
        "Energia"
    )

    st.divider()

    # ====================================
    # GRAFICO DE LUCRO
    # ====================================

    st.subheader("Evolução do Lucro")

    sns.set_style("white")

    fig, ax = plt.subplots(
        figsize=(12,6)
    )

    sns.lineplot(
        data=dados_lucro,
        x="trimestre",
        y="valor",
        marker="o",
        markersize=10,
        linewidth=4,
        color="#00A651",
        ax=ax
    )

    ax.fill_between(
        dados_lucro["trimestre"],
        dados_lucro["valor"],
        alpha=0.20,
        color="#00A651"
    )

    for x, y in zip(
        dados_lucro["trimestre"],
        dados_lucro["valor"]
    ):
        ax.text(
            x,
            y,
            f"{y:,.0f}",
            fontsize=9,
            fontweight="bold",
            ha="center"
        )

    ax.set_title(
        "Evolução do Lucro da Petrobras",
        fontsize=18,
        fontweight="bold"
    )

    ax.set_xlabel("")
    ax.set_ylabel("Valor (R$)")

    plt.xticks(rotation=45)

    sns.despine()

    st.pyplot(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Base de Dados")

    st.dataframe(
        df,
        use_container_width=True
    )

# ========================================
# TAB 2
# ========================================

with tab2:

    st.title("🏢 Empresas Listadas na B3")

    df_b3 = pd.read_excel("planilhao_b3.xlsx")

    col1, col2 = st.columns([2,1])

    with col1:
        st.dataframe(
            df_b3,
            use_container_width=True
        )

    empresas_setor = (
        df_b3.groupby("setor")
        .size()
        .reset_index(name="quantidade")
        .sort_values(
            "quantidade",
            ascending=False
        )
    )

    with col2:

        st.metric(
            "Total Empresas",
            len(df_b3)
        )

        st.metric(
            "Total Setores",
            empresas_setor.shape[0]
        )

    st.divider()

    # ====================================
    # GRAFICO DE SETORES
    # ====================================

    fig2, ax2 = plt.subplots(
        figsize=(12,7)
    )

    cores = sns.color_palette(
        "viridis",
        len(empresas_setor)
    )

    sns.barplot(
        data=empresas_setor,
        x="quantidade",
        y="setor",
        palette=cores,
        ax=ax2
    )

    for i, valor in enumerate(
        empresas_setor["quantidade"]
    ):
        ax2.text(
            valor + 0.3,
            i,
            str(valor),
            va="center",
            fontweight="bold"
        )

    ax2.set_title(
        "Número de Empresas por Setor",
        fontsize=18,
        fontweight="bold"
    )

    ax2.set_xlabel("Quantidade")
    ax2.set_ylabel("")

    sns.despine()

    st.pyplot(
        fig2,
        use_container_width=True
    )

    st.divider()

    st.subheader("Distribuição por Setor")

    st.dataframe(
        empresas_setor,
        use_container_width=True
    )
    