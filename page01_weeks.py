#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
import plotly.express as px

# cc = ss.df_weeks[list(ss.df_weeks.keys())[1]]

# st.dataframe(ss.df_weeks[list(ss.df_weeks.keys())[1]]  , width = "content")

def make_lineplot_by_age_and_sex_1(x, tit):

    if "type" in x.columns:
        x = x[x["type"] == "all"]

    fig = px.line(
        data_frame = x,
        x = "date",
        y = "value",
        color = "agegroup",
        facet_row= "sex",
        title = tit,
        height = 1000
        )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="gray", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="gray", mirror=True)
    
    return fig


for k in ss.df_weeks.keys():
    try:
        df = ss.df_weeks[k] 
        fig = make_lineplot_by_age_and_sex_1(df, k)
        st.plotly_chart(fig, use_container_width=True)
    except:
        print("caca")    
    
