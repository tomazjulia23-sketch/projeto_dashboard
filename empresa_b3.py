import pandas as pd

df = pd.read_excel("PETR4_evolucao.xlsx")
print(df)

# Selecionando a coluna "valor" e aplicando funcoes estatisticas
df["valor"].max()
df["valor"].min()
df["valor"].mean()
df["valor"].std()

# selecionar linhas
df[0:1]

# selecionar linhas e colunas
colunas = ["conta", "valor"]
df[23:24][colunas]

# filtrar linhas atraves valor
linhas = df["trimestre"] == "20262T"
colunas = ["conta", "valor"]
df[linhas][colunas]

# linha 
linhas = df["conta"] == "lucro"
colunas = ["valor"]
df[linhas][colunas].mean()

# gráfico do lucro
import seaborn as sns
dados = df[linhas][colunas]
sns.lineplot(dados)

import matplotlib.pyplot as plt
import seaborn as sns
linhas = df["conta"] == "lucro"
colunas = ["trimestre", "valor"]
dados = df[linhas][colunas]
sns.lineplot(dados, x='trimestre', y='valor')
plt.title("Grafico do Lucro")
plt.xticks(rotation=45)

# Rosa
import matplotlib.pyplot as plt
import seaborn as sns
linhas = df["conta"] == "lucro"
colunas = ["trimestre", "valor"]
dados = df[linhas][colunas]
sns.set_palette(sns.color_palette(["#ffb6c1", "#ff69b4", "#ff1493"]))  # rosa claro, rosa médio, rosa forte
sns.set_style("whitegrid")
sns.lineplot(data=dados, x='trimestre', y='valor', linewidth=2, marker='o')
plt.title("Gráfico do Lucro", fontsize=16, fontweight='bold', color="#ff1493")
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

