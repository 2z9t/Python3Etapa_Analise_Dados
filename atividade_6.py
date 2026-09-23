import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ibge = pd.read_excel("Tabela 1.1.1.xls", sheet_name="2022", header=None)
ibge_dados = ibge.iloc[9:, [0, 1, 2, 3, 4, 5, 6, 7]].copy()
ibge_dados.columns = ["Estado", "Total", "Branca_Total", "PretaParda_Total", "Homem_Branca", "Homem_PretaParda", "Mulher_Branca", "Mulher_PretaParda"]
ibge_dados = ibge_dados[ibge_dados["Estado"].notna()]
ibge_dados = ibge_dados[~ibge_dados["Estado"].astype(str).str.contains("Fonte|Notas|\\(", na=False)]

estados_uf = ["Rondônia", "Acre", "Amazonas", "Roraima", "Pará", "Amapá", "Tocantins", "Maranhão", "Piauí", "Ceará", "Rio Grande do Norte", "Paraíba", "Pernambuco", "Alagoas", "Sergipe", "Bahia", "Minas Gerais", "Espírito Santo", "Rio de Janeiro", "São Paulo", "Paraná", "Santa Catarina", "Rio Grande do Sul", "Mato Grosso do Sul", "Mato Grosso", "Goiás", "Distrito Federal"]

ibge_estados = ibge_dados[ibge_dados["Estado"].isin(estados_uf)].copy()
for col in ibge_estados.columns[1:]:
    ibge_estados[col] = pd.to_numeric(ibge_estados[col], errors="coerce")

t2012 = pd.read_csv("Tabela5-sem_emprego_2012.csv", sep=";", encoding="utf-8-sig")
t2026 = pd.read_csv("Tabela5-sem_emprego_2026.csv", sep=";", encoding="utf-8-sig")
t2012.columns = ["Sigla", "Codigo", "Estado", "homens_2012", "mulheres_2012"]
t2026.columns = ["Sigla", "Codigo", "Estado", "homens_2026", "mulheres_2026"]

comp = t2012.merge(t2026, on=["Sigla", "Codigo", "Estado"], how="inner")
comp_ibge = comp.merge(ibge_estados, on="Estado", how="inner")

ordem = comp_ibge.sort_values("mulheres_2026", ascending=False)["Estado"]

longo = comp_ibge.melt(
    id_vars=["Sigla", "Codigo", "Estado"],
    value_vars=["mulheres_2012", "mulheres_2026"],
    var_name="Ano",
    value_name="Participacao_mulheres",
)
longo["Ano"] = longo["Ano"].map({"mulheres_2012": "2012 T1", "mulheres_2026": "2026 T1"})

fig, ax = plt.subplots(figsize=(10, 10))
sns.barplot(data=longo, y="Estado", x="Participacao_mulheres", hue="Ano", order=ordem, ax=ax)
ax.axvline(50, color="red", linestyle="--", linewidth=1)
ax.set_xlabel("Participação das mulheres entre as pessoas desocupadas (%)")
ax.set_ylabel("")
ax.set_title("Desocupação: participação feminina em 2012 T1 e 2026 T1")
ax.legend(title="Período")
fig.tight_layout()
plt.show()