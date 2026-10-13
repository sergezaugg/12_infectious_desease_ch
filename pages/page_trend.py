
import streamlit as st
from streamlit import session_state as ss
import numpy as np
import plotly.express as px
import pandas as pd





# moving average 
df = ss.df_months_all_concat
df = df.sort_values(["disease", "date"])
ss.df_months_all_concat["value_ma_12m"] = (
    df.groupby("disease")["value"]
    .transform(lambda s: s.rolling(12, center=True, min_periods=3).median())
    .groupby(df["disease"])
    .transform(lambda s: s.rolling(5, center=True, min_periods=1, ).mean())
)


df['residuals'] = df['value'] - df['value_ma_12m']


df_long = df.melt(
    id_vars=[c for c in df.columns if c not in ["value", "value_ma_12m"]],
    value_vars=["value", "value_ma_12m"],
    var_name="measure",
    value_name="outcome"
)

# st.dataframe(df_long)

fig_smo = px.line(
    data_frame = df_long,
    x = "date",
    y = "outcome",
    color = "measure",
    facet_row= "disease",
    facet_row_spacing = 0.01,
    # markers=True,
    height = 6500,
    color_discrete_map={
        "value": "#03bc41",
        "value_ma_12m": "#e74c3c",
    },
    )
fig_smo.update_yaxes(matches=None)

fig_res = px.line(
    data_frame = df,
    x = "date",
    y = "residuals",
    facet_row= "disease",
    facet_row_spacing = 0.01,
    height = 6500,
    # color_discrete_map=["#ffffff","#e74c3c"],
    )

fig_res.update_yaxes(matches=None)



c0, c1 = st.columns(2)
with c0:
    st.plotly_chart(fig_smo, use_container_width=True, key = "aaaaaa")
with c1:    
    st.plotly_chart(fig_res, use_container_width=True, key = "bbbbbb")




