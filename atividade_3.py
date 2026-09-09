# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

file_path = "Tabela_3_Areas_gerais_de_formacao_na_graduacao.xlsx"
df = pd.read_excel(file_path, skiprows=1)

print(df.head(10))
print("\n" + "="*80 + "\n")

df.columns = [
    'Regiao',
    'Total_Geral', 'Total_Homens', 'Total_Mulheres',
    'STEM_Total', 'STEM_Homens', 'STEM_Mulheres',
    'Educacao_Saude_Total', 'Educacao_Saude_Homens', 'Educacao_Saude_Mulheres'
]

df = df.dropna(subset=['Regiao'])
df = df[~df['Regiao'].str.contains('Total|Fonte|Brasil', na=False)]
df = df.reset_index(drop=True)

print(df.head(10))
print(f"\nTotal de registros: {len(df)}")
print("\n" + "="*80 + "\n")

tabela_geral = df[['Regiao', 'Total_Homens', 'Total_Mulheres']].copy()
tabela_geral['Total_Regiao'] = tabela_geral['Total_Homens'] + tabela_geral['Total_Mulheres']

tabela_stem = df[['Regiao', 'STEM_Homens', 'STEM_Mulheres']].copy()
tabela_stem['STEM_Total'] = tabela_stem['STEM_Homens'] + tabela_stem['STEM_Mulheres']

tabela_educ_saude = df[['Regiao', 'Educacao_Saude_Homens', 'Educacao_Saude_Mulheres']].copy()
tabela_educ_saude['Educacao_Saude_Total'] = tabela_educ_saude['Educacao_Saude_Homens'] + tabela_educ_saude['Educacao_Saude_Mulheres']

print("Tabela 1 - Geral (Homens e Mulheres por região):")
print(tabela_geral.head(10))
print("\n" + "="*80 + "\n")

print("Tabela 2 - STEM (Ciência, Tecnologia, Engenharias e Matemática):")
print(tabela_stem.head(10))
print("\n" + "="*80 + "\n")

print("Tabela 3 - Educação, Serviços pessoais, Saúde e Bem-estar:")
print(tabela_educ_saude.head(10))

if not os.path.exists('output'):
    os.makedirs('output')

tabela_geral.to_excel("output/tabela_geral.xlsx", index=False)
tabela_stem.to_excel("output/tabela_stem.xlsx", index=False)
tabela_educ_saude.to_excel("output/tabela_educacao_saude.xlsx", index=False)

print("\n" + "="*80)
print("Tabelas salvas com sucesso em:")
print("- output/tabela_geral.xlsx")
print("- output/tabela_stem.xlsx")
print("- output/tabela_educacao_saude.xlsx")
print("="*80 + "\n")

print("\n" + "="*80)
print("ANÁLISE ESTATÍSTICA DAS TRÊS TABELAS")
print("="*80 + "\n")

print("\n" + "-"*40)
print("Tabela 1 - Geral (todas as áreas):")
print("-"*40)
print(tabela_geral[['Total_Homens', 'Total_Mulheres', 'Total_Regiao']].describe())
print("\n")

print("\n" + "-"*40)
print("Tabela 2 - STEM (Ciência, Tecnologia, Engenharias e Matemática):")
print("-"*40)
print(tabela_stem[['STEM_Homens', 'STEM_Mulheres', 'STEM_Total']].describe())
print("\n")

print("\n" + "-"*40)
print("Tabela 3 - Educação, Serviços pessoais, Saúde e Bem-estar:")
print("-"*40)
print(tabela_educ_saude[['Educacao_Saude_Homens', 'Educacao_Saude_Mulheres', 'Educacao_Saude_Total']].describe())
print("\n")

print("\n" + "="*80)
print("ANÁLISES ADICIONAIS")
print("="*80 + "\n")

print("\nProporção de homens e mulheres (Geral) - Top 5 regiões com mais mulheres:")
tabela_geral['Prop_Mulheres'] = (tabela_geral['Total_Mulheres'] / tabela_geral['Total_Regiao'] * 100)
tabela_geral_sorted = tabela_geral.sort_values('Prop_Mulheres', ascending=False)
print(tabela_geral_sorted[['Regiao', 'Prop_Mulheres']].head(10))

print("\nProporção de homens e mulheres na área STEM - Top 5 regiões com mais mulheres:")
tabela_stem['Prop_Mulheres_STEM'] = (tabela_stem['STEM_Mulheres'] / tabela_stem['STEM_Total'] * 100)
tabela_stem_sorted = tabela_stem.sort_values('Prop_Mulheres_STEM', ascending=False)
print(tabela_stem_sorted[['Regiao', 'Prop_Mulheres_STEM']].head(10))

print("\nProporção de homens e mulheres na área Educação/Saúde - Top 5 regiões com mais mulheres:")
tabela_educ_saude['Prop_Mulheres_Educ'] = (tabela_educ_saude['Educacao_Saude_Mulheres'] / tabela_educ_saude['Educacao_Saude_Total'] * 100)
tabela_educ_saude_sorted = tabela_educ_saude.sort_values('Prop_Mulheres_Educ', ascending=False)
print(tabela_educ_saude_sorted[['Regiao', 'Prop_Mulheres_Educ']].head(10))

print("\n" + "="*80)
print("RESUMO POR GRANDES REGIÕES")
print("="*80 + "\n")

regioes = {
    'Norte': ['Rondônia', 'Acre', 'Amazonas', 'Roraima', 'Pará', 'Amapá', 'Tocantins'],
    'Nordeste': ['Maranhão', 'Piauí', 'Ceará', 'Rio Grande do Norte', 'Paraíba', 'Pernambuco', 'Alagoas', 'Sergipe', 'Bahia'],
    'Sudeste': ['Minas Gerais', 'Espírito Santo', 'Rio de Janeiro', 'São Paulo'],
    'Sul': ['Paraná', 'Santa Catarina', 'Rio Grande do Sul'],
    'Centro-Oeste': ['Mato Grosso do Sul', 'Mato Grosso', 'Goiás', 'Distrito Federal']
}

def agregar_por_regiao(df, col_homens, col_mulheres, col_total):
    dados = {}
    for regiao, estados in regioes.items():
        mask = df['Regiao'].isin(estados)
        dados[regiao] = {
            'Homens': df.loc[mask, col_homens].sum(),
            'Mulheres': df.loc[mask, col_mulheres].sum(),
            'Total': df.loc[mask, col_total].sum()
        }
    return pd.DataFrame(dados).T

resumo_geral = agregar_por_regiao(tabela_geral, 'Total_Homens', 'Total_Mulheres', 'Total_Regiao')
resumo_stem = agregar_por_regiao(tabela_stem, 'STEM_Homens', 'STEM_Mulheres', 'STEM_Total')
resumo_educ = agregar_por_regiao(tabela_educ_saude, 'Educacao_Saude_Homens', 'Educacao_Saude_Mulheres', 'Educacao_Saude_Total')

print("\nResumo por Grande Região - Geral:")
print(resumo_geral)
print("\nResumo por Grande Região - STEM:")
print(resumo_stem)
print("\nResumo por Grande Região - Educação/Saúde:")
print(resumo_educ)

with pd.ExcelWriter('output/analises_adicionais.xlsx') as writer:
    tabela_geral.to_excel(writer, sheet_name='Geral', index=False)
    tabela_stem.to_excel(writer, sheet_name='STEM', index=False)
    tabela_educ_saude.to_excel(writer, sheet_name='Educacao_Saude', index=False)
    resumo_geral.to_excel(writer, sheet_name='Resumo_Geral')
    resumo_stem.to_excel(writer, sheet_name='Resumo_STEM')
    resumo_educ.to_excel(writer, sheet_name='Resumo_Educ_Saude')

print("\n" + "="*80)
print("Análises adicionais salvas em output/analises_adicionais.xlsx")
print("="*80 + "\n")

print("\n" + "="*80)
print("CONCLUSÕES PRINCIPAIS")
print("="*80 + "\n")

total_homens = tabela_geral['Total_Homens'].sum()
total_mulheres = tabela_geral['Total_Mulheres'].sum()
total_geral = total_homens + total_mulheres

print(f"Total de pessoas com nível superior completo no Brasil: {total_geral:,.0f}")
print(f"  - Homens: {total_homens:,.0f} ({total_homens/total_geral*100:.1f}%)")
print(f"  - Mulheres: {total_mulheres:,.0f} ({total_mulheres/total_geral*100:.1f}%)")

total_stem_homens = tabela_stem['STEM_Homens'].sum()
total_stem_mulheres = tabela_stem['STEM_Mulheres'].sum()
total_stem = total_stem_homens + total_stem_mulheres

print(f"\nTotal de pessoas na área STEM: {total_stem:,.0f}")
print(f"  - Homens: {total_stem_homens:,.0f} ({total_stem_homens/total_stem*100:.1f}%)")
print(f"  - Mulheres: {total_stem_mulheres:,.0f} ({total_stem_mulheres/total_stem*100:.1f}%)")

total_educ_homens = tabela_educ_saude['Educacao_Saude_Homens'].sum()
total_educ_mulheres = tabela_educ_saude['Educacao_Saude_Mulheres'].sum()
total_educ = total_educ_homens + total_educ_mulheres

print(f"\nTotal de pessoas na área Educação/Saúde: {total_educ:,.0f}")
print(f"  - Homens: {total_educ_homens:,.0f} ({total_educ_homens/total_educ*100:.1f}%)")
print(f"  - Mulheres: {total_educ_mulheres:,.0f} ({total_educ_mulheres/total_educ*100:.1f}%)")

prop_mulheres_geral = total_mulheres / total_geral * 100
prop_mulheres_stem = total_stem_mulheres / total_stem * 100
prop_mulheres_educ = total_educ_mulheres / total_educ * 100

print(f"\nProporção de mulheres por área:")
print(f"  - Geral: {prop_mulheres_geral:.1f}%")
print(f"  - STEM: {prop_mulheres_stem:.1f}%")
print(f"  - Educação/Saúde: {prop_mulheres_educ:.1f}%")

print("\n" + "="*80)