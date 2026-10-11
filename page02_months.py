#--------------------             
# Author : Serge Zaugg
# Description : TBD
#--------------------

import pandas as pd 
import streamlit as st
from streamlit import session_state as ss
from utils import download_all_data, data_pre_select, data_select_chfl
from utils import data_select_years, data_select_months, data_select_weeks
import plotly.express as px

# cc = ss.df_months[list(ss.df_months.keys())[1]]

# st.dataframe(ss.df_months[list(ss.df_months.keys())[1]], width = "content")

def make_lineplot_by_age_and_sex_2(x, tit):
    fig = px.line(
        data_frame = x,
        x = "date",
        y = "value",
        color = "agegroup",
        facet_row= "sex",
        title = tit,
        height = 500

        )
    fig.update_xaxes(showline=True, linewidth=1, linecolor="gray", mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor="gray", mirror=True)
    return fig

for k in ss.df_months.keys():
    try:
        df = ss.df_months[k] 
        fig = make_lineplot_by_age_and_sex_2(df, k)
        st.plotly_chart(fig, use_container_width=True)
    except:
        print("caca")    

