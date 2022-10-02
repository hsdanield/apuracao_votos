import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats
from scipy.stats import norm
import altair as alt
import requests as requests


# print response
response = requests.get('https://resultados.tse.jus.br/oficial/ele2022/544/dados-simplificados/br/br-c0001-e000544-r.json')
dados = response.json()


candidatos = dados["cand"]
secao_totalizada = dados["pst"]
horario_atualizacao = dados["ht"]
total_voto = dados["tv"]

st.write("Seção Totalizada: ", secao_totalizada)
st.write("Última atualização: ", horario_atualizacao)
st.write("Total de Voto: ", total_voto)


df = pd.DataFrame(candidatos, columns=["nm", "vap", "pvap"])     \
                                      .rename(columns={"nm": "nome","pvap":"porcentagem", "vap": "votos"})


df_chart = df[["nome", "porcentagem"]]
df_chart["porcentagem"] = df_chart["porcentagem"].apply(lambda x: x.replace(",", ".")).astype(float)
df_chart = df_chart.sort_values("porcentagem", ascending=False).head()

chart = (
    alt.Chart(df_chart)
    .mark_bar(color="#61b33b", point=True)
    .encode(
        x=alt.X("nome:O", title="nome", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("porcentagem:Q", title="Porcentagem (%)"),
        # opacity="nome:O",
        color="nome"
        
    )
    .properties(width=800, height=600)
)
# Place conversion rate as text above each bar
chart_text = chart.mark_text(
    align="center", baseline="middle", dy=-10, color="white"
).encode(text=alt.Text("porcentagem:Q", format=",.3g"))

st.altair_chart( (chart + chart_text).interactive())
st.table(df)

